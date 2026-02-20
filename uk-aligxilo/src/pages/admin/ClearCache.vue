<template>
  <admin-breadcrumbs title="Forigi kaŝmemoron" />

  <loading-spinner v-if="loading" />
  <template v-else>
    <n-alert type="info" v-if="files.length === 0">Ne estas kaŝmemoro.</n-alert>
    <template v-else>
      <n-table style="max-width: 400px">
        <tbody>
          <tr v-for="file in files" :key="file">
            <td>{{ file }}</td>
            <td style="text-align: right">
              <n-button @click="clear(file)" :loading="loadingFiles.includes(file)" type="error" size="small">
                Forigi
              </n-button>
            </td>
          </tr>
        </tbody>
      </n-table>

      <p>
        <n-button @click="clearAll" :loading="clearAllLoading" type="primary"> Forigi ĉion </n-button>
      </p>
    </template>
  </template>

  <p v-if="!loading">
    <n-button @click="loaddata" type="default"> Refreŝigi </n-button>
  </p>
</template>

<script>
import AdminBreadcrumbs from '@/components/admin/AdminBreadcrumbs.vue';
import { mapGetters } from 'vuex';
import axios from 'axios';
import { useMessage, NTable } from 'naive-ui';
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue';

export default {
  name: 'ClearCache',
  components: { LoadingSpinner, NTable, AdminBreadcrumbs },
  data() {
    return {
      loading: true,
      clearAllLoading: false,
      message: useMessage(),
      files: [],
      loadingFiles: [],
    };
  },
  computed: {
    ...mapGetters(['key']),
  },
  methods: {
    loaddata() {
      this.loading = true;
      axios
        .post('/admin/getcache', { key: this.key })
        .then((response) => {
          this.files = response.data.files;
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    clearAll() {
      this.clearAllLoading = true;
      axios
        .post('/clearCache', { key: this.key })
        .then(() => {
          this.files = [];
          this.message.success('Kaŝmemoro forigita.', {
            keepAliveOnHover: true,
          });
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.clearAllLoading = false;
        });
    },
    clear(file) {
      this.loadingFiles.push(file);
      axios
        .post('/admin/deletecachefile', { key: this.key, filename: file })
        .then(() => {
          this.files = this.files.filter((f) => f !== file);
          this.message.success(`La dosiero ${file} estis forigita.`, {
            keepAliveOnHover: true,
          });
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.loadingFiles = this.loadingFiles.filter((f) => f !== file);
        });
    },
  },
  created() {
    this.loaddata();
  },
};
</script>
