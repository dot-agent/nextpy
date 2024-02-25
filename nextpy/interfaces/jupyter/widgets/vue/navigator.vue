<template>
  <span></span>
</template>
​
<script>
modules.export = {
  created() {
    history.scrollRestoration = "manual";
    if (!window.solara) {
      window.solara = {};
    }
    if (!window.solara.router) {
      window.solara.router = {};
    }
    window.solara.router.push = (href) => {
      console.log("external router push", href);
      // take of the anchor
      if (href.indexOf("#") !== -1) {
        href = href.slice(0, href.indexOf("#"));
      }
      this.location = href;
    };
    let location = window.location.pathname.slice(solara.rootPath.length);
    // take of the anchor
    if (location.indexOf("#") !== -1) {
      location = location.slice(0, location.indexOf("#"));
    }
    this.location = location + window.location.search;
    window.addEventListener("popstate", this.onPopState);
    window.addEventListener("scroll", this.onScroll);
  },
  destroyed() {
    window.removeEventListener("popstate", this.onPopState);
    window.removeEventListener("scroll", this.onScroll);
  },
  methods: {
    onScroll() {
      window.history.replaceState(
        { top: document.documentElement.scrollTop },
        null,
        solara.rootPath + this.location
      );
    },
    onPopState(event) {
      console.log("pop state!", event.state, window.location.href);
      if (!window.location.pathname.startsWith(solara.rootPath)) {
        throw `window.location.pathname = ${window.location.pathname}, but it should start with the solara.rootPath = ${solara.rootPath}`;
      }
      let newLocation = window.location.pathname.slice(solara.rootPath.length);
      // the router/server shouldn't care about the hash, that's for the frontend
      if (newLocation.indexOf("#") !== -1) {
        newLocation = newLocation.slice(0, newLocation.indexOf("#"));
      }
      this.location = newLocation + window.location.search;
      if (event.state) {
        const top = event.state.top;
        /*
        // we'd like to restore the scroll position, but we do not know when yet
        // maybe we will have a life cycle hook for this in the future
        setTimeout(() => {
          document.documentElement.scrollTop = top;
        }, 500);
        */
      }
    },
  },
  watch: {
    location(value) {
      console.log("changed", this.location, value);
      pathnameNew = (new URL(value, window.location)).pathname
      pathnameOld = window.location.pathname
      // if we use the back navigation, this watch will trigger,
      // but we don't want to push the history
      // otherwise we cannot go forward
      if (!window.location.pathname.startsWith(solara.rootPath)) {
        throw `window.location.pathname = ${window.location.pathname}, but it should start with the solara.rootPath = ${solara.rootPath}`;
      }
      const oldLocation = window.location.pathname.slice(solara.rootPath.length) + window.location.search;
      console.log(
        "location changed",
        oldLocation,
        this.location,
        document.documentElement.scrollTop
      );
      if (oldLocation != this.location) {
        window.history.pushState({ top: 0 }, null, solara.rootPath + this.location);
        if (pathnameNew != pathnameOld) {
          // we scroll to the top only when we change page, not when we change
          // the search string
          window.scrollTo(0, 0);
        }
        const event = new Event('solara.router');
        window.dispatchEvent(event);
      }
    },
  },
};
</script>
