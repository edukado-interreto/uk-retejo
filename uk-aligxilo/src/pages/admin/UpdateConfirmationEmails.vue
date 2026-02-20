<template>
  <admin-breadcrumbs title="Mesaĝoj pri konfirmo de mendoj" />

  <loading-spinner v-if="loading" />
  <template v-else>
    <n-table :single-line="false" striped v-if="participants.length > 0">
      <thead>
        <tr>
          <th>KN</th>
          <th>Nomo</th>
          <th>UEA-kodo</th>
          <th>
            <span @click="checkAll" style="margin-right: 7px">Sendi?</span>
            <n-checkbox @update:checked="checkAll" :checked="checkedAll" />
          </th>
          <th>Antaŭvidi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="participant in participants" :key="participant.unique_id">
          <td @click="toggleSend(participant.unique_id)">{{ participant.KN }}</td>
          <td @click="toggleSend(participant.unique_id)">
            {{ participant.persona_nomo }} {{ participant.familia_nomo }}
          </td>
          <td @click="toggleSend(participant.unique_id)">{{ participant.uea_kodo }}</td>
          <td>
            <n-checkbox
              @update:checked="toggleSend(participant.unique_id)"
              :checked="sendIds.includes(participant.unique_id)"
            />
          </td>
          <td>
            <n-button @click="preview(participant.unique_id, participant.retadreso)" type="info" size="small">
              Antaŭvidi
            </n-button>
          </td>
        </tr>
      </tbody>
    </n-table>
    <n-alert type="info" v-else>Ne estas konfirmaj mesaĝoj por sendi.</n-alert>

    <n-modal
      v-model:show="showModal"
      preset="card"
      style="max-width: 1000px"
      :title="'Mesaĝo sendota al ' + emailTo"
      size="small"
    >
      <div v-if="previewLoading" class="loading">
        <n-spin size="large" />
      </div>
      <div v-else v-html="previewHtml"></div>
    </n-modal>

    <p>
      <n-space>
        <n-button
          v-if="participants.length > 0"
          type="primary"
          @click="send"
          :loading="sendLoading"
          :disabled="sendIds.length === 0"
        >
          Sendi
        </n-button>
        <n-button @click="loaddata" type="default"> Refreŝigi </n-button>
      </n-space>
    </p>
    <n-card title="Klarigoj" style="margin-top: 1.6rem">
      <p style="margin-top: 0">Por povi sendi konfirman mesaĝon pri ŝanĝo de mendo:</p>
      <ul style="margin-bottom: 0">
        <li>iru al la folio <code>Akceptejo</code>,</li>
        <li>
          en la kolumno <code>konfirma_mesagxo</code> (kolumno AB, se nenio ŝanĝiĝis), skribu <code>sendi</code> ĉe la
          koncerna kongresano,
        </li>
        <li>
          eventuale skribu aldonan tekston, kiu devas aperi en la mesaĝo, en la kolumno
          <code>aldona_informo_por_la_mesagxo</code>.
        </li>
      </ul>
    </n-card>
  </template>
</template>

<script>
import AdminBreadcrumbs from '@/components/admin/AdminBreadcrumbs.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue';

export default {
  name: 'UpdateConfirmationEmails',
  components: { LoadingSpinner, AdminBreadcrumbs },
  data() {
    return {
      loading: true,
      participants: [],
      sendIds: [],
      showModal: false,
      previewLoading: false,
      previewHtml: '',
      sendLoading: false,
    };
  },
  computed: {
    ...mapGetters(['key']),
    checkedAll() {
      return this.participants.length === this.sendIds.length;
    },
  },
  methods: {
    loaddata() {
      this.loading = true;
      this.sendIds = [];
      axios
        .post('/admin/getchangestoconfirm', { key: this.key })
        .then((response) => {
          this.participants = response.data.participants;
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
    toggleSend(id) {
      if (this.sendIds.includes(id)) {
        this.sendIds = this.sendIds.filter((i) => i !== id);
      } else {
        this.sendIds.push(id);
      }
    },
    checkAll() {
      if (this.checkedAll) {
        this.sendIds = [];
      } else {
        this.sendIds = this.participants.map((p) => p.unique_id);
      }
    },
    preview(id, email) {
      this.showModal = true;
      this.emailTo = email;
      this.previewLoading = true;
      this.previewHtml = '';
      axios
        .post('/admin/previewchangeconfirmationemail', { key: this.key, id })
        .then((response) => {
          this.previewHtml = response.data;
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.previewLoading = false;
        });
    },
    send() {
      this.sendLoading = true;
      axios
        .post('/admin/sendchangeconfirmationemails', { key: this.key, ids: this.sendIds })
        .then((response) => {
          this.participants = response.data.participants;
          this.sendIds = [];
        })
        .catch((error) => {
          this.message.error(error, {
            keepAliveOnHover: true,
          });
        })
        .finally(() => {
          this.sendLoading = false;
        });
    },
  },
  created() {
    this.loaddata();
  },
};
</script>
