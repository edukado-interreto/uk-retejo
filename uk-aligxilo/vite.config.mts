import { readdirSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

const absolute = (path: string) => fileURLToPath(import.meta.resolve(path))

const BASE_PATH = "/static/vue/"

const ENTRYPOINTS = Object.fromEntries(
  readdirSync("./entrypoints")
    .map(path.parse)
    .map((f: path) => [f.name, `entrypoints/${f.base}`])
)

const codeSplitting = {
  groups: [{ name: "naive-ui", test: /node_modules\/naive-ui/ }],
}

export default defineConfig(() => ({
  base: BASE_PATH,
  build: {
    outDir: absolute(`../backend/apps/registration${BASE_PATH}`),
    emptyOutDir: true,
    manifest: "manifest.json",
    rolldownOptions: {
      input: ENTRYPOINTS,
      output: { codeSplitting },
    },
  },
  clearScreen: false,
  plugins: [vue()],
  resolve: { alias: { "@": absolute("./src") } },
  server: { host: "0.0.0.0", port: 5173 },
}))
