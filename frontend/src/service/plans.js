export const PlanType = {
  CLASSIC: 'classic',
  PREMIUM: 'premium'
};

export const PLAN_LIMITS = {
  [PlanType.CLASSIC]: {
    name: 'Classic',
    max_guests: 100,
    max_pages: 2,
    max_sites: 1,
    has_cover_page: true,
    has_rsvp_form: false,
    can_use_tables: true,
    can_customize_extensively: false
  },
  [PlanType.PREMIUM]: {
    name: 'Premium',
    max_guests: 500,
    max_pages: 10,
    max_sites: 5,
    has_cover_page: true,
    has_rsvp_form: true,
    can_use_tables: true,
    can_customize_extensively: true
  }
};

export const getPlanInfo = (planName) => {
  return PLAN_LIMITS[planName] || PLAN_LIMITS[PlanType.CLASSIC];
};
