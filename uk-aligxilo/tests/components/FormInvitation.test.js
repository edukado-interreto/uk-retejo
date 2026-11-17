// Invitation letter for the visa, part of the booking form
import { describe, expect, it, vi } from "vitest"

import FormBooking from "@/components/form/parts/FormBooking.vue"
import FormInvitation from "@/components/form/parts/booking/FormInvitation.vue"
import MainForm from "@/components/MainForm.vue"
import Edit from "@/embedded/Edit.vue"
import { mockApi, requests } from "../support/api.js"
import { expectBookingWarnings, expectInvitationDisabledProp } from "../support/known-bugs.js"
import { mountApp, settle } from "../support/mount.js"

const download = vi.hoisted(() => vi.fn())
vi.mock("downloadjs", () => ({ default: download }))

async function mountInvitation(options, { open = false } = {}) {
  expectBookingWarnings()
  window.history.replaceState({}, "", "/mendilo/y2eig1xo0ib6ws50ya694o205dtv869o6")
  const app = await mountApp(Edit, options)
  const form = app.findComponent(MainForm)
  await vi.waitFor(() => expect(form.findComponent(FormBooking).exists()).toBe(true))
  await settle()
  const invitation = form.findComponent(FormInvitation)
  if (open) {
    expectInvitationDisabledProp()
    await invitation.find("#invitationNeeded").trigger("click")
    await settle()
  }
  return { form, invitation, vm: invitation.vm }
}

describe("FormInvitation", () => {
  it("shows the invitation data only when an invitation is needed", async () => {
    expectInvitationDisabledProp()
    const { invitation } = await mountInvitation()
    expect(invitation.find("#invitationName").exists()).toBe(false)
    await invitation.find("#invitationNeeded").trigger("click")
    await settle()
    expect(invitation.find("#invitationName").exists()).toBe(true)
    expect(invitation.findAll(".n-date-picker").length).toBe(3)
  })

  it("starts with the data already known of the registrant", async () => {
    const { vm, form } = await mountInvitation()
    expect(vm.defaultName).toBe(`${form.vm.form.persona_nomo} ${form.vm.form.familia_nomo}`.trim())
    expect(vm.birthDate).toBe(form.vm.form.naskigxdato)
    expect(form.vm.form.sxtataneco).toBe(form.vm.form.lando)
  })

  it("cannot download before the passport data is complete", async () => {
    const { invitation, vm } = await mountInvitation({}, { open: true })
    const button = () => invitation.find("button.n-button--info-type")
    expect(vm.canSubmit).toBeFalsy()
    expect(button().attributes("disabled")).toBeDefined()

    Object.assign(vm.form, { pasporto: "AB123456" })
    Object.assign(vm, { passportValidFrom: "2024-01-01", passportValidTo: "2034-01-01" })
    await settle()
    expect(vm.canSubmit).toBeTruthy()
    expect(button().attributes("disabled")).toBeUndefined()
  })

  it("downloads the invitation as a PDF named after the registrant", async () => {
    mockApi("POST", "/invitation", "%PDF")
    const { vm } = await mountInvitation({ global: { mocks: { $route: { params: { id: "abc" } } } } }, { open: true })
    Object.assign(vm.form, { pasporto: "AB123456" })
    Object.assign(vm, { passportValidFrom: "2024-01-01", passportValidTo: "2034-01-01" })

    await vm.download()
    await settle()
    expect(requests.at(-1)).toMatchObject({
      method: "POST",
      url: "/invitation",
      body: { id: "abc", passportNumber: "AB123456", passportValidFrom: "2024-01-01", country: vm.form.sxtataneco },
    })
    expect(download).toHaveBeenCalledWith("%PDF", `Invitletero ${vm.defaultName}.pdf`)
    expect(vm.loading).toBe(false)
  })

  // Known bug: download() reads `this.$route.params.id`, but the embedded apps have no
  // vue-router. Replace `it.fails` by `it` once fixed.
  it.fails("downloads in the embedded app, which has no router", async () => {
    mockApi("POST", "/invitation", "%PDF")
    const { vm } = await mountInvitation()
    await vm.download()
    expect(download).toHaveBeenCalled()
  })
})
