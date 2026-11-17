// The server calls and error handling behind the card payment. Stripe itself is mocked in
// tests/setup.js, and fetch answers what each test says.
import { mount } from "@vue/test-utils"
import { describe, expect, it, vi } from "vitest"

import StripableFormdict from "@/components/form/fields/StripableFormdict.vue"
import { settle } from "../support/mount.js"

const props = {
  formdict: { lando: "FR" },
  stripe_key: "pk_test_dummy",
  card_owner_fullname: "Ana Bertrand",
  card_owner_email: "ana@example.org",
  server_endpoint: "http://server.test/",
  please_wait: false,
}

async function mountStripable(changes = {}) {
  const wrapper = mount(StripableFormdict, { props: { ...props, ...changes } })
  await settle()
  return wrapper
}

/** Answer the fetch calls in order; an Error is thrown, anything else is the body. */
function mockFetch(...answers) {
  const bodies = []
  vi.stubGlobal("fetch", async (url, init) => {
    bodies.push(JSON.parse(init.body))
    const answer = answers[bodies.length - 1]
    if (answer instanceof Error) throw answer
    const text = typeof answer === "string" ? answer : JSON.stringify(answer)
    return { text: async () => text, json: async () => JSON.parse(text) }
  })
  return bodies
}

const serverError = { error_code: "ERR_SERVER", error_msg: "No" }
const rejection = (promise) => promise.then(() => null, (error) => error)

describe("StripableFormdict", () => {
  it("loads Stripe and mounts the card element", async () => {
    const wrapper = await mountStripable()
    expect(wrapper.vm.stripe).toBeDefined()
    expect(wrapper.vm.card_element).toBeDefined()
    expect(wrapper.find("#card_element").exists()).toBe(true)
  })

  describe("calculate_price", () => {
    it("asks the server for the price of the form and signals the wait", async () => {
      const wrapper = await mountStripable()
      const bodies = mockFetch({ sum: 42 })
      expect(await wrapper.vm.calculate_price()).toEqual({ sum: 42 })
      expect(bodies).toEqual([{ op: "calculate-price", formdict: props.formdict }])
      expect(wrapper.emitted()).toHaveProperty("wait_start")
      expect(wrapper.emitted()).toHaveProperty("wait_end")
    })

    it("does nothing while another request is running", async () => {
      const wrapper = await mountStripable({ please_wait: true })
      const bodies = mockFetch({ sum: 1 })
      expect(await wrapper.vm.calculate_price()).toBeUndefined()
      expect(bodies).toEqual([])
    })

    it("throws the error of the server", async () => {
      const wrapper = await mountStripable()
      mockFetch(serverError)
      expect(await rejection(wrapper.vm.calculate_price())).toMatchObject(serverError)
    })

    it("throws a network error when the request fails", async () => {
      const wrapper = await mountStripable()
      mockFetch(new Error("offline"))
      const error = await rejection(wrapper.vm.calculate_price())
      expect(error.error_code).toBe("ERR_NETWORK")
      expect(wrapper.emitted()).toHaveProperty("wait_end")
    })
  })

  describe("signup", () => {
    it("sends the form for direct processing and returns the answer", async () => {
      const wrapper = await mountStripable()
      const bodies = mockFetch({ success: true })
      expect(await wrapper.vm.signup()).toEqual({ success: true })
      expect(bodies).toEqual([{ op: "direct-process", formdict: props.formdict }])
    })

    it("does nothing while another request is running", async () => {
      const wrapper = await mountStripable({ please_wait: true })
      const bodies = mockFetch({ success: true })
      expect(await wrapper.vm.signup()).toBeUndefined()
      expect(bodies).toEqual([])
    })

    it("throws the error of the server", async () => {
      const wrapper = await mountStripable()
      mockFetch(serverError)
      expect(await rejection(wrapper.vm.signup())).toMatchObject(serverError)
    })

    it("throws a network error when the answer is not JSON", async () => {
      const wrapper = await mountStripable()
      mockFetch("<html>502 Bad Gateway</html>")
      const error = await rejection(wrapper.vm.signup())
      expect(error.error_code).toBe("ERR_NETWORK")
      expect(error.server_response).toContain("502")
    })

    it("throws a network error when the request fails", async () => {
      const wrapper = await mountStripable()
      mockFetch(new Error("offline"))
      expect((await rejection(wrapper.vm.signup())).error_code).toBe("ERR_NETWORK")
    })
  })

  describe("signup_pay", () => {
    const pay = { client_secret: "secret" }

    it("asks for a secret, pays with Stripe, and confirms the payment", async () => {
      const wrapper = await mountStripable()
      const bodies = mockFetch(pay, { success: true })
      expect(await wrapper.vm.signup_pay()).toEqual({ success: true })
      expect(bodies.map((b) => b.op)).toEqual(["pre-payment", "post-payment"])
      expect(bodies[1].intent).toBe("pi_test")
    })

    it("does nothing while another request is running", async () => {
      const wrapper = await mountStripable({ please_wait: true })
      const bodies = mockFetch(pay)
      expect(await wrapper.vm.signup_pay()).toBeUndefined()
      expect(bodies).toEqual([])
    })

    it("stops when the server refuses the payment", async () => {
      const wrapper = await mountStripable()
      mockFetch(serverError)
      expect(await rejection(wrapper.vm.signup_pay())).toMatchObject(serverError)
    })

    it("stops when the pre-payment answer is not JSON", async () => {
      const wrapper = await mountStripable()
      mockFetch("oops")
      expect((await rejection(wrapper.vm.signup_pay())).error_code).toBe("ERR_NETWORK")
    })

    it("throws the message of Stripe when the card is refused", async () => {
      const wrapper = await mountStripable()
      vi.spyOn(wrapper.vm.stripe, "handleCardPayment").mockResolvedValue({ error: { message: "Card declined" } })
      mockFetch(pay)
      expect(await rejection(wrapper.vm.signup_pay())).toMatchObject({
        error_code: "ERR_STRIPE",
        error_msg: "Card declined",
      })
    })

    it("throws a fatal error when Stripe is not reachable", async () => {
      const wrapper = await mountStripable()
      vi.spyOn(wrapper.vm.stripe, "handleCardPayment").mockRejectedValue(new Error("blocked"))
      mockFetch(pay)
      expect((await rejection(wrapper.vm.signup_pay())).error_code).toBe("ERR_STRIPE_FATAL")
    })

    it("throws the error of the server after the payment", async () => {
      const wrapper = await mountStripable()
      mockFetch(pay, serverError)
      expect(await rejection(wrapper.vm.signup_pay())).toMatchObject(serverError)
    })

    it("throws a network error when the confirmation fails", async () => {
      const wrapper = await mountStripable()
      mockFetch(pay, new Error("offline"))
      expect((await rejection(wrapper.vm.signup_pay())).error_code).toBe("ERR_NETWORK")
    })
  })
})
