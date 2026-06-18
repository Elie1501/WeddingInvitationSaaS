from typing import Dict, Any, FrozenSet

# ─── Forfait des comptes non encore payés ──────────────────────────────────────
# Un nouveau compte démarre sans forfait : aucun accès produit tant que Stripe
# n'a pas confirmé le paiement (paywall strict). Le plan réel est posé par
# confirm-payment / le webhook Stripe.
UNPAID_PLAN: str = "none"

# Forfaits réellement payés (donnant accès au produit).
PAID_PLANS: FrozenSet[str] = frozenset({"classic", "premium"})

# Rang des forfaits pour la garde anti double-paiement (non payé = 0).
PLAN_RANK: Dict[str, int] = {UNPAID_PLAN: 0, "classic": 1, "premium": 2}


def has_paid_plan(plan_name: str) -> bool:
    """True si le forfait donne accès au produit (Classic ou Premium)."""
    return (plan_name or UNPAID_PLAN) in PAID_PLANS


# ─── Prix en centimes d'euro ───────────────────────────────────────────────────
PLAN_PRICES: Dict[str, int] = {
    "classic": 2900,   # 29,00 €
    "premium": 7900,   # 79,00 €
}

# ─── Sections/blocs réservés au forfait Premium ────────────────────────────────
# Ces IDs sont comparés avec config_json.sections lors de chaque auto-save.
PREMIUM_SECTION_IDS: FrozenSet[str] = frozenset({
    "countdown",
    "program",
    "custom-text",
    "image",
})

# ─── Limites par forfait ──────────────────────────────────────────────────────
PLAN_LIMITS: Dict[str, Dict[str, Any]] = {
    "classic": {
        "max_pages":                3,
        "max_sites":                1,
        "has_cover_page":           True,
        "has_rsvp_form":            True,
        "can_use_tables":           True,
        "can_customize_extensively": True,
        "can_import_export":        False,
        "can_upload_music":         False,
        "can_edit_typography":      False,
        "can_export_csv":           False,
    },
    "premium": {
        "max_pages":                20,
        "max_sites":                5,
        "has_cover_page":           True,
        "has_rsvp_form":            True,
        "can_use_tables":           True,
        "can_customize_extensively": True,
        "can_import_export":        True,
        "can_upload_music":         True,
        "can_edit_typography":      True,
        "can_export_csv":           True,
    },
}


def get_limits(plan_name: str) -> Dict[str, Any]:
    plan_name = (plan_name or "classic").lower()
    return PLAN_LIMITS.get(plan_name, PLAN_LIMITS["classic"])


def get_upgrade_amount() -> int:
    """Montant de l'upgrade Classic → Premium en centimes (différence uniquement)."""
    return PLAN_PRICES["premium"] - PLAN_PRICES["classic"]  # 5000 = 50,00 €
