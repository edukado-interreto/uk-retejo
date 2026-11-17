// Behaviour of the registration form, checked through structure and state, never copy
import { describe, expect, it } from "vitest"

import FormBooking from "@/components/form/parts/FormBooking.vue"
import FormPayment from "@/components/form/parts/FormPayment.vue"
import FormPersonalData from "@/components/form/parts/FormPersonalData.vue"
import MainForm from "@/components/MainForm.vue"
import StripableFormdict from "@/components/form/fields/StripableFormdict.vue"
import Registration from "@/embedded/Registration.vue"
import { fixtures, mockApi, requests } from "../support/api.js"
import { mountApp, settle } from "../support/mount.js"

async function mountForm(options) {
  const app = await mountApp(Registration, options)
  const form = app.findComponent(MainForm)
  return { app, form, vm: form.vm }
}

describe("MainForm (registration)", () => {
  it("prefills the detected country and the congress dates", async () => {
    const { vm } = await mountForm()
    const { detectedCountry, formOptions } = fixtures.loaddata
    expect(vm.form.lando).toBe(detectedCountry)
    expect(vm.form.partopreno_de).toBe(formOptions.congressStart)
    expect(vm.form.partopreno_gxis).toBe(formOptions.congressEnd)
    expect(vm.form.sxildolando).toBeTruthy()
  })

  it("has no booking part and no payment block before a fee type is chosen", async () => {
    const { form, vm } = await mountForm()
    expect(vm.sum).toBeNull()
    expect(form.findComponent(FormBooking).exists()).toBe(false)
    expect(form.findComponent(FormPayment).exists()).toBe(false)
    expect(form.find("#errorAlert").exists()).toBe(false)
  })

  it("computes a price and renders for every fee type", async () => {
    const { form, vm } = await mountForm()
    for (const kotizo of Object.keys(fixtures.loaddata.prices.participation)) {
      vm.form.kotizo = kotizo
      await settle()
      expect(vm.detailedSum.sum, kotizo).toBeTypeOf("number")
      expect(vm.detailedSum.sum, kotizo).toBeGreaterThanOrEqual(0)
      expect(form.find("table.price").exists(), kotizo).toBe(true)
    }
  })

  // Known bug: MainForm passes the store `prices` to calculatePrice, which reads
  // `prices.membershipPrice`, but that table is sent as `formOptions.membershipPrice`.
  // Replace `it.fails` by `it` once fixed.
  it.fails("adds the membership fee for a non member who wants to join", async () => {
    const errors = []
    const { form, vm } = await mountForm({ global: { config: { errorHandler: (e) => errors.push(e) } } })
    const { yes, no } = fixtures.loaddata.formOptions.boolValues
    Object.assign(vm.form, { kotizo: "baza", membreco: no, volas_membrigxi: yes, membreco_tipo: "MB" })
    await settle()
    expect(errors).toEqual([])
    expect(vm.detailedSum.membrigxo).toBeGreaterThan(0)
    expect(form.find("table.price").exists()).toBe(true)
  })

  it("shows the payment methods and the price table once a fee type is chosen", async () => {
    const { form, vm } = await mountForm()
    vm.form.kotizo = "baza"
    await settle()
    expect(vm.sum).toBeGreaterThan(0)
    const payment = form.findComponent(FormPayment)
    expect(payment.exists()).toBe(true)
    const methods = payment.findAll("input[type=radio]")
    expect(methods.length).toBeGreaterThanOrEqual(Object.keys(fixtures.loaddata.formOptions.payment).length - 1)
    expect(form.find("table.price").exists()).toBe(true)
  })

  it("loads Stripe and mounts the card element when paying by card", async () => {
    const { form, vm } = await mountForm()
    vm.form.kotizo = "baza"
    vm.form.pagmaniero = "Stripe"
    await settle()
    const stripable = form.findComponent(StripableFormdict)
    expect(stripable.vm.stripe).toBeDefined()
    expect(stripable.find("#card_element").exists()).toBe(true)
  })

  it("hides the personal data once a valid UEA code is entered", async () => {
    mockApi("POST", "/checkcode", {
      valid: true,
      member: {
        missingFields: [],
        isRegistered: false,
        isMember: true,
        countryCategory: "A",
        countryMembershipCategory: 1,
        ageGroup: null,
        specialCategory: null,
        discount: 0,
        maxPeriod: 10,
      },
    })
    const { form, vm } = await mountForm()
    expect(form.findComponent(FormPersonalData).find(".n-card").exists()).toBe(true)

    await form.find("input#uea_kodo, #uea_kodo input").setValue("abcd-e")
    await settle()

    expect(requests.at(-1)).toEqual({ method: "POST", url: "/checkcode", body: { code: "abcd-e" } })
    expect(vm.ueaCodeValid).toBe(true)
    expect(vm.showPersonalData).toBe(false)
    expect(vm.membershipLocked).toBe(true)
    expect(vm.form.membreco).toBe(fixtures.loaddata.formOptions.boolValues.yes)
    expect(form.find(".n-form-item-blank--success #uea_kodo").exists()).toBe(true)
  })

  it("marks the form invalid and does not send it when required fields are empty", async () => {
    const { form, vm } = await mountForm()
    await form.find("button.n-button--primary-type").trigger("click")
    await settle()
    expect(Object.keys(vm.errors.value).length).toBeGreaterThan(0)
    expect(form.find("#errorAlert").exists()).toBe(true)
    expect(form.findAll(".n-form-item-feedback--error").length).toBeGreaterThan(0)
    expect(requests.map((r) => r.url)).toEqual(["/loaddata"])
    expect(document.querySelector(".n-message-container")).not.toBeNull()
  })
  // Known bug: the button of the success message calls `$router.go()`, but the embedded
  // apps have no vue-router. Replace `it.fails` by `it` once fixed.
  it.fails("success message button works", async () => {
    const errors = []
    const { form, vm } = await mountForm({ global: { config: { errorHandler: (e) => errors.push(e) } } })
    vm.success = true
    await settle()
    expect(form.find("#successAlert").exists()).toBe(true)
    expect(form.find("form").exists()).toBe(false)
    await form.find("#successAlert button").trigger("click")
    expect(errors).toEqual([])
  })
})
