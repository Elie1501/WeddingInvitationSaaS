# WeddingInvitation SaaS

## Lancer le projet

```bash
docker-compose up -d
```

## Lancer les seeds

```bash
docker-compose exec backend python scripts/seed_users.py && docker-compose exec backend python scripts/seed_templates.py && docker-compose exec backend python scripts/seed_art_templates.py && docker-compose exec backend python scripts/seed_ultimate_minimal.py && docker-compose exec backend python scripts/seed_ora_template.py
```

## Relancer Docker + Seeds (tout en une fois)

```bash
docker-compose down && docker-compose up -d --build && docker-compose exec backend python scripts/seed_users.py && docker-compose exec backend python scripts/seed_templates.py && docker-compose exec backend python scripts/seed_art_templates.py && docker-compose exec backend python scripts/seed_ultimate_minimal.py && docker-compose exec backend python scripts/seed_ora_template.py
```

## URLs

| Service   | URL                        |
|-----------|----------------------------|
| Frontend  | http://localhost:5173      |
| API       | http://localhost:8000      |
| Adminer   | http://localhost:8080      |

## Comptes de test

| Email                  | Mot de passe | Plan    | Admin |
|------------------------|--------------|---------|-------|
| marie@classic.com      | password123  | classic | Non   |
| thomas@premium.com     | password123  | premium | Non   |
| admin@wedding.com      | password123  | premium | Oui   |
