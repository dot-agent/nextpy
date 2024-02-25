<template>
  <div ref="dropzone" class="solara-file-drop" effectAllowed="move">
    {{ (file_info && file_info.length === 1) ? file_info[0].name : label }}
  </div>
</template>

<script>
module.exports = {
  mounted() {
    this.chunk_size = 2 * 1024 * 1024;
    this.$refs.dropzone.addEventListener('dragover', event => {
      event.preventDefault();
    });

    this.$refs.dropzone.addEventListener('drop', async event => {
      event.preventDefault();
      const items = await Promise.all([...event.dataTransfer.items]);
      const files = items.map(i => i.webkitGetAsEntry())
      const fileHolder = files.filter(f => f.isFile)[0]
      const file = await new Promise((rs, rj) => fileHolder.file(rs, rj))

      this.native_file_info = [file]
      this.file_info = this.native_file_info.map(
          ({name, isFile, size}) => ({
            name,
            isFile,
            size,
          }));
    });
  },
  methods: {
    jupyter_clear() {
      this.native_file_info = [];
      this.file_info = [];
    },
    jupyter_read(chunk) {
      const {id, file_index, offset, length} = chunk;
      let to_do = length;
      let sub_offset = offset;

      (async () => {
        while (to_do > 0) {
          console.log(this.chunk_size, to_do);
          const sub_length = Math.min(to_do, this.chunk_size);

          const file = this.native_file_info[file_index];
          const blob = file.slice(sub_offset, sub_offset + sub_length);
          const buff = await blob.arrayBuffer();

          const msg = {id, file_index, offset: sub_offset, length: sub_length}
          this.upload(msg, [buff]);

          to_do -= sub_length
          sub_offset += sub_length
        }
      })();
    }
  }
}
</script>

<style id="solara-file-drop">
.solara-file-drop {
  height: 100px;
  border: 1px dashed gray;
  margin: 8px 0;
  padding: 8px
}
</style>
