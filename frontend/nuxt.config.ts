// https://nuxt.com/docs/api/configuration/nuxt-config
// import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  css: [
    '@unocss/reset/tailwind.css'
  ],
  runtimeConfig: {
    // Private keys are only available on the server
    // apiSecret: process.env.NUXT_API_SECRET,
    
    // Public keys that are exposed to the client
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'
    }
  },
  modules: [
    '@nuxt/content',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    'shadcn-nuxt',
    'nuxt-echarts',
    '@nuxtjs/color-mode',
    '@unocss/nuxt',
    '@nuxt/ui',
    '@vueuse/nuxt'
  ],
  colorMode: {
    classSuffix: ''
  },
  features: {
    inlineStyles: false,
  },
  echarts: {
    renderer: ['svg', 'canvas'],
    charts: [
      'BarChart',
      'LineChart',
      'PieChart',
      'ScatterChart',
      'MapChart',
      'HeatmapChart',
      'GraphChart'
    ],
    components: [
      'TitleComponent',
      'TooltipComponent',
      'GridComponent',
      'DatasetComponent',
      'TransformComponent',
      'LegendComponent',
      'ToolboxComponent',
      'VisualMapComponent',
      'GeoComponent',
      'CalendarComponent'
    ]
  },
  // vite: {
  //   plugins: [
  //     tailwindcss(),
  //   ],
  // },
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  }
})