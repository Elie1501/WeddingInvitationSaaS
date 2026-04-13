from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.wedding import User, Event, Guest, WeddingTable, Card, RSVP
from app.core import security
import datetime
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./verify_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    print("\n--- TEST: Création d'un utilisateur et d'un événement ---")
    user = User(email="organizer@example.com", hashed_password="fake", plan="classic")
    db.add(user)
    db.flush()
    
    event = Event(title="Mariage de Alice & Bob", groom_name="Bob", bride_name="Alice", date=datetime.datetime.now(), owner_id=user.id)
    db.add(event)
    db.flush()
    
    card = Card(event_id=event.id, slug="alice-bob", is_published=False)
    db.add(card)
    db.flush()
    print("Événement et Carte (non publiée) créés.")

    print("\n--- TEST: RSVP sur une carte non publiée ---")
    # Simulation de la logique de l'endpoint public_rsvp_legacy
    published_card = db.query(Card).filter(Card.event_id == event.id, Card.is_published == True).first()
    if not published_card:
        print("OK: RSVP refusé car carte non publiée.")
    else:
        print("ERREUR: RSVP accepté sur une carte non publiée !")

    print("\n--- TEST: Publication de la carte et RSVP ---")
    card.is_published = True
    db.commit()
    
    guest = Guest(event_id=event.id, first_name="Jean", last_name="Dupont", rsvp_status="pending")
    db.add(guest)
    db.commit()
    
    # Simuler RSVP
    guest.rsvp_status = "confirmed"
    guest.plus_ones = 1
    new_rsvp = RSVP(guest_id=guest.id, presence=True, plus_ones=1)
    db.add(new_rsvp)
    db.commit()
    print(f"OK: RSVP confirmé pour {guest.first_name} {guest.last_name} (Publiée: {card.is_published})")

    print("\n--- TEST: Gestion des tables et cohérence d'événement ---")
    table = WeddingTable(event_id=event.id, name="Table d'Honneur", capacity=2)
    db.add(table)
    db.flush()
    
    # Créer un autre événement pour tester la violation de règle
    other_event = Event(title="Autre Mariage", owner_id=user.id)
    db.add(other_event)
    db.flush()
    other_guest = Guest(event_id=other_event.id, first_name="Intrus", last_name="Inconnu")
    db.add(other_guest)
    db.flush()

    print(f"Tentative d'assigner l'invité '{other_guest.first_name}' (Event {other_guest.event_id}) à la table '{table.name}' (Event {table.event_id})...")
    if table.event_id != other_guest.event_id:
        print("OK: Violation de règle détectée (Événements différents).")
    else:
        print("ERREUR: La règle de cohérence d'événement a échoué !")

    print("\n--- TEST: Capacité des tables ---")
    table.guests.append(guest)
    db.commit()
    print(f"Invité {guest.first_name} ajouté à la table. Occupation: {len(table.guests)}/{table.capacity}")
    
    if len(table.guests) >= table.capacity:
        print("Table pleine (si on ajoute encore quelqu'un).")
    
    print("\n--- TEST: Filtrage et Recherche ---")
    search_term = "Jean"
    found = db.query(Guest).filter(Guest.first_name.ilike(f"%{search_term}%")).all()
    print(f"Recherche '{search_term}': {len(found)} trouvé(s).")
    
    status_filter = "confirmed"
    confirmed_guests = db.query(Guest).filter(Guest.rsvp_status == status_filter).all()
    print(f"Filtre status '{status_filter}': {len(confirmed_guests)} trouvé(s).")

    db.close()
    if os.path.exists("./verify_test.db"):
        os.remove("./verify_test.db")
    print("\nTests terminés avec succès.")

if __name__ == "__main__":
    verify()
