import axios from "axios"
import { config, enableAutoUnmount } from "@vue/test-utils"
import { afterEach, beforeEach, expect, vi } from "vitest"

import mixins from "@/mixins.js"
import naive from "@/plugins/naive-ui.js"
import store from "@/store.js"
import { apiAdapter, resetApi, unhandledRequests } from "./support/api.js"
import { checkConsole, resetConsole } from "./support/console.js"

// Stripe is loaded from js.stripe.com at runtime: never touch the network in tests
vi.mock("@stripe/stripe-js", () => {
  const element = { mount: () => {}, on: () => {}, addEventListener: () => {}, destroy: () => {} }
  const stripe = {
    elements: () => ({ create: () => element }),
    handleCardPayment: async () => ({ paymentIntent: { id: "pi_test" } }),
  }
  return { loadStripe: async () => stripe }
})

// Same wiring as entrypoints/*.js
axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.defaults.adapter = apiAdapter
config.global.plugins = [store, naive]
config.global.mixins = [mixins]

// A fixed "today", so date dependent UI (registration periods, default dates) is stable
export const NOW = new Date("2027-02-15T10:00:00Z")

const initialState = JSON.stringify(store.state)
// Tests may change the path (Edit.vue reads the booking id from it): restore it, keeping
// the original URL so that it also works inside the iframe of Vitest browser mode
const initialUrl = window.location.href

beforeEach(() => {
  vi.setSystemTime(NOW)
  window.history.replaceState({}, "", initialUrl)
  store.replaceState(JSON.parse(initialState))
  resetApi()
  resetConsole()
  vi.stubGlobal("fetch", async (url) => {
    unhandledRequests.push(`fetch ${url}`)
    throw new Error(`Unmocked fetch ${url}`)
  })
})

// afterEach hooks run in reverse order: unmount, clean the DOM, then check the logs
afterEach(() => {
  vi.useRealTimers()
  checkConsole()
  expect(unhandledRequests, "requests without a mock in tests/support/api.js").toEqual([])
})
afterEach(() => {
  document.body.innerHTML = ""
})
enableAutoUnmount(afterEach)
