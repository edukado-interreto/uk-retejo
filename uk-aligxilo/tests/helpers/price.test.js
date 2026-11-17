// Logic only: every amount below is synthetic, real prices live in the backend data
import { describe, expect, it } from "vitest"

import { calculatePrice, isChild, isYouth, isYouthForMembership } from "@/helpers/price.js"

const formOptions = {
  boolValues: { yes: "jes", no: "ne" },
  childBirthDate: "2010-01-01",
  youthBirthDate: "1995-01-01",
  membershipYouthBirthDate: "2000-01-01",
  dayPriceMember: 10,
  dayPriceNonmember: 20,
}
const pricesList = { baza: { price: 100 }, junulo: { price: 50 } }
const prices = { membershipPrice: { 1: { MB: 30, MA: 60, MB50: 15, MB75: 7 } } }

const form = (overrides = {}) => ({
  kotizo: "baza",
  membreco: "ne",
  volas_membrigxi: "ne",
  membreco_tipo: undefined,
  naskigxdato: "1980-05-05",
  partopreno_de: "2027-07-01",
  partopreno_gxis: "2027-07-08",
  donaco_uk: null,
  ...overrides,
})

const price = (f, { discount = 0, showPersonalData = true, memberAgeGroup = null, priceData = prices } = {}) =>
  calculatePrice(f, pricesList, 1, "A", discount, formOptions, priceData, showPersonalData, memberAgeGroup)

describe("age groups", () => {
  it.each([
    ["2012-01-01", false, true],
    ["2005-06-01", true, false],
    ["1999-06-01", true, false],
    ["1990-01-01", false, false],
  ])("born %s: youth %s, child %s", (birthday, youth, child) => {
    expect(isYouth(birthday, true, null, formOptions)).toBe(youth)
    expect(isChild(birthday, true, null, formOptions)).toBe(child)
  })

  it("uses the boundaries inclusively for the start of the range", () => {
    expect(isYouth(formOptions.youthBirthDate, true, null, formOptions)).toBe(true)
    expect(isYouth(formOptions.childBirthDate, true, null, formOptions)).toBe(false)
    expect(isChild(formOptions.childBirthDate, true, null, formOptions)).toBe(true)
  })

  it("has its own youth limit for the membership", () => {
    expect(isYouthForMembership("1997-01-01", true, null, formOptions)).toBe(false)
    expect(isYouthForMembership("2003-01-01", true, null, formOptions)).toBe(true)
  })

  it("without a birthday, answers 'maybe' unless strict", () => {
    for (const fn of [isYouth, isChild, isYouthForMembership]) {
      expect(fn(null, true, null, formOptions)).toBe(true)
      expect(fn(null, true, null, formOptions, true)).toBe(false)
    }
  })

  it("trusts the age group of the UEA database when personal data is hidden", () => {
    expect(isYouth("1950-01-01", false, "youth", formOptions)).toBe(true)
    expect(isYouth("2001-01-01", false, "adult", formOptions)).toBe(false)
    expect(isChild("1950-01-01", false, "child", formOptions)).toBe(true)
    expect(isYouthForMembership("1950-01-01", false, "membershipyouth", formOptions)).toBe(true)
    expect(isYouthForMembership("2003-01-01", false, "youth", formOptions)).toBe(false)
  })
})

describe("calculatePrice", () => {
  it("returns null until a fee type is chosen", () => {
    expect(price(form({ kotizo: null }))).toBeNull()
  })

  it("uses the fee of the chosen type for a full stay", () => {
    expect(price(form())).toEqual({ aligxkotizo: 100, sum: 100 })
  })

  it("charges per day for stays shorter than 3 days", () => {
    const short = { partopreno_de: "2027-07-01", partopreno_gxis: "2027-07-02" }
    expect(price(form(short)).sum).toBe(2 * formOptions.dayPriceNonmember)
    expect(price(form({ ...short, membreco: "jes" })).sum).toBe(2 * formOptions.dayPriceMember)
    expect(price(form({ ...short, volas_membrigxi: "traktata" })).sum).toBe(2 * formOptions.dayPriceMember)
  })

  it("adds the membership fee, reduced for young members", () => {
    const join = { volas_membrigxi: "jes", membreco_tipo: "MB" }
    expect(price(form(join))).toEqual({ aligxkotizo: 100, membrigxo: 30, sum: 130 })
    expect(price(form({ ...join, naskigxdato: "2003-01-01" })).membrigxo).toBe(15)
    expect(price(form({ ...join, naskigxdato: "2012-01-01" })).membrigxo).toBe(7)
    expect(price(form({ ...join, membreco_tipo: "MA", naskigxdato: "2012-01-01" })).membrigxo).toBe(60)
  })

  it("adds donations but ignores empty ones", () => {
    const result = price(form({ donaco_uk: 12.5, donaco_iik: 0, donaco_co2: null }))
    expect(result).toEqual({ aligxkotizo: 100, donaco_uk: 12.5, sum: 112.5 })
  })

  it("subtracts the early discount for the member status and country category", () => {
    const priceData = { ...prices, earlyDiscounts: { baza: [{ A: 5 }, { A: 8 }] } }
    expect(price(form(), { priceData })).toMatchObject({ earlyDiscount: -8, sum: 92 })
    expect(price(form({ membreco: "jes" }), { priceData })).toMatchObject({ earlyDiscount: -5, sum: 95 })
    expect(price(form({ kotizo: "junulo" }), { priceData })).not.toHaveProperty("earlyDiscount")
  })

  it("applies a personal discount only when it is lower than the fee", () => {
    expect(price(form(), { discount: 30 })).toMatchObject({ discount: -30, sum: 70 })
    expect(price(form(), { discount: 100 })).not.toHaveProperty("discount")
  })

  it("rounds to cents and never goes below zero", () => {
    expect(price(form({ donaco_uk: 0.1 + 0.2 })).sum).toBe(100.3)
    const priceData = { ...prices, earlyDiscounts: { baza: [{ A: 500 }, { A: 500 }] } }
    expect(price(form(), { priceData }).sum).toBe(0)
  })
})
