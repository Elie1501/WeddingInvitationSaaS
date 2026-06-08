import json
import os
import sys
import uuid

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def seed_ultimate_minimal():
    db = SessionLocal()
    
    # On ne crée plus ce template
    print("Le template Arche d'Or n'est plus utilisé.")
    
    db.close()

if __name__ == "__main__":
    seed_ultimate_minimal()
