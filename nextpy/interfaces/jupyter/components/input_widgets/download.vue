<template>
    <div @click="request_download = true" class="solara-file-download-container">
        <jupyter-widget v-for="child in children" :key="child" :widget="child"></jupyter-widget>
    </div>
</template>

<script>
module.exports = {
    watch: {
        bytes(value) {
            if (this.request_download) {
                const a = document.createElement('a');
                a.download = this.filename;
                const blob = new Blob([this.bytes], { type: this.mime_type });
                const blobUrl = window.URL.createObjectURL(blob);
                a.href = blobUrl;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                setTimeout(() => {
                    // Make sure we clean up
                    window.URL.revokeObjectURL(blobUrl);
                }, 1000);
                this.request_download = false;
            }
        }
    }
}
</script>

<style id="solara-file-download">
.solara-file-download-container {
    cursor: pointer;
}
</style>
