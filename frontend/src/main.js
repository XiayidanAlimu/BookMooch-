import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import { GridLayout, GridItem } from 'vue-grid-layout-v3'
import App from './App.vue'
import './style.css'
import { useUserStore } from './stores/user'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.component('GridLayout', GridLayout)
app.component('GridItem', GridItem)

const userStore = useUserStore()
userStore.initializeAxios()

app.use(ArcoVue)

app.mount('#app')
