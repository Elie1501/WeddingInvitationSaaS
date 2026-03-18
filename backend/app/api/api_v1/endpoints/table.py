from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api import deps
from app.models.wedding import WeddingTable, Guest, Event, User
from app.schemas.table import TableCreate, TableResponse

router = APIRouter()

@router.post("/", response_model=TableResponse)
def create_table(
    table_in: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Vérification proprio
    event = db.query(Event).filter(Event.id == table_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    new_table = WeddingTable(**table_in.model_dump())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.post("/{table_id}/assign/{guest_id}")
def assign_guest_to_table(
    table_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    table = db.query(WeddingTable).filter(WeddingTable.id == table_id).first()
    guest = db.query(Guest).filter(Guest.id == guest_id).first()

    if not table or not guest:
        raise HTTPException(status_code=404, detail="Table ou invité introuvable")

    # REGLE METIER : Vérifier si l'invité et la table appartiennent au même mariage
    if table.event_id != guest.event_id:
        raise HTTPException(status_code=400, detail="L'invité n'appartient pas à ce mariage")

    # REGLE METIER : Vérifier la capacité
    current_sitting = len(table.guests)
    if current_sitting >= table.capacity:
        raise HTTPException(status_code=400, detail="La table est déjà pleine")

    # Assignation (SQLAlchemy gère la table d'association tout seul !)
    table.guests.append(guest)
    db.commit()
    return {"message": f"{guest.first_name} a été placé à la table {table.name}"}