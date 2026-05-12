import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { registerPlugins } from './plugins/registerPlugins'
import { initRequestService } from './service/http'
import router from './router'
import App from './App.vue'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
registerPlugins(app)
initRequestService()

app.mount('#app')
