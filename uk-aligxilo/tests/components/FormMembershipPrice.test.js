// Fee type choice and the price summary of the registration form
import { describe, expect, it } from "vitest"

import FormMembershipPrice from "@/components/form/parts/FormMembershipPrice.vue"
import PriceTypeChoice from "@/components/form/parts/PriceTypeChoice.vue"
import MainForm from "@/components/MainForm.vue"
import Registration from "@/embedded/Registration.vue"
import { mountApp, settle } from "../support/mount.js"

async function mountForm() {
  const app = await mountApp(Registration)
  const form = app.findComponent(MainForm)
  return { form, vm: form.vm }
}

describe("PriceTypeChoice", () => {
  it.each(["kunulo", "akompananto"])("shows the field of the main registrant for %s", async (kotizo) => {
    const { form, vm } = await mountForm()
    vm.form.kotizo = kotizo
    await settle()
    expect(form.findComponent(PriceTypeChoice).find("#cxefaligxinto, #cxefaligxinto input").exists()).toBe(true)
  })

  it("rejects the own name or UEA code as the main registrant", async () => {
    const { form, vm } = await mountForm()
    const choice = () => form.findComponent(PriceTypeChoice).vm
    Object.assign(vm.form, { kotizo: "kunulo", cxefaligxinto: "" })
    await settle()
    expect(choice().cxefaligxintoError).toBeNull()

    Object.assign(vm.form, { uea_kodo: "abcd-e", cxefaligxinto: "abcd-e" })
    await settle()
    expect(choice().cxefaligxintoError).toContain("kunulo")

    Object.assign(vm.form, { uea_kodo: "", persona_nomo: "Ana", familia_nomo: " Bertrand ", cxefaligxinto: "Bertrand" })
    await settle()
    expect(choice().cxefaligxintoError).toContain("kunulo")

    vm.form.cxefaligxinto = "Someone Else"
    await settle()
    expect(choice().cxefaligxintoError).toBeNull()
  })
})

describe("FormMembershipPrice", () => {
  it("lists every part of the price with a title", async () => {
    const { form, vm } = await mountForm()
    Object.assign(vm.form, { kotizo: "baza", donaco_uk: 20 })
    vm.discount = 5
    await settle()
    const rows = form.findComponent(FormMembershipPrice).vm.priceWithLabels
    const sums = rows.map((row) => row.sum)
    expect(sums.at(-1)).toBe(vm.detailedSum.sum)
    expect(sums).toContain(vm.detailedSum.aligxkotizo)
    expect(sums).toContain(-5) // the discount of a former participant
    expect(sums).toContain(20) // the donation
    expect(rows.every((row) => row.title)).toBe(true)
  })

  it("has no price list without a fee type", async () => {
    const { form } = await mountForm()
    expect(form.findComponent(FormMembershipPrice).vm.priceWithLabels).toBeNull()
  })

  it("only lists the donations that were made in edit mode", async () => {
    const { form, vm } = await mountForm()
    vm.$store.dispatch("setEditMode", true)
    vm.form.donaco_uk = 15
    await settle()
    expect(Object.keys(form.findComponent(FormMembershipPrice).vm.filteredFoundations)).toEqual(["uk"])
  })
})
