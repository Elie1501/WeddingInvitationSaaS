from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.db.session import get_db
from app.api import deps
from app.models.wedding import WeddingTable, Guest, Event, User
from app.schemas.table import TableCreate, TableResponse
from app.api.plans import get_limits

router = APIRouter()

@router.get("/event/{event_id}", response_model=List[TableResponse])
def list_tables(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Liste toutes les tables d'un mariage."""
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
    """Crée une nouvelle table."""
    event = db.query(Event).filter(Event.id == table_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    new_table = WeddingTable(**table_in.model_dump())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.delete("/{table_id}")
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Supprime une table."""
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
    """Assigne un invité à une table avec vérification d'événement et de capacité."""
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()

    if not table or not guest:
        raise HTTPException(status_code=404, detail="Table ou invité introuvable")

    # CONTRAINTE MÉTIER : Un invité ne peut être affecté qu'à une table appartenant au même événement
    if table.event_id != guest.event_id:
        raise HTTPException(
            status_code=400, 
            detail="L'invité et la table doivent appartenir au même événement."
        )

    # Vérifier la capacité
    if len(table.guests) >= table.capacity:
        raise HTTPException(status_code=400, detail="La table est déjà pleine")

    # Vérifier si l'invité est déjà à cette table
    if guest in table.guests:
        return table

    # Désassigner l'invité de TOUTES ses tables actuelles (règle : 1 invité = 1 place)
    guest.assigned_tables = []
    
    table.guests.append(guest)
    db.commit()
    db.refresh(table)
    return table

@router.get("/event/{event_id}/status")
def get_tables_status(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Consulte l'état de remplissage global de toutes les tables de l'événement."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    tables = db.query(WeddingTable).filter(WeddingTable.event_id == event_id).all()
    
    status = []
    total_capacity = 0
    total_seated = 0
    
    for t in tables:
        seated = len(t.guests)
        total_capacity += t.capacity
        total_seated += seated
        status.append({
            "id": t.id,
            "name": t.name,
            "capacity": t.capacity,
            "seated_count": seated,
            "is_full": seated >= t.capacity
        })
    
    return {
        "tables": status,
        "total_capacity": total_capacity,
        "total_seated": total_seated,
        "overall_fill_rate": (total_seated / total_capacity * 100) if total_capacity > 0 else 0
    }

@router.post("/{table_id}/unassign/{guest_id}", response_model=TableResponse)
def unassign_guest_from_table(
    table_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_use_tables"))
):
    """Retire un invité d'une table."""
    table = db.query(WeddingTable).join(Event).filter(WeddingTable.id == table_id, Event.owner_id == current_user.id).first()
    guest = db.query(Guest).filter(Guest.id == guest_id).first()

    if not table or not guest:
        raise HTTPException(status_code=404, detail="Table ou invité introuvable")

    if guest in table.guests:
        table.guests.remove(guest)
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
    """Exporte le plan de table au format CSV."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    tables = db.query(WeddingTable).filter(WeddingTable.event_id == event_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Table", "Capacité", "Places occupées", "Invités"])
    
    for table in tables:
        guest_names = ", ".join([f"{g.first_name} {g.last_name}" for g in table.guests])
        writer.writerow([table.name, table.capacity, len(table.guests), guest_names])
    
    content = output.getvalue()
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=plan_de_table_{event_id}.csv"}
    )
