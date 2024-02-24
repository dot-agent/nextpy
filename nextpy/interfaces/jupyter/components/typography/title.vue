<template><span style="display: none">{{ title }}</span></template>

<script>
module.exports = {
  mounted() {
    if (window._solaraTitles === undefined) {
      window._solaraTitles = [];
    }
    window._solaraTitles.push(this);
    this.updateTitle();
  },
  destroyed() {
    window._solaraTitles.splice(window._solaraTitles.indexOf(this), 1);
    if (window._solaraTitles.length) {
      window._solaraTitles[0].updateTitle();
    }
  },
  watch: {
    title() {
      this.updateTitle();
    },
    level() {
      this.updateTitle();
    },
  },
  methods: {
    updateTitle() {
      let deepestTitle = window._solaraTitles[0];
      for (let i = 1; i < window._solaraTitles.length; i++) {
        if (window._solaraTitles[i].level > deepestTitle.level) {
          deepestTitle = window._solaraTitles[i];
        }
      }
      document.title = deepestTitle.title;
    }
  },
};
</script>
