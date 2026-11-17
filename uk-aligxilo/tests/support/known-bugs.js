// Warnings caused by known bugs in src/. Each test that triggers one declares it, and
// fails as soon as the warning disappears, so remove the entry once the bug is fixed.
import { expectConsole } from "./console.js"

export function expectBookingWarnings() {
  expectConsole(
    /Failed to resolve component: router-link/,
    "FormBooking.vue uses <router-link> but the embedded apps have no vue-router",
  )
  expectConsole(
    /Invalid prop: type check failed for prop "trip"/,
    "FormTripsTrip.vue declares `trip: Array` but receives a trip object",
  )
}

export function expectUndeclaredMembershipCategory() {
  expectConsole(
    /Property "countryMembershipCategoryFromDB" was accessed during render but is not defined/,
    "MainForm.vue assigns countryMembershipCategoryFromDB but does not declare it in data()",
  )
}

export function expectInvitationDisabledProp() {
  expectConsole(
    /Invalid prop: type check failed for prop "disabled". Expected Boolean, got String/,
    "FormInvitation.vue passes the birth date string to <n-date-picker :disabled>",
  )
}
