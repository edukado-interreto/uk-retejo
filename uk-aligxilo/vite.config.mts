import { fileURLToPath, URL } from "node:url"
import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

const absolute = (path: string) => fileURLToPath(import.meta.resolve(path))

// https://vite.dev/config/build-options.html
// https://vite.dev/guide/env-and-mode.html#modes
// https://vitejs.dev/config/
export default defineConfig(() => ({
  base: "/static/vue/",
  build: {
    outDir: absolute("../apps/registration/static/vue"),
    emptyOutDir: true,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        registration: "src/registration.js",
        edit: "src/edit.js",
      },
    },
  },
  clearScreen: false,
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: { host: "0.0.0.0", port: 5173 },
}))
