// Booking part of the edit form: every hotel, trip and room of the fixture must render
import { describe, expect, it, vi } from "vitest"

import FormBooking from "@/components/form/parts/FormBooking.vue"
import FormHotels from "@/components/form/parts/booking/FormHotels.vue"
import FormBookingPrice from "@/components/form/parts/booking/FormBookingPrice.vue"
import FormPassport from "@/components/form/parts/booking/FormPassport.vue"
import MainForm from "@/components/MainForm.vue"
import Edit from "@/embedded/Edit.vue"
import { fixtures } from "../support/api.js"
import { expectBookingWarnings } from "../support/known-bugs.js"
import { mountApp, settle } from "../support/mount.js"

async function mountEdit(options) {
  expectBookingWarnings()
  window.history.replaceState({}, "", "/mendilo/y2eig1xo0ib6ws50ya694o205dtv869o6")
  const app = await mountApp(Edit, options)
  const form = app.findComponent(MainForm)
  await vi.waitFor(() => expect(form.findComponent(FormBooking).exists()).toBe(true))
  await settle()
  return { app, form }
}

// Skipped while FormBooking.vue is limited to the invitation letter: hotels, trips and
// banquet are kept aside in FormBookingCopy.vue. Restore with `describe` once they are back.
describe.skip("booking", () => {
  const { formOptions } = fixtures.loaddata
  const priceRows = (form) => form.findComponent(FormBookingPrice).findAll("tr").length

  async function mountBooking() {
    const errors = []
    const { form } = await mountEdit({ global: { config: { errorHandler: (e) => errors.push(e) } } })
    return { form, vm: form.vm, errors }
  }

  it("renders every hotel and room", async () => {
    const { form, vm, errors } = await mountBooking()
    const before = priceRows(form)
    for (const [hotel, { rooms }] of Object.entries(formOptions.hotels)) {
      for (const room of Object.keys(rooms ?? {})) {
        Object.assign(vm.form, { hotelo: hotel, hotelo_cxambro: room })
        await settle()
        expect(errors, `${hotel}/${room}`).toEqual([])
        expect(form.findComponent(FormPassport).exists(), hotel).toBe(true)
      }
    }
    expect(priceRows(form)).toBeGreaterThan(before)
  })

  it.each(["ak", "pk"])("renders every %s trip and room", async (type) => {
    const { form, vm, errors } = await mountBooking()
    const trips = Object.values(formOptions.preposttrips).filter((t) => t.type === type)
    for (const trip of trips) {
      for (const room of Object.keys(trip.rooms)) {
        Object.assign(vm.form, { [type]: trip.id, [`${type}_cxambro`]: room })
        await settle()
        expect(errors, `${trip.id}/${room}`).toEqual([])
        expect(vm.foodTypeRequired || Object.keys(trip.rooms).length <= 1 || type === "pk").toBe(true)
      }
    }
    expect(form.findAll(".n-select").length).toBeGreaterThan(0)
  })

  it("renders every banquet option and excursion", async () => {
    const { form, vm, errors } = await mountBooking()
    const before = priceRows(form)
    for (const banquet of Object.keys(formOptions.banquet)) {
      vm.form.bankedo = banquet
      await settle()
      expect(errors, banquet).toEqual([])
    }
    vm.form.ekskursoj = formOptions.trips.map((t) => t.sessions[0].id)
    await settle()
    expect(errors).toEqual([])
    expect(vm.foodTypeRequired).toBe(true)
    expect(priceRows(form)).toBeGreaterThan(before)
  })

  it("forgets the room when the hotel changes to one without it, and keeps a valid one", async () => {
    const { form, vm } = await mountBooking()
    const hotels = form.findComponent(FormHotels)
    // Two hotels where the first has a room the second one does not
    const entries = Object.entries(formOptions.hotels)
    const [first, second] = entries.flatMap((a) => entries.map((b) => [a, b])).find(
      ([a, b]) => Object.keys(a[1].rooms).some((r) => !(r in b[1].rooms)),
    )
    const room = Object.keys(first[1].rooms).find((r) => !(r in second[1].rooms))

    vm.form.hotelo = first[0]
    vm.form.hotelo_cxambro = room
    hotels.vm.hotelChange(first[0])
    expect(vm.form.hotelo_cxambro).toBe(room)

    hotels.vm.hotelChange(second[0])
    expect(vm.form.hotelo_cxambro).toBeNull()
    hotels.vm.hotelChange("no such hotel")
    expect(vm.form.parkloko).toBe(false)
  })

  it("starts the stay on the days of the congress, and limits the dates by the minimum nights", async () => {
    const { form, vm } = await mountBooking()
    const hotels = form.findComponent(FormHotels)
    vm.form.hotelo = Object.keys(formOptions.hotels)[0]
    await settle()
    expect(hotels.vm.minEnd > vm.form.hotelo_de).toBe(true)
    expect(hotels.vm.maxStart < vm.form.hotelo_gxis).toBe(true)
    vm.form.hotelo_de = vm.form.hotelo_gxis = ""
    await settle()
    expect(hotels.vm.minEnd).toBeDefined()
    expect(hotels.vm.maxStart).toBeDefined()
  })

  it("remembers the entered UEA code of the room mate", async () => {
    const { form } = await mountBooking()
    const hotels = form.findComponent(FormHotels)
    hotels.vm.ueaCodeResult({ valid: true })
    expect(hotels.vm.codeValid).toBe(true)
    hotels.vm.ueaCodeResult({ valid: false })
    expect(hotels.vm.codeValid).toBe(false)
  })
})
