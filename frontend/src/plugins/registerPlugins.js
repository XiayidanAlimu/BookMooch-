import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import VxeUIBase from 'vxe-pc-ui'
import 'vxe-pc-ui/lib/style.css'

export const registerPlugins = (app) => {
  app.use(ArcoVue)
  app.use(VxeUIBase)
}
