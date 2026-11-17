import { describe, expect, it } from "vitest"

import Participants from "@/embedded/Participants.vue"
import { fixtures, mockApi, requests } from "../support/api.js"
import { mountApp, settle } from "../support/mount.js"

const { participants } = fixtures.participants

async function answerQuestion(wrapper, year = "2027") {
  await wrapper.find("input").setValue(year)
  await wrapper.find("button").trigger("click")
  await settle()
}

describe("RegisteredParticipants", () => {
  it("asks the security question before loading the list", async () => {
    const wrapper = await mountApp(Participants)
    expect(wrapper.find(".n-card input").exists()).toBe(true)
    expect(wrapper.find("table").exists()).toBe(false)
    expect(requests.map((r) => r.url)).toEqual(["/loaddata"])
  })

  it("loads the list for the given year, by name", async () => {
    const wrapper = await mountApp(Participants)
    await answerQuestion(wrapper, "2027")
    expect(requests.at(-1)).toEqual({ method: "POST", url: "/participants", body: { year: "2027" } })
    expect(wrapper.findAll("tbody tr")).toHaveLength(participants.length)
    expect(wrapper.findAll("tbody td.participant-hidden")).toHaveLength(participants.filter((p) => p.hidden).length)
  })

  it("filters by first letter of the family name", async () => {
    const wrapper = await mountApp(Participants)
    await answerQuestion(wrapper)
    const letterButtons = wrapper.findAll(".buttonsList button")
    // "all" + one button per letter
    expect(letterButtons.length).toBeGreaterThan(2)
    await letterButtons[1].trigger("click")
    const rows = wrapper.findAll("tbody tr").length
    expect(rows).toBeGreaterThan(0)
    expect(rows).toBeLessThan(participants.length)
    await letterButtons[0].trigger("click")
    expect(wrapper.findAll("tbody tr")).toHaveLength(participants.length)
  })

  it("groups by country, unknown countries last", async () => {
    const wrapper = await mountApp(Participants)
    await answerQuestion(wrapper)
    const [, byCountry] = wrapper.findAll(".n-input-group button")
    await byCountry.trigger("click")
    const countries = new Set(participants.map((p) => p.country))
    const cards = wrapper.findAll(".country-card")
    expect(cards).toHaveLength(countries.size)
    expect(wrapper.find("table").exists()).toBe(false)

    // Filter on one country
    await wrapper.findAll(".buttonsList button")[1].trigger("click")
    expect(wrapper.findAll(".country-card")).toHaveLength(1)
  })

  it.each([
    ["the answer is refused", () => ({ success: false })],
    ["the request fails", () => new Error("Network Error")],
  ])("keeps the question and shows a message when %s", async (_, response) => {
    mockApi("POST", "/participants", response)
    const wrapper = await mountApp(Participants)
    await answerQuestion(wrapper)
    expect(wrapper.find(".n-card input").exists()).toBe(true)
    expect(document.querySelector(".n-message")).not.toBeNull()
  })
})
