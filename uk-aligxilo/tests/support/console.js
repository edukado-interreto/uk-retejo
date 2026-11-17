// Any console.warn / console.error (Vue warnings, naive-ui warnings, logged errors)
// fails the test, unless the test declared it with `expectConsole()`.
import { expect, vi } from "vitest"

let messages = []
let expected = []

const format = (args) =>
  args.map((a) => (a instanceof Error ? `${a.name}: ${a.message}` : typeof a === "string" ? a : String(a))).join(" ")

export function resetConsole() {
  messages = []
  expected = []
  for (const level of ["warn", "error"]) {
    vi.spyOn(console, level).mockImplementation((...args) => {
      messages.push(`[${level}] ${format(args)}`)
    })
  }
}

/**
 * Declare a console message this test is known to produce (e.g. a known bug).
 * The test fails if the message does NOT appear, so the exception goes away once fixed.
 */
export function expectConsole(pattern, reason) {
  expected.push({ pattern, reason })
}

export function checkConsole() {
  const unexpected = messages.filter((m) => !expected.some(({ pattern }) => pattern.test(m)))
  expect(unexpected, "unexpected console warnings/errors").toEqual([])
  for (const { pattern, reason } of expected) {
    expect(
      messages.some((m) => pattern.test(m)),
      `expected console message ${pattern} did not happen (fixed? ${reason})`,
    ).toBe(true)
  }
}
