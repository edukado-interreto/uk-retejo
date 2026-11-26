// Consents and conditions of registration, at the end of the form
import { beforeEach, describe, expect, it } from "vitest"

import FormConditions from "@/components/form/parts/FormConditions.vue"
import store from "@/store.js"
import { mountComponent, settle } from "../support/mount.js"

beforeEach(async () => {
  await store.dispatch("loaddata")
})

const emptyForm = () => ({
  kompreno_pago: false,
  konsento_aligxlisto: false,
  konsento_kongreslibro: false,
  kongreslibro_adreso: [],
  konfirmilo: null,
  fotado: null,
  akcepto_reguloj: false,
})

async function mountConditions() {
  const { wrapper, state } = await mountComponent(FormConditions, { props: { modelValue: emptyForm() } })
  return { wrapper, form: state.modelValue }
}

async function click(wrapper, selector) {
  await wrapper.find(selector).trigger("click")
  await settle()
}

describe("FormConditions", () => {
  it("writes each consent into the form", async () => {
    const { wrapper, form } = await mountConditions()
    for (const field of ["kompreno_pago", "konsento_aligxlisto", "akcepto_reguloj"]) {
      await click(wrapper, `#${field}`)
      expect(form[field], field).toBe(true)
    }
  })

  it("asks for the congress book address only after the consent", async () => {
    const { wrapper, form } = await mountConditions()
    expect(wrapper.find("#kongreslibro_adreso").exists()).toBe(false)

    await click(wrapper, "#konsento_kongreslibro")
    expect(form.konsento_kongreslibro).toBe(true)
    expect(wrapper.find("#kongreslibro_adreso").exists()).toBe(true)

    await click(wrapper, "#kongreslibro_adreso .n-checkbox")
    expect(form.kongreslibro_adreso).toEqual(["posxtadreso"])
  })

  it("records the choice about being photographed", async () => {
    const { wrapper, form } = await mountConditions()
    const refuse = wrapper.findAll("#fotado .n-radio").find((radio) => radio.text().startsWith("Ne,"))
    await refuse.trigger("click")
    await settle()
    expect(form.fotado).toBe("ne")
  })

  it("shows the conditions of registration, but not when editing a registration", async () => {
    const conditions = (wrapper) => wrapper.findAll(".n-card").some((card) => card.text().includes("ne estas repagebla"))

    const { wrapper } = await mountConditions()
    expect(conditions(wrapper)).toBe(true)

    store.dispatch("setEditMode", true)
    await settle()
    expect(conditions(wrapper)).toBe(false)
  })
})
