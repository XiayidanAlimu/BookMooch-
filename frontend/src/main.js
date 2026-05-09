import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { registerPlugins } from './plugins/registerPlugins'
import { initRequestService } from './service/http'
import App from './App.vue'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
registerPlugins(app)
initRequestService()

app.mount('#app')
