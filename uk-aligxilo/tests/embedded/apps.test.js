import { describe, expect, it, vi } from "vitest"

import FormBooking from "@/components/form/parts/FormBooking.vue"

import PeriodCards from "@/components/kotizoj/PeriodCards.vue"
import PriceTable from "@/components/kotizoj/PriceTable.vue"
import Edit from "@/embedded/Edit.vue"
import Participants from "@/embedded/Participants.vue"
import Price from "@/embedded/Price.vue"
import Registration from "@/embedded/Registration.vue"
import { mockApi, requests } from "../support/api.js"
import { expectBookingWarnings } from "../support/known-bugs.js"
import { mountApp, settle } from "../support/mount.js"

describe("Registration", () => {
  it("renders the registration form once the data is loaded", async () => {
    const wrapper = await mountApp(Registration)
    expect(requests.map((r) => r.url)).toEqual(["/loaddata"])
    expect(wrapper.find("form.mainform").exists()).toBe(true)
  })
})

describe("Price", () => {
  it("renders the price page", async () => {
    const wrapper = await mountApp(Price)
    expect(wrapper.findComponent(PriceTable).exists() || wrapper.findComponent(PeriodCards).exists()).toBe(true)
  })
})

describe("Participants", () => {
  it("renders the security question", async () => {
    const wrapper = await mountApp(Participants)
    expect(wrapper.find(".n-card input").exists()).toBe(true)
  })
})

describe("Edit", () => {
  it("renders the edit form with the booking part", async () => {
    expectBookingWarnings()
    window.history.replaceState({}, "", "/mendilo/abc123")
    const wrapper = await mountApp(Edit)
    await vi.waitFor(() => expect(wrapper.findComponent(FormBooking).exists()).toBe(true))
    await settle()
    expect(wrapper.find("form.mainform").exists()).toBe(true)
    expect(wrapper.find(".n-alert[role=alert]").exists()).toBe(false)
  })

  it("shows an error instead of the form without a booking id in the URL", async () => {
    const wrapper = await mountApp(Edit)
    expect(wrapper.find(".n-alert[role=alert]").exists()).toBe(true)
    expect(wrapper.find("form").exists()).toBe(false)
  })

  it("shows the error of the server", async () => {
    mockApi("POST", "/getRegistration", { success: false, error: "x", errorTitle: "y" })
    window.history.replaceState({}, "", "/mendilo/abc123")
    const wrapper = await mountApp(Edit)
    expect(wrapper.find(".n-alert[role=alert]").exists()).toBe(true)
    expect(wrapper.find("form").exists()).toBe(false)
    expect(wrapper.find(".n-spin").exists()).toBe(false)
  })

  it("shows an error when the request fails", async () => {
    mockApi("POST", "/getRegistration", () => new Error("Network Error"))
    window.history.replaceState({}, "", "/mendilo/abc123")
    const wrapper = await mountApp(Edit)
    expect(wrapper.find(".n-alert[role=alert]").exists()).toBe(true)
    expect(wrapper.find("form").exists()).toBe(false)
  })
})
