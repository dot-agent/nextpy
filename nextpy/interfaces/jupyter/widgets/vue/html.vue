<template>
    <component :is="tag" v-bind="attributes" v-html="unsafe_innerHTML">
    </component>
</template>

<script>
module.exports = {
    mounted() {
        // maybe we should not do this for the html component, but do a separate
        // markdown element?
        mermaid.init()
    },
    updated() {
        // if the html gets update, rerun mermaid
        mermaid.init()
    }
}
</script>
