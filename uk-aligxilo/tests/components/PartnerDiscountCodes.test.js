// Discount codes of the partners, shown in the booking form
import { describe, expect, it } from "vitest"

import PartnerDiscountCodes from "@/components/form/parts/booking/PartnerDiscountCodes.vue"
import { mountComponent, settle } from "../support/mount.js"

describe("PartnerDiscountCodes", () => {
  const copyButtons = (wrapper) => wrapper.findAll("button[aria-label^='Kopii la']")

  it("links to the Alvenebloj page, never directly to Qantas", async () => {
    const { wrapper } = await mountComponent(PartnerDiscountCodes)
    const link = wrapper.find("a.alvenebloj-link")
    expect(link.attributes("href")).toMatch(/\/alvenebloj$/)
    expect(wrapper.find("a[href*='qantas']").exists()).toBe(false)
  })

  it("copies the code of the clicked partner and marks only that one as copied", async () => {
    const { wrapper } = await mountComponent(PartnerDiscountCodes)

    const [qantas, skybus] = copyButtons(wrapper)
    expect(qantas.text()).toBe("Kopii")
    expect(skybus.text()).toBe("Kopii")

    await skybus.trigger("click")
    await settle()

    // happy-dom implements the Clipboard API used by useClipboard
    expect(await navigator.clipboard.readText()).toBe("WCUEA27")
    const [qantasAfter, skybusAfter] = copyButtons(wrapper)
    expect(skybusAfter.text()).toBe("Kopiita")
    expect(qantasAfter.text()).toBe("Kopii")
  })
})
