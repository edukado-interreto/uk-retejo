<template>
  <n-form-item :label="label" :required="isRequired" :path="fieldName" :feedback="feedback" :style="style">
    <n-radio-group v-model:value="modelValue" :name="fieldName" :id="fieldName" :disabled="!isEditable">
      <div class="radio-option" v-for="option in optionsList" :key="option.value">
        <n-radio :value="option.value" :disabled="isEditable && disabledOptions.includes(option.value)">
          <span v-html="option.label"></span>
        </n-radio>
        <n-button text style="font-size: 20px" v-if="option.description" @click="showDescription(option)">
          <n-icon color="#2050cf">
            <InformationCircleOutline />
          </n-icon>
        </n-button>
      </div>
    </n-radio-group>
  </n-form-item>

  <n-modal v-model:show="showModal" preset="card" style="max-width: 600px" :title="descriptionTitle" size="small">
    <div v-html="descriptionText"></div>
  </n-modal>
</template>

<script setup>
import { ref, computed, inject } from 'vue';
import { useStore } from 'vuex';
import { NIcon } from 'naive-ui';
import InformationCircleOutline from '@/components/ui/icons/InformationCircleOutline.vue';

const props = defineProps({
  modelValue: String,
  fieldName: String,
  options: Object,
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  vertical: {
    type: Boolean,
    default: false,
  },
  help: {
    type: String,
    default: null,
  },
  label: {
    type: String,
    default: null,
  },
  style: {
    default: null,
  },
  disabledOptions: {
    type: Array,
    default: () => [],
  },
});

const store = useStore();
const fields = computed(() => store.getters.fields);
const editMode = computed(() => store.getters.editMode);

const modelValue = defineModel('modelValue');

const optionsList = computed(() => {
  if (Array.isArray(props.options)) {
    for (let i = 0; i < props.options.length; i++) {
      if (typeof props.options[i] !== 'object') {
        props.options[i] = { value: props.options[i], label: props.options[i] };
      }
    }
    return props.options;
  }

  const optionsArray = [];
  for (const [key, value] of Object.entries(props.options)) {
    optionsArray.push({ value: key, label: value });
  }
  return optionsArray;
});

const field = computed(() => fields.value[props.fieldName]);
const isRequired = computed(
  () =>
    props.required ||
    ('validation_rules' in field.value && Object.values(field.value.validation_rules).includes('required')),
);
const isEditable = computed(() => !editMode.value || field.value.editable !== false);
const label = computed(() => (props.label ? props.label : field.value.label));

const formErrors = inject('formErrors');
const hasError = computed(() => props.fieldName in formErrors.value);
const error = computed(() => (hasError.value ? formErrors.value[props.fieldName] : ''));
const feedback = computed(() => (hasError.value ? error.value : props.help));

// Modal
const showModal = ref(false);
const descriptionTitle = ref('');
const descriptionText = ref('');

function showDescription(option) {
  descriptionTitle.value = option.label;
  descriptionText.value = option.description;
  showModal.value = true;
}
</script>

<style scoped lang="scss">
.radio-option {
  margin: 6px 0;
  display: flex;
  position: relative;

  .button {
    position: absolute;
  }
}
</style>
