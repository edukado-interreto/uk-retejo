import { describe, expect, it } from "vitest"

import { dayOfWeekEO, daysBetweenDates, formatDateString, formatTime, numberOfDays } from "@/helpers/time.js"

describe("time helpers", () => {
  it("counts days between two dates in both directions", () => {
    expect(daysBetweenDates("2027-07-01", "2027-07-08")).toBe(7)
    expect(daysBetweenDates("2027-07-08", "2027-07-01")).toBe(7)
    expect(daysBetweenDates("2027-02-27", "2027-03-01")).toBe(2)
    expect(daysBetweenDates(null, "2027-07-01")).toBe(0)
  })

  it("counts both the first and the last day of a stay", () => {
    expect(numberOfDays("2027-07-01", "2027-07-01")).toBe(1)
    expect(numberOfDays("2027-07-01", "2027-07-08")).toBe(8)
    expect(numberOfDays(null, "2027-07-08")).toBe(0)
  })

  it("formats a date with the day number and the year only on demand", () => {
    const short = formatDateString("2027-07-05")
    expect(short).toMatch(/^5-a /)
    expect(formatDateString("2027-07-05", true)).toMatch(/^5-an /)
    expect(formatDateString("2027-07-05", false, true)).toBe(`${short} 2027`)
  })

  it("gives a different name to each day of the week", () => {
    const week = ["2027-07-04", "2027-07-05", "2027-07-06", "2027-07-07", "2027-07-08", "2027-07-09", "2027-07-10"]
    const names = week.map((d) => dayOfWeekEO(d))
    expect(new Set(names).size).toBe(7)
    expect(dayOfWeekEO("2027-07-11")).toBe(names[0])
    const capitalized = dayOfWeekEO("2027-07-05", true)
    expect(capitalized.toLowerCase()).toBe(names[1])
    expect(capitalized[0]).toBe(capitalized[0].toUpperCase())
  })

  it("formats a time as HH:MM on 24 hours", () => {
    expect(formatTime(new Date(2027, 6, 5, 9, 5))).toMatch(/^0?9:05$/)
    expect(formatTime(new Date(2027, 6, 5, 21, 30))).toBe("21:30")
  })
})
