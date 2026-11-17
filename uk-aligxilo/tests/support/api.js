// In-memory backend for axios. Every request goes through `apiAdapter`, so no test
// can reach the network. Unknown routes fail the test (see tests/setup.js).
import { AxiosError } from "axios"

import loaddata from "../../../backend/apps/devel/data/loaddata.json"
import registration from "../../../backend/apps/devel/data/registration.json"

export const fixtures = {
  loaddata,
  registration,
  // Same shape as backend/apps/devel/views.py:_participants, but deterministic
  participants: {
    success: true,
    participants: [
      { country: "FR", hidden: false, first_name: "Ana", last_name: "Bertrand" },
      { country: "FR", hidden: true, first_name: "Bob", last_name: "Durand" },
      { country: "SK", hidden: false, first_name: "Cyril", last_name: "Novák" },
      { country: "PL", hidden: false, first_name: "Dorota", last_name: "Zielińska" },
      { country: "XX", hidden: false, first_name: "Emil", last_name: "Ŝtono" },
    ],
  },
}

const defaultRoutes = () => ({
  "GET /loaddata": () => fixtures.loaddata,
  "POST /getRegistration": () => fixtures.registration,
  "POST /participants": () => fixtures.participants,
  "POST /checkcode": ({ code }) => ({ valid: !code.endsWith("-x") }),
})

let routes = defaultRoutes()

/** Every request handled so far, in order: { method, url, body }. */
export const requests = []
export const unhandledRequests = []

/**
 * Override or add a route for the current test.
 * `response` is a value, or a function receiving the parsed body. Throw inside the
 * function (or return an Error) to simulate a failed request.
 */
export function mockApi(method, url, response) {
  routes[`${method.toUpperCase()} ${url}`] = typeof response === "function" ? response : () => response
}

export function resetApi() {
  routes = defaultRoutes()
  requests.length = 0
  unhandledRequests.length = 0
}

export async function apiAdapter(config) {
  const method = config.method.toUpperCase()
  const url = config.url.replace(config.baseURL ?? "", "")
  const body = typeof config.data === "string" ? JSON.parse(config.data) : (config.data ?? {})
  requests.push({ method, url, body })

  const handler = routes[`${method} ${url}`]
  if (handler === undefined) {
    unhandledRequests.push(`${method} ${url}`)
    throw new AxiosError(`Unmocked request ${method} ${url}`, "ERR_UNMOCKED", config)
  }
  const data = await handler(body)
  if (data instanceof Error) {
    throw new AxiosError(data.message, "ERR_BAD_RESPONSE", config)
  }
  return { data: structuredClone(data), status: 200, statusText: "OK", headers: {}, config, request: {} }
}
