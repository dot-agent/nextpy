<template>
    <div>
        <div ref="plotElement"></div>
    </div>
</template>
<script>
module.exports = {
    created() {
        this.vegaLoaded = this.loadVega();
        this.do_plot_debounced = _.debounce(async () => {
            await this.vegaLoaded;
            this.do_plot()
        }, 100)
    },
    mounted() {
        this.do_plot_debounced();
    },
    watch: {
        spec() {
            this.do_plot_debounced();
        },
        listen_to_click() {
            this.do_plot_debounced();
        }
    },
    methods: {
        do_plot() {
            require(['vega', 'vega-lite', 'vega-embed'], (vega, vl, vegaEmbed) => {
                (async () => {
                    const spec = {
                        ...this.spec,
                    };
                    const { view } = await vegaEmbed(this.$refs.plotElement, spec);
                    // events https://github.com/vega/vega-view#event-handling
                    if (this.listen_to_click) {
                        view.addEventListener('click', (event, item) => {
                            if (item && item.datum) {
                                this.altair_click(item.datum);
                            } else {
                                this.altair_click(null)
                            }
                        })
                    }
                    if (this.listen_to_hover) {
                        view.addEventListener('mouseover', (event, item) => {
                            if (item && item.datum) {
                                this.altair_hover(item.datum);
                            } else {
                                this.altair_hover(null)
                            }
                        })
                    }
                })();
            });
        },
        async loadVega() {
            await this.loadRequire();
            requirejs.undef("vega")
            requirejs.undef("vega-lite")
            requirejs.undef("vega-embed")
            require.config({
                map: {
                    '*': {
                        'vega': `${this.getCdn()}/vega@5/build/vega.min.js`,
                        'vega-lite': `${this.getCdn()}/vega-lite@5/build/vega-lite.min.js`,
                        'vega-embed': `${this.getCdn()}/vega-embed@6/build/vega-embed.min.js`,
                    }
                }
            })
            // pre load
            await new Promise((resolve, reject) => {
                require(['vega', 'vega-lite', 'vega-embed'], () => {
                    resolve()
                }, reject)
            });
        },
        loadRequire() {
            /* Needed in lab */
            if (window.requirejs) {
                console.log('require found');
                return Promise.resolve()
            }
            return new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = `${this.getCdn()}/requirejs@2.3.6/require.js`;
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        },
        getBaseUrl() {
            if (window.solara && window.solara.rootPath !== undefined) {
                return solara.rootPath + "/";
            }
            // if base url is set, we use ./ for relative paths compared to the base url
            if (document.getElementsByTagName("base").length) {
                return "./";
            }
            const labConfigData = document.getElementById('jupyter-config-data');
            if (labConfigData) {
                /* lab and Voila */
                return JSON.parse(labConfigData.textContent).baseUrl;
            }
            let base = document.body.dataset.baseUrl || document.baseURI;
            if (!base.endsWith('/')) {
                base += '/';
            }
            return base
        },
        getCdn() {
            return (typeof solara_cdn !== "undefined" && solara_cdn) || `${this.getBaseUrl()}_solara/cdn`;
        }
    },
}
</script>
