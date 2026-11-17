// Personal data of the registrant: name tag, birth date check, and the view for known members
import { describe, expect, it } from "vitest"

import FormPersonalData from "@/components/form/parts/FormPersonalData.vue"
import MainForm from "@/components/MainForm.vue"
import Registration from "@/embedded/Registration.vue"
import store from "@/store.js"
import { fixtures } from "../support/api.js"
import { expectUndeclaredMembershipCategory } from "../support/known-bugs.js"
import { mountApp, settle } from "../support/mount.js"

async function mountPersonalData() {
  const app = await mountApp(Registration)
  const form = app.findComponent(MainForm)
  return { form, vm: form.vm, personal: form.findComponent(FormPersonalData) }
}

describe("FormPersonalData", () => {
  it("copies the first name to the name tag, or the family name when it is empty", async () => {
    const { vm, personal } = await mountPersonalData()
    Object.assign(vm.form, { persona_nomo: " Ana ", familia_nomo: "Bertrand" })
    personal.vm.updateNametagName()
    expect(vm.form.sxildonomo).toBe("Ana")
    expect(vm.form.karto_posedanto).toBe("Ana")

    Object.assign(vm.form, { persona_nomo: " ", familia_nomo: " Bertrand " })
    personal.vm.updateNametagName()
    expect(vm.form.sxildonomo).toBe("Bertrand")
  })

  it("updates the name tag when typing the names", async () => {
    const { vm, personal } = await mountPersonalData()
    await personal.find("#persona_nomo input, input#persona_nomo").setValue("Cyril")
    expect(vm.form.sxildonomo).toBe("Cyril")
  })

  it("follows the country on the name tag and in the store", async () => {
    const { vm, personal } = await mountPersonalData()
    const [code, { name }] = Object.entries(fixtures.loaddata.countries)[1]
    personal.vm.updateNameTagCountry(code)
    expect(vm.form.sxildolando).toBe(name)
    expect(store.state.userCountry ?? store.getters.userCountry).toBeDefined()
    personal.vm.updateNameTagCountry("not a country")
    expect(vm.form.sxildolando).toBe(name)
  })

  it("asks to check birth dates that look like a baby, and only those", async () => {
    const { personal } = await mountPersonalData()
    personal.vm.checkBirthDate("1990-05-01")
    await settle()
    expect(document.querySelector(".n-dialog")).toBeNull()

    personal.vm.checkBirthDate("2026-05-01")
    await settle()
    expect(document.querySelector(".n-dialog")).not.toBeNull()
  })

  it("shows a short card for a known member, and the form again on request", async () => {
    expectUndeclaredMembershipCategory()
    const { form, vm } = await mountPersonalData()
    vm.ueaCodeValid = true
    vm.showPersonalData = false
    await settle()
    const personal = form.findComponent(FormPersonalData)
    expect(personal.find("input#lando, #lando").exists()).toBe(false)
    expect(personal.find("button").exists()).toBe(true)

    await personal.find("button").trigger("click")
    await settle()
    expect(vm.showPersonalData).toBe(true)
  })

  it("still asks for what UEA does not know about a known member", async () => {
    expectUndeclaredMembershipCategory()
    const { form, vm } = await mountPersonalData()
    vm.ueaCodeValid = true
    vm.showPersonalData = false
    vm.missingFields = ["naskigxdato", "retadreso"]
    await settle()
    const personal = form.findComponent(FormPersonalData)
    expect(personal.findAll(".n-form-item").length).toBe(2)
  })

  it("only asks for the missing field when one is missing", async () => {
    expectUndeclaredMembershipCategory()
    const { form, vm } = await mountPersonalData()
    vm.ueaCodeValid = true
    vm.showPersonalData = false
    vm.missingFields = ["naskigxdato"]
    await settle()
    expect(form.findComponent(FormPersonalData).findAll(".n-form-item").length).toBe(1)
  })
})
