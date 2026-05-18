from enum import Enum
from typing import Dict, Any

class PlanType(str, Enum):
    CLASSIC = "classic"
    PREMIUM = "premium"

PLAN_LIMITS: Dict[PlanType, Dict[str, Any]] = {
    PlanType.CLASSIC: {
        "max_pages": 3,
        "max_sites": 1,
        "has_cover_page": True,
        "has_rsvp_form": True,
        "can_use_tables": True,
        "can_customize_extensively": True,
        "can_import_export": False,
        "can_upload_music": False
    },
    PlanType.PREMIUM: {
        "max_pages": 20,
        "max_sites": 5,
        "has_cover_page": True,
        "has_rsvp_form": True,
        "can_use_tables": True,
        "can_customize_extensively": True,
        "can_import_export": True,
        "can_upload_music": True
    }
}

def get_limits(plan_name: str):
    try:
        plan = PlanType(plan_name)
    except ValueError:
        plan = PlanType.CLASSIC
    return PLAN_LIMITS[plan]
