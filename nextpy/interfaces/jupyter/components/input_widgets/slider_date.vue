<template>
  <div>
    <v-slider :label="label" :min="0" :max="days" v-model="value" :disabled="disabled">
      <template v-slot:append>
        <!-- give it a fixed with so the slider doesn't move around -->
        <div class="solara-fixedwidth">
          <div class="solara-makespace">2000-mmm-99</div>
          <div class="solara-realvalue">
            {{ valueDate }}
          </div>
        </div>
      </template>
    </v-slider>
  </div>
</template>
<script>
module.exports = {
  mounted() {},
  computed: {
    startDate() {
      return new Date(this.min * 1000);
    },
    date() {
      const date = new Date(this.startDate);
      date.setDate(date.getDate() + this.value);
      return date;
    },
    valueDate() {
      const date = this.date;
      if (date) {
        const year = date.toLocaleDateString(undefined, { year: "numeric" });
        const month = date.toLocaleDateString(undefined, { month: "short" });
        const day = date.toLocaleDateString(undefined, { day: "numeric" });
        return `${year}-${month}-${day}`;
      }
    },
  },
  watch: {},
};
</script>
<style id="solara-slider-date">
.v-input__append-outer {
  white-space: nowrap;
}
.solara-fixedwidth {
  position: relative;
}
.solara-makespace {
  visibility: hidden;
}
.solara-realvalue {
  position: absolute;
  left: 0;
  top: 0;
}
</style>
