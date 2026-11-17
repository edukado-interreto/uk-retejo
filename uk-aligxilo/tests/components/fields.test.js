// Form fields and small UI components, mounted on their own
import { mount } from "@vue/test-utils"
import { beforeEach, describe, expect, it } from "vitest"
import { defineComponent, h, nextTick, ref } from "vue"

import AdminBreadcrumbs from "@/components/admin/AdminBreadcrumbs.vue"
import CheckboxInput from "@/components/form/fields/CheckboxInput.vue"
import DateInput from "@/components/form/fields/DateInput.vue"
import MultiCheckboxInput from "@/components/form/fields/MultiCheckboxInput.vue"
import NumberInput from "@/components/form/fields/NumberInput.vue"
import RadioInput from "@/components/form/fields/RadioInput.vue"
import SelectInput from "@/components/form/fields/SelectInput.vue"
import TextInput from "@/components/form/fields/TextInput.vue"
import TimeInput from "@/components/form/fields/TimeInput.vue"
import UeaCodeInput from "@/components/form/fields/UeaCodeInput.vue"
import EmailIcon from "@/components/ui/icons/EmailIcon.vue"
import ExternalLinkIcon from "@/components/ui/icons/ExternalLinkIcon.vue"
import FacebookIcon from "@/components/ui/icons/FacebookIcon.vue"
import InformationCircleOutline from "@/components/ui/icons/InformationCircleOutline.vue"
import InstagramIcon from "@/components/ui/icons/InstagramIcon.vue"
import TelegramIcon from "@/components/ui/icons/TelegramIcon.vue"
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue"
import SlideTransition from "@/components/ui/SlideTransition.vue"
import store from "@/store.js"
import { fixtures } from "../support/api.js"
import { expectConsole } from "../support/console.js"
import { mountComponent, settle } from "../support/mount.js"

const { formOptions } = fixtures.loaddata

beforeEach(async () => {
  await store.dispatch("loaddata")
})

const FIELDS = [
  { component: TextInput, props: { fieldName: "persona_nomo", modelValue: "" } },
  { component: TextInput, props: { fieldName: "komento", modelValue: "", type: "textarea" } },
  { component: SelectInput, props: { fieldName: "titolo", modelValue: null, options: formOptions.titles } },
  { component: RadioInput, props: { fieldName: "genro", modelValue: null, options: formOptions.genders } },
  { component: CheckboxInput, props: { fieldName: "konsento_aligxlisto", modelValue: false } },
  {
    component: MultiCheckboxInput,
    props: { fieldName: "kongreslibro_adreso", modelValue: [], options: formOptions.kongreslibro },
  },
  { component: DateInput, props: { fieldName: "naskigxdato", modelValue: null } },
  {
    component: NumberInput,
    props: { fieldName: "donaco_uk", modelValue: "0" },
    // Known bug (unused component): `modelValue: String` is passed to <n-input-number>
    knownWarning: /Invalid prop: type check failed for prop "value". Expected Number/,
  },
  { component: TimeInput, props: { fieldName: "komento", modelValue: null } },
  { component: UeaCodeInput, props: { fieldName: "uea_kodo", modelValue: "" } },
]
const name = ({ component, props }) => `${component.name ?? component.__name} (${props.fieldName})`
// Known bugs, the error message of the server is lost:
// - TextInput.vue and SelectInput.vue read `formErrors.value[field.valueName]` (undefined)
//   instead of `formErrors.value[props.fieldName]`
// - DateInput.vue and TimeInput.vue compute `error` but bind `:feedback="help"`
const LOSES_ERROR_MESSAGE = [TextInput, SelectInput, DateInput, TimeInput]
const INPUT = "input, textarea, .n-base-selection, .n-checkbox"
const DISABLED = "input[disabled], textarea[disabled], .n-base-selection--disabled, .n-checkbox--disabled"

describe.each(FIELDS.map((f) => [name(f), f]))("%s", (_, { component, props, knownWarning }) => {
  beforeEach(() => {
    if (knownWarning) expectConsole(knownWarning, `known bug in ${name({ component, props })}`)
  })

  it("renders a form item with its input", async () => {
    const { wrapper } = await mountComponent(component, { props })
    expect(wrapper.find(".n-form-item").exists()).toBe(true)
    expect(wrapper.find(INPUT).exists()).toBe(true)
  })

  // Known bug: MultiCheckboxInput.vue gives each <n-checkbox> `:disabled="isEditable && ..."`,
  // an explicit `false` that overrides the disabled group, so the boxes stay clickable
  const disabledTest = component === MultiCheckboxInput ? it.fails : it
  disabledTest("is disabled in edit mode when the field is not editable", async () => {
    store.dispatch("setEditMode", true)
    const { wrapper } = await mountComponent(component, { props })
    const editable = store.getters.fields[props.fieldName].editable !== false
    expect(wrapper.find(DISABLED).exists()).toBe(!editable)
  })

  const errorTest = LOSES_ERROR_MESSAGE.includes(component) ? it.fails : it
  errorTest("shows the error of the server", async () => {
    const formErrors = { value: { [props.fieldName]: "error" } }
    const { wrapper } = await mountComponent(component, { props, formErrors })
    const feedback = wrapper.find(".n-form-item-feedback")
    expect(feedback.exists()).toBe(true)
    expect(feedback.text()).not.toBe("")
  })
})

describe("v-model", () => {
  it("TextInput", async () => {
    const { wrapper, state } = await mountComponent(TextInput, { props: { fieldName: "persona_nomo", modelValue: "" } })
    await wrapper.find("input").setValue("abc")
    expect(state.modelValue).toBe("abc")
  })

  it("CheckboxInput", async () => {
    const { wrapper, state } = await mountComponent(CheckboxInput, {
      props: { fieldName: "konsento_aligxlisto", modelValue: false },
    })
    await wrapper.find(".n-checkbox").trigger("click")
    expect(state.modelValue).toBe(true)
  })

  it("RadioInput", async () => {
    const { wrapper, state } = await mountComponent(RadioInput, {
      props: { fieldName: "genro", modelValue: null, options: formOptions.genders },
    })
    const radios = wrapper.findAll("input[type=radio]")
    expect(radios).toHaveLength(Object.keys(formOptions.genders).length)
    await radios[1].setValue()
    expect(state.modelValue).toBe(Object.keys(formOptions.genders)[1])
  })

  describe("options of the checkbox and radio lists", () => {
    const options = [
      ["plain strings", ["a", "b"], 2],
      ["objects with a description", [{ value: "x", label: "X", description: "More about X" }], 1],
    ]

    it.each(options)("MultiCheckboxInput accepts %s", async (_, list, count) => {
      const { wrapper } = await mountComponent(MultiCheckboxInput, {
        props: { fieldName: "kongreslibro_adreso", modelValue: [], options: structuredClone(list) },
      })
      expect(wrapper.findAll(".n-checkbox")).toHaveLength(count)
    })

    it.each(options)("RadioInput accepts %s", async (_, list, count) => {
      const { wrapper } = await mountComponent(RadioInput, {
        props: { fieldName: "genro", modelValue: null, options: structuredClone(list) },
      })
      expect(wrapper.findAll(".n-radio")).toHaveLength(count)
    })

    it.each([MultiCheckboxInput, RadioInput])("opens the description of an option in a dialog (%#)", async (component) => {
      const { wrapper } = await mountComponent(component, {
        props: {
          fieldName: component === RadioInput ? "genro" : "kongreslibro_adreso",
          modelValue: component === RadioInput ? null : [],
          options: [{ value: "x", label: "X", description: "More about X" }],
        },
      })
      await wrapper.find(".n-button").trigger("click")
      await settle()
      expect(document.querySelector(".n-modal, .n-card")).not.toBeNull()
      expect(wrapper.vm.showModal).toBe(true)
    })
  })

  it("MultiCheckboxInput", async () => {
    const { wrapper, state } = await mountComponent(MultiCheckboxInput, {
      props: { fieldName: "kongreslibro_adreso", modelValue: [], options: formOptions.kongreslibro },
    })
    const boxes = wrapper.findAll(".n-checkbox")
    expect(boxes).toHaveLength(Object.keys(formOptions.kongreslibro).length)
    await boxes[0].trigger("click")
    await boxes[1].trigger("click")
    expect(state.modelValue).toEqual(Object.keys(formOptions.kongreslibro).slice(0, 2))
  })

  it("UeaCodeInput only asks the server for complete codes", async () => {
    const { wrapper, state } = await mountComponent(UeaCodeInput, { props: { fieldName: "uea_kodo", modelValue: "" } })
    await wrapper.find("input").setValue("abc")
    await settle()
    expect(wrapper.emitted("codeChecked").at(-1)).toEqual([{ valid: false }])
    await wrapper.find("input").setValue("abcd-x")
    await settle()
    expect(state.modelValue).toBe("abcd-x")
    expect(wrapper.emitted("codeChecked").at(-1)).toEqual([{ valid: false }])
    expect(wrapper.find(".n-form-item-feedback--error, .n-form-item-blank--error").exists()).toBe(true)
  })
})

describe("UI components", () => {
  it.each([EmailIcon, ExternalLinkIcon, FacebookIcon, InformationCircleOutline, InstagramIcon, TelegramIcon])(
    "icon %#",
    (Icon) => {
      expect(mount(Icon).find("svg").exists()).toBe(true)
    },
  )

  it("LoadingSpinner", async () => {
    const { wrapper } = await mountComponent(LoadingSpinner)
    expect(wrapper.find(".loading .n-spin").exists()).toBe(true)
  })

  it("AdminBreadcrumbs", async () => {
    const { RouterLinkStub } = await import("@vue/test-utils")
    const wrapper = mount(AdminBreadcrumbs, {
      props: { title: "x" },
      global: { stubs: { RouterLink: RouterLinkStub } },
    })
    expect(wrapper.find(".n-breadcrumb").exists()).toBe(true)
    expect(wrapper.findComponent(RouterLinkStub).exists()).toBe(true)
  })

  it("SlideTransition animates in and out, then cleans the inline styles", async () => {
    const show = ref(false)
    const Host = defineComponent({
      render: () => h(SlideTransition, { duration: 1 }, () => (show.value ? h("div", { class: "content" }) : null)),
    })
    const wrapper = mount(Host, { attachTo: document.body, global: { stubs: { transition: false } } })
    const wait = () => new Promise((resolve) => setTimeout(resolve, 20))

    show.value = true
    await nextTick()
    const el = wrapper.find(".content").element
    expect(el.style.transitionProperty).toContain("height")
    await wait()
    expect(el.getAttribute("style") ?? "").not.toContain("height")

    show.value = false
    await nextTick()
    expect(el.style.overflow).toBe("hidden")
    await wait()
    await nextTick()
    expect(wrapper.find(".content").exists()).toBe(false)
  })
})
