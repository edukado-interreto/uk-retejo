import { fileURLToPath, URL } from "node:url"
import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

const absolute = (path: string) => fileURLToPath(import.meta.resolve(path))

const BASE_PATH = "/static/vue/"

export default defineConfig(() => ({
  base: BASE_PATH,
  build: {
    outDir: absolute(`../backend/apps/registration${BASE_PATH}`),
    emptyOutDir: true,
    manifest: "manifest.json",
    rolldownOptions: {
      input: {
        edit: "src/edit.js",
        participants: "src/participants.js",
        registration: "src/registration.js",
        price: "src/price.js",
      },
      output: {
        codeSplitting: {
          groups: [{ name: "naive-ui", test: /node_modules\/naive-ui/ }],
        },
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
