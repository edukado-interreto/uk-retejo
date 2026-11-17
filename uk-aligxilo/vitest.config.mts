import { readdirSync } from "node:fs"
import { fileURLToPath } from "node:url"

import vue from "@vitejs/plugin-vue"
import { configDefaults, defineConfig } from "vitest/config"

import { reachableFromEntrypoints } from "./tests/support/reachable.mjs"

// Standalone config on purpose: vite.config.mts writes the production build into
// ../backend, so the test runner must never load its `build` section.
const absolute = (path: string) => fileURLToPath(import.meta.resolve(path))

export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { "@": absolute("./src") } },
  test: {
    environment: "happy-dom",
    include: ["tests/**/*.test.js"],
    // Screenshot tests run in a real browser, see vitest.visual.config.mts
    exclude: [...configDefaults.exclude, "tests/visual/**"],
    setupFiles: ["tests/setup.js"],
    // Same values in every environment so that snapshots never depend on a local .env file
    env: {
      VITE_API_URL: "http://api.test",
      VITE_WEBSITE_URL: "http://website.test",
      VITE_STRIPE_PUBLISHABLE_KEY: "pk_test_dummy",
    },
    // Full form mounts take ~0.3 s locally; keep a margin for slow or busy CI runners
    testTimeout: 20_000,
    restoreMocks: true,
    unstubGlobals: true,
    coverage: {
      provider: "v8",
      // Only the code the entrypoints use; pages nobody imports (leftovers of the former
      // vue-router app) are not counted. Follows the imports, so new components join by themselves.
      include: reachableFromEntrypoints(readdirSync("entrypoints").map((f) => `entrypoints/${f}`)),
      reporter: ["text-summary", "text", "html"],
      reportsDirectory: "coverage",
      // The CI fails below these. v8 counts every template arrow function, hence the lower functions value
      thresholds: { statements: 90, branches: 90, lines: 90, functions: 80 },
    },
  },
})
