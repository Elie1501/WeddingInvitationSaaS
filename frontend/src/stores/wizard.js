import { defineStore } from 'pinia';

export const useWizardStore = defineStore('wizard', {
  state: () => ({
    step:       1,
    groomName:  '',
    brideName:  '',
    date:       '',
    location:   '',
    style:      'all',
  }),

  actions: {
    next() { if (this.step < 4) this.step++; },
    prev() { if (this.step > 1) this.step--; },

    reset() {
      this.$patch({ step: 1, groomName: '', brideName: '', date: '', location: '', style: 'all' });
    },

    save() {
      localStorage.setItem('wizard_data', JSON.stringify({
        groomName: this.groomName,
        brideName: this.brideName,
        date:      this.date,
        location:  this.location,
        style:     this.style,
      }));
    },
  },
});
