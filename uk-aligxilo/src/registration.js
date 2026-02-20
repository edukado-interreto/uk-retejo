import axios from "axios"
import { createApp } from "vue"
import Registration from "./embedded/Registration.vue"
import mixins from "./mixins.js"
import naive from "./plugins/naive-ui.js"
import store from "./store.js"

axios.defaults.baseURL = import.meta.env.VITE_API_URL

const app = createApp(Registration)
app.use(store)
app.use(naive)
app.mixin(mixins)

app.mount("#vue-registration")
