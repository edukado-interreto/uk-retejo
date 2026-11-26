import { describe, expect, it, vi } from "vitest"
import { nextTick } from "vue"

import { flagEmoji, registrationIdFromUrl, scrollTo } from "@/helpers/functions.js"
import mixins from "@/mixins.js"

describe("registrationIdFromUrl", () => {
  it.each([
    ["/mendilo/abc123", "abc123"],
    ["/2027/mendilo/abc123/", "abc123"],
    ["/2027/mendilo-sekreta/abc123/", "abc123"],
    ["/2027/mendilo", null],
    ["/2027/mendilo-sekreta/", null],
    ["/2027/aligxilo/abc123/", null],
    ["/2027/ne-mendilo/abc123/", null],
  ])("reads the ID in %s", (path, id) => {
    window.history.replaceState({}, "", path)
    expect(registrationIdFromUrl()).toBe(id)
  })
})

describe("flagEmoji", () => {
  it("turns a country code into its two regional indicator symbols", () => {
    expect(flagEmoji("fr")).toBe("\u{1F1EB}\u{1F1F7}")
    expect(flagEmoji("SKX")).toBe(flagEmoji("sk"))
    expect([...flagEmoji("PL")]).toHaveLength(2)
  })
})

describe.each([
  ["helpers/functions scrollTo", (id, px) => scrollTo(id, px)],
  ["mixin scrollTo", (id, px) => mixins.methods.scrollTo.call({ $nextTick: nextTick }, id, px)],
])("%s", (_, scroll) => {
  it("scrolls to the element, with an offset", async () => {
    const spy = vi.spyOn(window, "scrollTo").mockImplementation(() => {})
    const el = document.createElement("div")
    el.id = "target"
    document.body.appendChild(el)
    vi.spyOn(el, "getBoundingClientRect").mockReturnValue({ top: 500 })

    scroll("target", 40)
    await nextTick()
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ top: 500 + window.scrollY - 40, left: 0 }))
  })

  it("does nothing when the element does not exist", async () => {
    const spy = vi.spyOn(window, "scrollTo").mockImplementation(() => {})
    scroll("missing")
    await nextTick()
    expect(spy).not.toHaveBeenCalled()
  })
})

describe("mixin helpers", () => {
  it("formats minutes as HH:MM", () => {
    expect(mixins.methods.minutesToTime(0)).toBe("00:00")
    expect(mixins.methods.minutesToTime(9 * 60 + 5)).toBe("09:05")
  })

  it("formats dates like the time helper", async () => {
    const { formatDateString } = await import("@/helpers/time.js")
    for (const args of [["2027-07-05"], ["2027-07-05", true], ["2027-07-05", false, true]]) {
      expect(mixins.methods.formatDate(...args)).toBe(formatDateString(...args))
    }
  })
})
