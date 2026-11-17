import { flushPromises, mount } from "@vue/test-utils"
import { defineComponent, h, reactive } from "vue"

import BaseApp from "@/embedded/BaseApp.vue"

/** Mount a root app (src/embedded/*.vue) like the entrypoints do, and wait for its API calls. */
export async function mountApp(App, options = {}) {
  const wrapper = mount(App, { attachTo: container(), ...options })
  await settle()
  return wrapper
}

/**
 * Mount a single component inside BaseApp (naive-ui providers) with the `formErrors`
 * injection that MainForm provides to the form fields.
 * Returns `wrapper` (the component itself) and `state`, the reactive props: changing it
 * re-renders the component and `update:xxx` events are written back into it (v-model).
 */
export async function mountComponent(Component, { props = {}, slots, formErrors = { value: {} } } = {}) {
  const state = reactive({ ...props })
  const Host = defineComponent({
    provide: { formErrors },
    render: () =>
      h(BaseApp, null, {
        default: () => h(Component, { ...state, ...listenersFor(state) }, slots),
      }),
  })
  const host = mount(Host, { attachTo: container() })
  await settle()
  return { wrapper: host.findComponent(Component), state }
}

function listenersFor(state) {
  return Object.fromEntries(Object.keys(state).map((key) => [`onUpdate:${key}`, (value) => (state[key] = value)]))
}

function container() {
  const el = document.createElement("div")
  document.body.appendChild(el)
  return el
}

/** Let pending promises (mocked API calls) and the following re-renders finish. */
export async function settle() {
  for (let i = 0; i < 3; i++) {
    await flushPromises()
  }
}
