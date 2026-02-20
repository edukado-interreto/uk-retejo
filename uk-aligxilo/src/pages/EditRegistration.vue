<template>
  <template v-if="error !== undefined">
    <congress-header />
    <n-alert :title="errorTitle" type="error">
      {{ error }}
    </n-alert>
  </template>
  <div
      v-else-if="data === undefined"
      class="loading"
  >
    <n-spin size="large" />
  </div>
  <template v-else>
    <congress-header />
    <n-h2>Mendilo por {{ name }} (kongresnumero {{ data.KN }})</n-h2>
    <main-form :default-data="data" :edit="true" />
  </template>
</template>

<script>
import CongressHeader from "@/components/layout/CongressHeader.vue";
import MainForm from "@/components/MainForm.vue";
import axios from "axios";
import {useMessage} from "naive-ui";

export default {
  name: "EditRegistration",
  components: {MainForm, CongressHeader},
  data() {
    return {
      uniqueId: undefined,
      data: undefined,
      errorTitle: undefined,
      error: undefined,
      message: useMessage(),
    }
  },
  computed: {
    name() {
      return `${this.data.persona_nomo} ${this.data.familia_nomo}`.trim();
    }
  },
  methods: {
    fetchData() {
      axios.post('/getRegistration', { id: this.uniqueId })
          .then(result => {
            if (result.data.success) {
              this.data = result.data.registration;
              this.data.akcepto_reguloj = true;
              this.data.kompreno_pago = true;
            }
            else {
              this.error = result.data.error;
              this.errorTitle = result.data.errorTitle;
            }
          })
          .catch((error) => {
            this.message.error(error, {
              keepAliveOnHover: true
            });
          });
    }
  },
  created() {
    this.uniqueId = this.$route.params.id;
    if (this.uniqueId === undefined) {
      this.errorTitle = 'Mankanta identigilo';
      this.error = 'Se vi volas mendi servojn, bonvolu uzi la ligilon, kiu estis sendita al vi per retpoŝto.';
    }
    else {
      this.fetchData();
    }
  }
}
</script>

<style scoped>
.loading {
  text-align: center;
  margin-top: 10vh;
  margin-bottom: 10vh;
  transform: scale(3);
}
</style>