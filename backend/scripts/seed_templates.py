import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import CardTemplate, Base
from app.core.config import settings
import json

# On utilise l'URL des settings
db_url = settings.DATABASE_URL

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_templates():
    db = SessionLocal()
    # Création des tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    templates_to_create = []

    for template_data in templates_to_create:
        template = db.query(CardTemplate).filter(CardTemplate.id == template_data["id"]).first()
        if not template:
            new_template = CardTemplate(**template_data)
            db.add(new_template)
            print(f"Template créé : {template_data['name']} ({template_data['id']})")
        else:
            # Mise à jour si déjà existant
            for key, value in template_data.items():
                setattr(template, key, value)
            print(f"Template mis à jour : {template_data['name']}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_templates()
