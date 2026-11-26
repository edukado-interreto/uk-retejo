// Edit mode of the registration form (embedded/Edit.vue), with the booking part
import { describe, expect, it, vi } from "vitest"

import FormBooking from "@/components/form/parts/FormBooking.vue"
import FormPayment from "@/components/form/parts/FormPayment.vue"
import MainForm from "@/components/MainForm.vue"
import Edit from "@/embedded/Edit.vue"
import { fixtures, requests } from "../support/api.js"
import { mountApp, settle } from "../support/mount.js"

describe("MainForm (edit mode)", () => {
  async function mountEdit(options) {
    window.history.replaceState({}, "", "/mendilo/y2eig1xo0ib6ws50ya694o205dtv869o6")
    const app = await mountApp(Edit, options)
    const form = app.findComponent(MainForm)
    // FormBooking is an async component
    await vi.waitFor(() => expect(form.findComponent(FormBooking).exists()).toBe(true))
    await settle()
    return { app, form }
  }

  it("loads the registration of the URL and shows the booking part", async () => {
    const { form } = await mountEdit()
    expect(requests).toContainEqual({
      method: "POST",
      url: "/getRegistration",
      body: { id: "y2eig1xo0ib6ws50ya694o205dtv869o6" },
    })
    expect(form.props("edit")).toBe(true)
    expect(form.vm.form.persona_nomo).toBe(fixtures.registration.registration.persona_nomo)
    expect(form.findComponent(FormBooking).find("#invitationNeeded").exists()).toBe(true)
    expect(form.findComponent(FormPayment).isVisible()).toBe(false)
  })

  it("works on a copy: the loaded data is not modified by the form", async () => {
    const { form } = await mountEdit()
    form.vm.form.komento = "changed"
    expect(form.props("defaultData").komento).toBe(fixtures.registration.registration.komento)
  })

  // Known bug, see MainForm.registration.test.js
  it.fails("success message button works", async () => {
    const errors = []
    const { form } = await mountEdit({ global: { config: { errorHandler: (e) => errors.push(e) } } })
    form.vm.success = true
    await settle()
    expect(form.find("#successAlert").exists()).toBe(true)
    await form.find("#successAlert button").trigger("click")
    expect(errors).toEqual([])
  })
})
