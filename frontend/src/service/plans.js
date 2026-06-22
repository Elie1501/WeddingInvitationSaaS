export const PlanType = {
  CLASSIC: 'classic',
  PREMIUM: 'premium'
};

export const PLAN_LIMITS = {
  [PlanType.CLASSIC]: {
    name: 'Classic',
    max_pages: 3,
    max_sites: 1,
    has_cover_page: true,
    has_rsvp_form: true,
    can_use_tables: true,
    can_customize_extensively: true,
    can_import_export: false,
    can_upload_music: true
  },
  [PlanType.PREMIUM]: {
    name: 'Premium',
    max_pages: 20,
    max_sites: 5,
    has_cover_page: true,
    has_rsvp_form: true,
    can_use_tables: true,
    can_customize_extensively: true,
    can_import_export: true,
    can_upload_music: true
  }
};

export const getPlanInfo = (planName) => {
  return PLAN_LIMITS[planName] || PLAN_LIMITS[PlanType.CLASSIC];
};
