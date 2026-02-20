<template>
  <n-card
      v-if="!isLoggedIn"
      class="custom-card"
      title="Ensaluto"
  >
    <p>
      <n-input
          type="text"
          size="large"
          style="width: 20em;"
          placeholder="Uzantnomo"
          v-model:value="username"
          @keydown.enter="login"
      />
    </p>
    <p>
      <n-input
          type="password"
          size="large"
          style="width: 20em;"
          placeholder="Pasvorto"
          v-model:value="password"
          @keydown.enter="login"
      />
    </p>
    <p>
      <n-button
          size="large"
          type="primary"
          :loading="loading"
          :disabled="username === '' || password === ''"
          @click="login"
      >
        Ensaluti
      </n-button>
    </p>
  </n-card>
  <template v-else>
    <ul>
      <li>
        <router-link :to="{ name: 'clearCache' }">
          Forigi kaŝmemoron de datumoj el Google Sheets
        </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'updateConfirmationEmails' }">
          Dissendi mesaĝojn pri konfirmo de mendoj
        </router-link>
      </li>
    </ul>

    <p>
      <n-button
          type="primary"
          @click="logout"
      >
        Elsaluti
      </n-button>
    </p>
  </template>
</template>

<script>
import axios from "axios";
import {mapGetters} from "vuex";
import {useMessage} from "naive-ui";

export default {
  name: "AdminPage",
  data() {
    return {
      loading: false,
      username: '',
      password: '',
      message: useMessage(),
    }
  },
  computed: {
    ...mapGetters([
      'key',
      'isLoggedIn',
    ]),
  },
  methods: {
    login() {
      this.loading = true;
      axios.post('/admin/login', { username: this.username, password: this.password })
          .then(result => {
            if (result.data.success) {
              this.$store.dispatch('login', result.data.key);
              localStorage.setItem('adminKey', result.data.key);
            }
            else {
              this.message.error("Malĝusta uzantnomo aŭ pasvorto.", {
                keepAliveOnHover: true
              });
            }
          })
          .catch((error) => {
            this.message.error(error, {
              keepAliveOnHover: true
            });
          })
          .finally(() => {
            this.loading = false;
          });
    },
    logout() {
      this.$store.dispatch('logout');
      localStorage.removeItem('adminKey')
    },
  },
  created() {
    if (localStorage.getItem('adminKey') !== null) {
      this.$store.dispatch('login', localStorage.getItem('adminKey'));
    }
  }
}
</script>

<style scoped>
li a {
  text-decoration: none;
  color: #0030DB;
}

li a:hover, li a:active, li a:focus {
  text-decoration: underline;
  color: #3366FF;
}
</style>