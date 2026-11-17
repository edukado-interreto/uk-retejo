import { describe, expect, it, vi } from "vitest"

import KotizojPage from "@/components/kotizoj/KotizojPage.vue"
import PeriodCards from "@/components/kotizoj/PeriodCards.vue"
import PersonaBox from "@/components/kotizoj/PersonaBox.vue"
import PriceTable from "@/components/kotizoj/PriceTable.vue"
import { normalize, useKotizoj } from "@/components/kotizoj/useKotizoj.js"
import Price from "@/embedded/Price.vue"
import { fixtures } from "../support/api.js"
import { mountApp } from "../support/mount.js"

const { countries, detectedCountry, registrationPeriods } = fixtures.loaddata

function mockScreen({ mobile }) {
  vi.spyOn(window, "matchMedia").mockImplementation((query) => ({
    matches: mobile,
    media: query,
    addEventListener: () => {},
    removeEventListener: () => {},
  }))
}

describe("Price page", () => {
  it("shows the price table on large screens", async () => {
    mockScreen({ mobile: false })
    const wrapper = await mountApp(Price)
    expect(wrapper.findComponent(PriceTable).exists()).toBe(true)
    expect(wrapper.findComponent(PeriodCards).exists()).toBe(false)
  })

  it("shows period cards on small screens", async () => {
    mockScreen({ mobile: true })
    const wrapper = await mountApp(Price)
    expect(wrapper.findComponent(PeriodCards).exists()).toBe(true)
    expect(wrapper.findComponent(PriceTable).exists()).toBe(false)
  })

  it("passes one period per registration deadline, plus the last open one", async () => {
    const wrapper = await mountApp(Price)
    const page = wrapper.findComponent(KotizojPage)
    expect(page.props("data").periodoj).toHaveLength(registrationPeriods.length + 1)
    expect(page.props("detectedCountry")).toBe(countries[detectedCountry].name)
  })

  it("follows the country chosen in the persona box", async () => {
    const wrapper = await mountApp(Price)
    const table = () => wrapper.findComponent(PriceTable)
    expect(table().props("category")).toBe(countries[detectedCountry].category)

    for (const category of ["A", "B"]) {
      const country = Object.values(countries).find((c) => c.category === category)
      wrapper.findComponent(PersonaBox).vm.$emit("update:country", country.name)
      await wrapper.vm.$nextTick()
      expect(table().props("category")).toBe(category)
    }
  })
})

describe("useKotizoj", () => {
  const data = {
    periodoj: [
      { numero: 1, gxis: "2026-11-30" },
      { numero: 2, gxis: "2027-03-31" },
      { numero: 3, gxis: null },
    ],
    landoj_A: ["Francio"],
    landoj_B: ["Brazilo"],
    flagoj: { Francio: "F" },
    junulo: { de: "1996-01-01", gxis: "2005-12-31" },
    senpage_post: "2005-12-31",
    prezoj: { A: { membro: [1, 2, 3] } },
  }
  const use = (period, country = null) =>
    useKotizoj(
      () => data,
      () => period,
      { value: country },
    )

  it("starts each period the day after the previous deadline", () => {
    const { periods } = use(0)
    expect(periods.value.map((p) => p.gxis)).toEqual(["2026-11-30", "2027-03-31", null])
    expect(periods.value[2].label).toContain("1")
  })

  it("clamps the current period", () => {
    expect(use(-3).nowIndex.value).toBe(0)
    expect(use(1).nowIndex.value).toBe(1)
    expect(use(99).nowIndex.value).toBe(2)
    expect(use(null).nowIndex.value).toBe(2)
  })

  it("finds the country category", () => {
    expect(use(0, "Francio").category.value).toBe("A")
    expect(use(0, "Brazilo").category.value).toBe("B")
    expect(use(0, "Nenie").category.value).toBeNull()
    expect(use(0).category.value).toBeNull()
  })

  it("lists countries sorted, with their flag when known", () => {
    expect(use(0).countryOptions.value.map((o) => o.value)).toEqual(["Brazilo", "Francio"])
    expect(use(0).countryOptions.value[1].label).toContain("F")
  })

  it("reads prices, free rows cost nothing", () => {
    const { price } = use(0)
    expect(price("A", "membro", 2)).toBe(3)
    expect(price("A", "free", 2)).toBe(0)
  })

  it("normalizes search terms (x-system and diacritics)", () => {
    expect(normalize("Ĉinio")).toBe("cinio")
    expect(normalize("cxinio")).toBe("cinio")
    expect(normalize("ŜVEDIO")).toBe(normalize("sxvedio"))
  })
})
