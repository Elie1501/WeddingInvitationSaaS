import os
import json
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def deploy_templates(templates_dir: str):
    db: Session = SessionLocal()
    try:
        for template_name in os.listdir(templates_dir):
            template_path = os.path.join(templates_dir, template_name)
            if not os.path.isdir(template_path):
                continue
            
            manifest_path = os.path.join(template_path, "manifest.json")
            if not os.path.exists(manifest_path):
                if HAS_YAML:
                    manifest_path = os.path.join(template_path, "manifest.yaml")
                else:
                    print(f"Skipping {template_name}: no manifest.json found and PyYAML not installed.")
                    continue
            
            if not os.path.exists(manifest_path):
                print(f"Skipping {template_name}: no manifest found.")
                continue
            
            with open(manifest_path, "r") as f:
                if manifest_path.endswith(".json"):
                    manifest = json.load(f)
                elif manifest_path.endswith(".yaml") and HAS_YAML:
                    manifest = yaml.safe_load(f)
                else:
                    print(f"Skipping {template_name}: unsupported manifest format.")
                    continue
            
            template_id = manifest.get("id")
            if not template_id:
                print(f"Skipping {template_name}: 'id' missing in manifest.")
                continue
            
            db_template = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
            if db_template:
                print(f"Updating template: {template_id}")
                db_template.name = manifest.get("name")
                db_template.description = manifest.get("description")
                db_template.required_plan = manifest.get("required_plan", "classic")
                db_template.manifest_json = json.dumps(manifest)
                db_template.thumbnail_url = manifest.get("thumbnail_url")
            else:
                print(f"Creating template: {template_id}")
                db_template = CardTemplate(
                    id=template_id,
                    name=manifest.get("name"),
                    description=manifest.get("description"),
                    required_plan=manifest.get("required_plan", "classic"),
                    manifest_json=json.dumps(manifest),
                    thumbnail_url=manifest.get("thumbnail_url")
                )
                db.add(db_template)
        
        db.commit()
        print("Templates deployed successfully.")
    except Exception as e:
        print(f"Error deploying templates: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_template.py <templates_dir>")
    else:
        deploy_templates(sys.argv[1])
