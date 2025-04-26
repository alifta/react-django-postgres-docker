import { defineConfig } from 'vite'

export default defineConfig({
    base: "/static/",
    build: {
      manifest: "manifest.json",
      outDir: resolve("./assets"),
      rollupOptions: {
        input: {
          <unique key>: '<path to your asset>'
        }
      }
    }
  })