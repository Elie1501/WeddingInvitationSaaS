import json
import os
import sys

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def seed_extended_art_templates():
    db = SessionLocal()
    
    new_templates = [
        {
            "id": "noir-eternel",
            "name": "Noir Éternel",
            "description": "L'élégance absolue du noir profond et de l'or mat. Un design prestigieux pour une union d'exception.",
            "thumbnail_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=800",
            "manifest": {
                "layout": "noir-eternel",
                "sections": ["noir-eternel-full"],
                "theme": {
                    "background": "#0A0A0A",
                    "accent": "#C9A84C",
                    "text": "#F5E6C8",
                    "fontFamily": "Playfair Display"
                },
                "content": {
                    "names": "Emma & Lucas",
                    "monogram": "E & L",
                    "romanDate": "XV · VI · MMXXVI"
                }
            }
        },
        {
            "id": "template-japonais",
            "name": "Jardin Japonais",
            "description": "Esthétique Wabi-sabi, taches d'encre et sérénité. Un voyage poétique pour une union zen.",
            "thumbnail_url": "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=400&q=80",
            "manifest": {
                "layout": "arch",
                "sections": ["japonais-full", "program", "footer"],
                "theme": {
                    "background": "#F5F0E8",
                    "accent": "#B8960C",
                    "text": "#1A1A1A",
                    "fontFamily": "Noto Serif JP"
                },
                "content": {
                    "names": "Yumi & Kenzo",
                    "image_url": "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=1200",
                    "divider_symbol": "❀"
                }
            }
        },
        {
            "id": "template-riviera",
            "name": "Riviera Anni 70",
            "description": "L'élégance vintage de la Côte d'Azur. Soleil, nostalgie et Dolce Vita.",
            "thumbnail_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=400&q=80",
            "manifest": {
                "layout": "split",
                "sections": ["riviera-full", "program", "footer"],
                "theme": {
                    "background": "#FAF7F0",
                    "accent": "#C1440E",
                    "text": "#C1440E",
                    "fontFamily": "Cormorant"
                },
                "content": {
                    "names": "Anita & Marcello",
                    "image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1200"
                }
            }
        },
        {
            "id": "template-brutaliste",
            "name": "Architecture Brutaliste",
            "description": "Radical, puissant et moderne. Pour ceux qui redéfinissent les codes du mariage.",
            "thumbnail_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&q=80",
            "manifest": {
                "layout": "es",
                "sections": ["brutaliste-full", "program", "footer"],
                "theme": {
                    "background": "#9E9E9E",
                    "accent": "#FF3E00",
                    "text": "#000000",
                    "fontFamily": "Inter"
                },
                "content": {
                    "names": "RACHEL / THOMAS",
                    "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200"
                }
            }
        },
        {
            "id": "template-film",
            "name": "Sépia & Film Argentique",
            "description": "Le glamour intemporel du cinéma classique. Une romance sur grand écran.",
            "thumbnail_url": "https://images.unsplash.com/photo-1437603565260-19658b689228?w=400&q=80",
            "manifest": {
                "layout": "typography-focus",
                "sections": ["film-full", "program", "footer"],
                "theme": {
                    "background": "#FFF8F0",
                    "accent": "#8B6914",
                    "text": "#0D0D0D",
                    "fontFamily": "Cormorant SC"
                },
                "content": {
                    "names": "Ava & Clark",
                    "image_url": "https://images.unsplash.com/photo-1437603565260-19658b689228?w=1200"
                }
            }
        },
        {
            "id": "riviera-blanche",
            "name": "Riviera Blanche",
            "description": "Un design éditorial d'une élégance rare, mêlant blanc chaud, bleu marine profond et minimalisme végétal.",
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
            "manifest": {
                "layout": "riviera-blanche",
                "sections": ["riviera-blanche-full"],
                "theme": { "background": "#FAFAF8", "accent": "#2E6E8E", "text": "#1C2B3A", "fontFamily": "Jost" },
                "content": { "names": "Emma & Lucas" }
            }
        },
        {
            "id": "jardin-celeste",
            "name": "Jardin Céleste",
            "description": "Une immersion poétique dans un vert forêt profond, avec des animations organiques et des touches d'or ambré.",
            "thumbnail_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800",
            "manifest": {
                "layout": "jardin-celeste",
                "sections": ["jardin-celeste-full"],
                "theme": { "background": "#1A2E1F", "accent": "#E8A598", "text": "#F2EBE0", "fontFamily": "Lato" },
                "content": { "names": "Emma & Lucas" }
            }
        },
        {
            "id": "empire-abstrait",
            "name": "Empire Abstrait",
            "description": "Un manifeste architectural. Des formes géométriques radicales et une typographie monumentale en terracotta.",
            "thumbnail_url": "https://images.unsplash.com/photo-1510076857177-7470076d4098?w=800",
            "manifest": {
                "layout": "empire-abstrait",
                "sections": ["empire-abstrait-full"],
                "theme": { "background": "#F7F3EE", "accent": "#C4622D", "text": "#1A0F0A", "fontFamily": "Spectral" },
                "content": { "names": "Emma & Lucas" }
            }
        }
    ]

    for t_data in new_templates:
        # On s'assure que manifest est stocké dans manifest_json et contient default_config
        manifest_to_save = {
            "name": t_data["name"],
            "description": t_data["description"],
            "default_config": t_data["manifest"]
        }
        
        # Check if exists
        existing = db.query(CardTemplate).filter(CardTemplate.id == t_data["id"]).first()
        if existing:
            existing.name = t_data["name"]
            existing.description = t_data["description"]
            existing.thumbnail_url = t_data["thumbnail_url"]
            existing.manifest_json = json.dumps(manifest_to_save)
        else:
            new_t = CardTemplate(
                id=t_data["id"],
                name=t_data["name"],
                description=t_data["description"],
                thumbnail_url=t_data["thumbnail_url"],
                manifest_json=json.dumps(manifest_to_save),
                required_plan="classic",
                is_active=True
            )
            db.add(new_t)
        print(f"Template {t_data['id']} synchronisé.")
    
    db.commit()
    db.close()

    print("Mise à jour des nouveaux templates terminée !")

if __name__ == "__main__":
    seed_extended_art_templates()
