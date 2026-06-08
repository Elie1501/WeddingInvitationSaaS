import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def seed_ky_template():
    db = SessionLocal()
    
    ky_manifest = {
        "layout": "ky",
        "theme": {
            "background": "#0A0A0A",
            "accent": "#C9A84C",
            "text": "#F4F4F4",
            "fontFamily": "Cormorant Garamond"
        },
        "content": {
            "names": "",
            "religious_intro": "B\"H — Sous le regard de Hachem",
            "s1_title": "Union Civile",
            "s1_location_name": "La Mairie",
            "s1_location": "75004 Paris",
            "s2_title": "Cérémonie Religieuse",
            "s2_location_name": "Salons prestigieux",
            "s2_location": "Paris",
            "s2_time": "18h00",
            "rsvp_deadline": "15 Juin 2026",
            "footer_msg": "Hâte de célébrer avec vous"
        }
    }

    template_id = "ky-style"
    existing = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    
    if existing:
        existing.name = "Style Karen & Yossef"
        existing.description = "Une reproduction fidèle du site karen-yossef.fr avec countdown immersif, musique et RSVP complet."
        existing.thumbnail_url = "https://images.unsplash.com/photo-1519741497674-611481863552?w=400"
        existing.manifest_json = json.dumps(ky_manifest)
        existing.required_plan = "premium"
        existing.is_active = True
    else:
        new_tpl = CardTemplate(
            id=template_id,
            name="Style Karen & Yossef",
            description="Une reproduction fidèle du site karen-yossef.fr avec countdown immersif, musique et RSVP complet.",
            thumbnail_url="https://images.unsplash.com/photo-1519741497674-611481863552?w=400",
            manifest_json=json.dumps(ky_manifest),
            required_plan="premium",
            is_active=True
        )
        db.add(new_tpl)
    
    db.commit()
    db.close()
    print(f"Template {template_id} seeded successfully.")

if __name__ == "__main__":
    seed_ky_template()
