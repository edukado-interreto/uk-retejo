// Sending the registration form: direct signup, card payment, and every kind of error
import { describe, expect, it, vi } from "vitest"

import MainForm from "@/components/MainForm.vue"
import Registration from "@/embedded/Registration.vue"
import { fixtures, mockApi } from "../support/api.js"
import { expectConsole } from "../support/console.js"
import { mountApp, settle } from "../support/mount.js"

async function mountForm() {
  vi.spyOn(console, "log").mockImplementation(() => {}) // signup() logs the server responses
  const app = await mountApp(Registration)
  const form = app.findComponent(MainForm)
  // A fee type makes the payment block (and its signup methods) available
  form.vm.form.kotizo = "baza"
  await settle()
  return { form, vm: form.vm }
}

/** Answer the calls of StripableFormdict, which uses fetch: one response per call, in order. */
function mockServer(...responses) {
  const calls = []
  vi.stubGlobal("fetch", async (url, init) => {
    const body = JSON.parse(init.body)
    calls.push(body.op)
    const response = typeof responses[0] === "function" ? responses[0](body) : responses[calls.length - 1]
    return { text: async () => JSON.stringify(response), json: async () => response }
  })
  return calls
}

const serverError = (messages) => ({ error_code: "ERR", error_msg: JSON.stringify(messages) })
const submitEvent = () => ({ preventDefault: vi.fn() })

describe("MainForm: sending", () => {
  it("signs up and shows the success state", async () => {
    const { form, vm } = await mountForm()
    const calls = mockServer({ success: true })
    await vm.signup()
    await settle()
    expect(calls).toEqual(["direct-process"])
    expect(vm.success).toBe(true)
    expect(form.find("#successAlert").exists()).toBe(true)
  })

  it("pays by card: pre-payment, Stripe, post-payment", async () => {
    const { vm } = await mountForm()
    vm.form.pagmaniero = "Stripe"
    await settle()
    const calls = mockServer({ client_secret: "secret" }, { success: true })
    await vm.signup(true)
    expect(calls).toEqual(["pre-payment", "post-payment"])
    expect(vm.success).toBe(true)
  })

  it("keeps the form open when the server does not confirm", async () => {
    const { vm } = await mountForm()
    mockServer({ success: false })
    await vm.signup()
    expect(vm.success).toBe(false)
  })

  it("shows the validation errors of the server under the fields", async () => {
    const { form, vm } = await mountForm()
    mockServer(serverError({ lando: "Eraro de la servilo" }))
    await vm.signup()
    await settle()
    expect(vm.errors.value).toEqual({ lando: "Eraro de la servilo" })
    expect(form.find("#errorAlert").exists()).toBe(true)
    expect(vm.canSubmit).toBe(true)
  })

  it("blocks a second attempt and shows a dialog on an unknown error", async () => {
    // showErrorMessage() gives plain strings as the content of <n-button>
    expectConsole(/Non-function value encountered for default slot/, "MainForm.vue showErrorMessage")
    const { vm } = await mountForm()
    mockServer({ error_code: "ERR", error_msg: "not json" })
    await vm.signup()
    await settle()
    expect(vm.canSubmit).toBe(false)
    expect(document.querySelector(".n-dialog")).not.toBeNull()
  })

  it("copies the error message of the dialog, and closes it", async () => {
    expectConsole(/Non-function value encountered for default slot/, "MainForm.vue showErrorMessage")
    const writeText = vi.fn()
    vi.stubGlobal("navigator", { ...navigator, clipboard: { writeText } })
    const { vm } = await mountForm()
    vm.showErrorMessage("boom")
    await settle()
    const [copy, close] = document.querySelectorAll(".n-dialog .n-button")
    copy.click()
    expect(writeText).toHaveBeenCalledWith("boom")
    close.click()
    await settle()
    expect(vm.dialog.destroyAll).toBeDefined()
  })

  it("renders the error message as an alert", async () => {
    const { vm } = await mountForm()
    const props = { type: "error", closable: true, onClose: () => {}, content: "Eraro" }
    expect(vm.renderErrorMessage(props).props).toMatchObject({ type: "error", closable: true })
    expect(vm.renderErrorMessage({ ...props, type: "loading" }).props.type).toBe("default")
  })

  it("signs up when the validation passes", async () => {
    const { vm } = await mountForm()
    vm.$refs.formRef.validate = async (callback) => callback(undefined)
    const calls = mockServer({ success: true })
    vm.sendForm(submitEvent())
    await settle()
    expect(calls).toEqual(["direct-process"])
  })

  it("pays by card when the validation passes and Stripe is chosen", async () => {
    const { vm } = await mountForm()
    vm.form.pagmaniero = "Stripe"
    await settle()
    vm.$refs.formRef.validate = async (callback) => callback(undefined)
    const calls = mockServer({ client_secret: "secret" }, { success: true })
    vm.sendForm(submitEvent())
    await settle()
    expect(calls).toEqual(["pre-payment", "post-payment"])
  })

  it("does not send the form on submit, only through the button", async () => {
    const { vm } = await mountForm()
    const event = submitEvent()
    vm.submitForm(event)
    expect(event.preventDefault).toHaveBeenCalled()
  })
})

describe("MainForm: UEA code and name tag", () => {
  const member = (changes = {}) => ({
    valid: true,
    member: {
      missingFields: [],
      isRegistered: false,
      isMember: false,
      countryCategory: "B",
      countryMembershipCategory: 2,
      ageGroup: "adult",
      specialCategory: null,
      discount: 5,
      maxPeriod: 3,
      ...changes,
    },
  })
  const { boolValues } = fixtures.loaddata.formOptions

  it("keeps what UEA knows about a member", async () => {
    const { vm } = await mountForm()
    vm.ueaCodeResult(member())
    expect(vm.membershipLocked).toBe(true)
    expect(vm.form.membreco).toBe(boolValues.no)
    expect(vm.discount).toBe(5)
    expect(vm.countryCategoryFromDB).toBe("B")
    expect(vm.maxPeriod).toBe(3)
    expect(vm.showPersonalData).toBe(false)
  })

  it("asks for the personal data again when the e-mail address is unknown", async () => {
    const { vm } = await mountForm()
    vm.ueaCodeResult(member({ missingFields: ["retadreso"] }))
    expect(vm.showPersonalData).toBe(true)
    expect(vm.missingFields).toEqual(["retadreso"])
  })

  it("warns a member who is already registered", async () => {
    const { vm } = await mountForm()
    vm.ueaCodeResult(member({ isRegistered: true }))
    await settle()
    expect(document.querySelector(".n-dialog")).not.toBeNull()
  })

  it("selects the special fee category of the member", async () => {
    const { vm } = await mountForm()
    const special = Object.keys(fixtures.loaddata.prices.participation).find((kotizo) => kotizo !== "baza")
    vm.ueaCodeResult(member({ specialCategory: special }))
    expect(vm.form.kotizo).toBe(special)
  })

  it("forgets everything when the code is not valid", async () => {
    const { vm } = await mountForm()
    vm.ueaCodeResult(member())
    vm.ueaCodeResult({ valid: false })
    expect(vm.membershipLocked).toBe(false)
    expect(vm.showPersonalData).toBe(true)
    expect(vm.missingFields).toEqual([])
    expect(vm.discount).toBe(0)
    expect(vm.maxPeriod).toBe(10)
  })

  it("puts the country name on the name tag", async () => {
    const { vm } = await mountForm()
    const [code, { name }] = Object.entries(fixtures.loaddata.countries)[0]
    vm.updateNameTagCountry(code)
    expect(vm.form.sxildolando).toBe(name)
    vm.updateNameTagCountry("not a country")
    expect(vm.form.sxildolando).toBe(name)
  })
})
