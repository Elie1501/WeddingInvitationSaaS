import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api import deps
from app.models.wedding import User
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutRequest(BaseModel):
    plan_name: str # 'classic' ou 'premium'

@router.post("/create-checkout-session")
def create_checkout_session(
    request: CheckoutRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    """Crée une session de paiement Stripe Checkout."""
    
    # Configuration des prix (IDs de prix Stripe réels à mettre dans votre Dashboard Stripe)
    # Ou simulation avec des montants fixes si vous utilisez des adresses de prix dynamiques
    prices = {
        "classic": {
            "amount": 2900, # 29.00€
            "name": "Forfait Mariage Classique"
        },
        "premium": {
            "amount": 7900, # 79.00€
            "name": "Forfait Mariage Premium"
        }
    }

    if request.plan_name not in prices:
        raise HTTPException(status_code=400, detail="Plan invalide")

    plan_data = prices[request.plan_name]

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': plan_data["name"],
                        },
                        'unit_amount': plan_data["amount"],
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"http://localhost:5173/dashboard?payment_success=true&plan={request.plan_name}",
            cancel_url="http://localhost:5173/dashboard?payment_cancel=true",
            metadata={
                "user_id": current_user.id,
                "plan": request.plan_name
            }
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        print(f"Erreur Stripe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook Stripe pour confirmer le paiement et mettre à jour le plan."""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload invalide
        return Response(status_code=400)
    except stripe.error.SignatureVerificationError as e:
        # Signature invalide
        return Response(status_code=400)

    # Gérer l'événement checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        user_id = session.get('metadata', {}).get('user_id')
        new_plan = session.get('metadata', {}).get('plan')
        
        if user_id and new_plan:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.plan = new_plan
                db.commit()
                print(f"Stripe: Plan mis à jour pour l'user {user_id} -> {new_plan}")

    return Response(status_code=200)
