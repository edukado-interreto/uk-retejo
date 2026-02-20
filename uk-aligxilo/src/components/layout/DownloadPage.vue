<template>
  <n-h1>{{ title }}</n-h1>

  <iframe v-if="heyzine" allowfullscreen="allowfullscreen" scrolling="no" class="fp-iframe" :src="heyzine"></iframe>

  <img
    v-for="(imageUrl, index) in imageUrls"
    :key="index"
    :src="imageUrl"
    :alt="title"
    @click="downloadFile"
    class="bulteno"
  />

  <div class="download">
    <n-button @click="downloadFile" type="primary" size="large" :class="{ 'show-small': accusative }">
      Elŝuti kiel PDF-dosieron ({{ size }})
    </n-button>
    <n-button v-if="accusative" @click="downloadFile" type="primary" size="large" class="show-big">
      Elŝuti la {{ accusative }} kiel PDF-dosieron ({{ size }})
    </n-button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import download from 'downloadjs';
import prettyBytes from 'pretty-bytes';

const props = defineProps({
  title: String,
  filesize: Number,
  imgPath: {
    type: [String, Array],
    default: null,
  },
  pdfPath: String,
  heyzine: {
    type: String,
    default: null,
  },
  accusative: {
    type: String,
    default: null,
  },
});

const imageUrls = computed(() => {
  if (!!props.imgPath) {
    const paths = typeof props.imgPath === 'string' ? [props.imgPath] : props.imgPath;
    return paths.map((p) => import.meta.env.BASE_URL + p);
  }
  return [];
});
const downloadUrl = computed(() => (props.pdfPath ? import.meta.env.BASE_URL + props.pdfPath : null));
const size = computed(() => prettyBytes(parseInt(props.filesize), { locale: 'eo' }));

function downloadFile() {
  download(downloadUrl.value);
}
</script>

<style scoped>
img.bulteno {
  cursor: pointer;
  border-radius: 3px;
  display: block;
  margin: auto;
  box-shadow: 2px 2px 5px #00000034;
}

img.bulteno + img.bulteno {
  margin-top: 2em;
}

.download {
  margin-top: 1rem;
  text-align: center;
}

iframe {
  border: 1px solid lightgray;
  border-radius: 5px;
  width: 99%;
  min-height: 250px;
  height: calc(100vh - 330px);
}

@media screen and (max-width: 512px) {
  iframe {
    height: calc(100vh - 420px);
  }
}

.show-small {
  display: none;
}

@media screen and (max-width: 640px) {
  .show-big {
    display: none;
  }
  .show-small {
    display: inline-block;
  }
}
</style>
