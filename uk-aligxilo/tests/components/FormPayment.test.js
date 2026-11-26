// Choice of the payment method, and the card form for Stripe
import { beforeEach, describe, expect, it } from "vitest"

import StripableFormdict from "@/components/form/fields/StripableFormdict.vue"
import FormPayment from "@/components/form/parts/FormPayment.vue"
import store from "@/store.js"
import { fixtures } from "../support/api.js"
import { mountComponent, settle } from "../support/mount.js"

const { formOptions } = fixtures.loaddata

// A country with a single peranto (local agent who collects payments), and one without any
const [perantoCountry, [peranto]] = Object.entries(formOptions.perantoj).find(([, list]) => list.length === 1)
const plainCountry = Object.keys(fixtures.loaddata.countries).find((code) => !(code in formOptions.perantoj))

beforeEach(async () => {
  await store.dispatch("loaddata")
})

async function mountPayment({ lando = plainCountry, ueaCodeValid = false } = {}) {
  const modelValue = { lando, pagmaniero: null, uea_kodo_paganto: "", karto_retadreso: "", karto_posedanto: "" }
  const { wrapper, state } = await mountComponent(FormPayment, {
    props: { modelValue, ueaCodeValid, isLoading: false, formToSend: {} },
  })
  return { wrapper, form: state.modelValue, state }
}

const options = (wrapper) => wrapper.findAll("#pagmaniero .n-radio")
const optionLabels = (wrapper) => options(wrapper).map((radio) => radio.text())

async function choose(wrapper, label) {
  await options(wrapper)
    .find((radio) => radio.text().startsWith(label))
    .trigger("click")
  await settle()
}

describe("FormPayment", () => {
  it("offers the payment methods of the server when the country has no peranto, Stripe first", async () => {
    const { wrapper } = await mountPayment()
    const values = options(wrapper).map((radio) => radio.find("input").element.value)
    expect(values).toEqual(Object.keys(formOptions.payment))
    expect(options(wrapper)[0].find(".remark").text()).toContain("Ni rekomendas")
  })

  it("adds the peranto of the country, and hides the own UEA account of non-members", async () => {
    const { wrapper } = await mountPayment({ lando: perantoCountry })
    const labels = optionLabels(wrapper)
    expect(labels.some((label) => label.includes(peranto.nomo))).toBe(true)
    expect(labels).not.toContain(formOptions.payment.UEA)
  })

  it("keeps the own UEA account for members, with the peranto before the last two methods", async () => {
    const { wrapper } = await mountPayment({ lando: perantoCountry, ueaCodeValid: true })
    const labels = optionLabels(wrapper)
    expect(labels).toContain(formOptions.payment.UEA)
    expect(labels.at(-3)).toContain(peranto.nomo)
  })

  it("tells that the peranto gets the registration data", async () => {
    const { wrapper, form } = await mountPayment({ lando: perantoCountry })
    expect(wrapper.text()).not.toContain("senditaj ankaŭ al la peranto")
    await choose(wrapper, "Pere de kongresa peranto")
    expect(form.pagmaniero).toBe(`Peranto: ${peranto.uea_kodo}`)
    expect(wrapper.text()).toContain("senditaj ankaŭ al la peranto")
  })

  it("asks for the UEA code of the payer only for another person's account", async () => {
    const { wrapper, form } = await mountPayment()
    expect(wrapper.find("#uea_kodo_paganto").exists()).toBe(false)
    await choose(wrapper, formOptions.payment["UEA-alia"])
    expect(form.pagmaniero).toBe("UEA-alia")
    expect(wrapper.find("#uea_kodo_paganto").exists()).toBe(true)
  })

  it("shows the card form only for Stripe, with the card errors", async () => {
    const { wrapper, form } = await mountPayment()
    const card = () => wrapper.findAll(".n-card").find((c) => c.text().includes("Pagformularo"))
    expect(card().attributes("style")).toContain("display: none")

    await choose(wrapper, formOptions.payment.Stripe)
    expect(form.pagmaniero).toBe("Stripe")
    expect(card().attributes("style") ?? "").not.toContain("display: none")

    const stripe = wrapper.findComponent(StripableFormdict)
    stripe.vm.$emit("card_change", { error: { message: "Nevalida kartnumero" } })
    await settle()
    expect(card().text()).toContain("Nevalida kartnumero")

    stripe.vm.$emit("card_change", { complete: true })
    await settle()
    expect(card().text()).not.toContain("Nevalida kartnumero")
  })

  it("forwards the waiting state of the card payment", async () => {
    const { wrapper, state } = await mountPayment()
    const stripe = wrapper.findComponent(StripableFormdict)
    stripe.vm.$emit("wait_start")
    expect(state.isLoading).toBe(true)
    stripe.vm.$emit("wait_end")
    expect(state.isLoading).toBe(false)
  })

  it("does not let the payment method change when editing a registration", async () => {
    const { wrapper } = await mountPayment()
    expect(wrapper.find("#pagmaniero").exists()).toBe(true)
    store.dispatch("setEditMode", true)
    await settle()
    expect(wrapper.find("#pagmaniero").exists()).toBe(false)
  })
})
