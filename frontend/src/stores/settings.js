import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    windowWidth: typeof window !== 'undefined' ? window.innerWidth : 0,
    windowHeight: typeof window !== 'undefined' ? window.innerHeight : 0,
  }),
  actions: {
    initWindowSize() {
      if (typeof window !== 'undefined') {
        this.updateWindowSize(window.innerWidth, window.innerHeight)
      }
    },
    updateWindowSize(width, height) {
      this.windowWidth = width
      this.windowHeight = height
    },
  },
})
