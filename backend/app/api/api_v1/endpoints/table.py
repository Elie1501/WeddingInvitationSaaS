from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.db.session import get_db
from app.api import deps
from app.models.wedding import WeddingTable, Guest, Event, User
from app.schemas.table import TableCreate, TableUpdate, TableResponse

router = APIRouter()

@router.get("/event/{event_id}", response_model=List[TableResponse])
def list_tables(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return db.query(WeddingTable).filter(WeddingTable.event_id == event_id).all()

@router.post("/", response_model=TableResponse)
def create_table(
    table_in: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    event = db.query(Event).filter(Event.id == table_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    new_table = WeddingTable(**table_in.model_dump())
    new_table.remaining_seats = new_table.capacity
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_in: TableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Modifie le nom ou la capacité d'une table."""
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table non trouvée")

    if table_in.name is not None:
        table.name = table_in.name

    if table_in.capacity is not None:
        seated = table.capacity - table.remaining_seats
        if table_in.capacity < seated:
            raise HTTPException(
                status_code=400,
                detail=f"Impossible de réduire la capacité : {seated} invité(s) déjà assigné(s)."
            )
        table.remaining_seats = table_in.capacity - seated
        table.capacity = table_in.capacity

    db.commit()
    db.refresh(table)
    return table

@router.delete("/{table_id}")
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table non trouvée")
    db.delete(table)
    db.commit()
    return {"message": "Table supprimée"}

@router.post("/{table_id}/assign/{guest_id}", response_model=TableResponse)
def assign_guest_to_table(
    table_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Assigne un invité (ou sous-invité) à une table. Chaque personne = 1 place."""
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()

    if not table or not guest:
        raise HTTPException(status_code=404, detail="Table ou invité introuvable")

    if guest in table.guests:
        return table

    # Libérer l'ancienne place si déjà assigné ailleurs
    for old_table in guest.assigned_tables:
        old_table.remaining_seats += 1
    
    if table.remaining_seats < 1:
        raise HTTPException(status_code=400, detail="La table est pleine")

    guest.assigned_tables = [table]
    table.remaining_seats -= 1
    
    db.commit()
    db.refresh(table)
    return table

@router.post("/{table_id}/unassign/{guest_id}", response_model=TableResponse)
def unassign_guest_from_table(
    table_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()

    if not table or not guest:
        raise HTTPException(status_code=404, detail="Table ou invité introuvable")

    if guest in table.guests:
        table.guests.remove(guest)
        table.remaining_seats += 1
        db.commit()
    
    db.refresh(table)
    return table

@router.get("/event/{event_id}/export/csv")
def export_table_plan_csv(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_export"))
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    tables = db.query(WeddingTable).filter(WeddingTable.event_id == event_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Table", "Capacité", "Places occupées", "Membres"])
    
    for table in tables:
        seated = table.capacity - table.remaining_seats
        members = [f"{g.first_name} {g.last_name}" for g in table.guests]
        writer.writerow([table.name, table.capacity, seated, ", ".join(members)])
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=plan_de_table_{event_id}.csv"}
    )