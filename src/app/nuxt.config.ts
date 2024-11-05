export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    'shadcn-nuxt',
    '@nuxt/icon',
    '@vueuse/motion/nuxt',
    // 'nuxt-security' // Temporarily disable this module to test
  ],

  shadcn: {
    prefix: '',
    componentDir: './components/ui'
  },

  // If you need to configure CORS or other security settings, use the `routeRules` or properly configure `nuxt-security`
  // For now, let's comment out the `security` configuration to test
  /*
  security: {
    headers: {
      // Adjust security headers as necessary
    },
    corsHandler: {
      origin: '*',
      methods: '*',
      credentials: true
    }
  },
  */

  // Remove deprecated `server` property
  // Set host and port using environment variables or `nitro` configuration
  // For production, it's common to set these via environment variables

  // Add the `app` configuration to set base URL and assets directory
  app: {
    baseURL: '/', // Base URL of your application
    buildAssetsDir: '/_nuxt/', // Directory where Nuxt will serve assets
  },

  // Remove `compatibilityDate` as it's not a standard Nuxt configuration
  // compatibilityDate: '2024-08-20',

  // Runtime configuration for environment variables
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || 'http://localhost:8000'
    }
  },

  // Configure Nitro (Nuxt's server engine)
  nitro: {
    // You can set the host and port here if necessary
    // For production, these are typically set via environment variables
    // For example:
    // preset: 'node-server', // Default preset
    // devServer: {
    //   host: '0.0.0.0',
    //   port: 3000
    // }
  },

  // Alternatively, set dev server options (effective during development)
  // This is optional and not usually needed in production
  // devServer: {
  //   host: '0.0.0.0',
  //   port: 3000,
  // },
});

