<template>
  <n-alert title="Jam mendita" type="info" v-if="alreadyBooked" style="margin-bottom: 2rem">
    {{ form.hotelo_cxefmendanto_nomo }} jam mendis loĝadon por vi.
  </n-alert>
  <template v-else>
    <radio-input
      v-model="form.hotelo"
      field-name="hotelo"
      :options="hotelOptions"
      :disabled-options="fullHotels"
      vertical
      @update:model-value="hotelChange"
    />

    <slide-transition>
      <div v-if="form.hotelo">
        <n-space>
          <date-input v-model="form.hotelo_de" field-name="hotelo_de" :min="pickedHotel.start" :max="maxStart" />
          <date-input v-model="form.hotelo_gxis" field-name="hotelo_gxis" :min="minEnd" :max="pickedHotel.end" />
        </n-space>

        <radio-input
          v-model="form.hotelo_cxambro"
          field-name="hotelo_cxambro"
          label="Tipo de ĉambro"
          :options="roomOptions"
          :disabled-options="fullRooms"
          vertical
          required
          style="margin-bottom: 1.5rem"
          :help="roomFeedback"
        />

        <text-input v-model="form.hotelo_alternativo" field-name="hotelo_alternativo" />

        <slide-transition>
          <div v-if="pickedRoom && pickedHotel.payForRoom && pickedRoom.people === 2">
            <uea-code-input
              v-model="form.hotelo_kunlogxanto"
              field-name="hotelo_kunlogxanto"
              :current-user="form.uea_kodo"
              mode="hotelo"
              help="Se vi ne konas la UEA-kodon aŭ la persono ankoraŭ ne estas kongresano, bonvolu indiki la nomon en la sekva kampo."
              @code-checked="ueaCodeResult"
            />
          </div>
        </slide-transition>

        <slide-transition>
          <text-input
            v-if="showRoommate2"
            style="margin-top: 1rem"
            v-model="form.hotelo_kunlogxanto2"
            field-name="hotelo_kunlogxanto2"
            :default-label="roommate2label"
            :required="roommate2required"
          />
        </slide-transition>

        <slide-transition>
          <checkbox-input v-model="form.parkloko" field-name="parkloko" v-if="showParking" />
        </slide-transition>
      </div>
    </slide-transition>
  </template>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import UeaCodeInput from '@/components/form/fields/UeaCodeInput.vue';
import TextInput from '@/components/form/fields/TextInput.vue';
import DateInput from '@/components/form/fields/DateInput.vue';
import CheckboxInput from '@/components/form/fields/CheckboxInput.vue';

const props = defineProps({
  modelValue: Object,
  defaultHotel: String, // Hotel already picked by user before loading the form
  defaultRoom: String, // Room already picked by user before loading the form
  defaultParking: Boolean, // Parking already picked by user before loading the form
});

const emit = defineEmits(['update:modelValue']);

const codeValid = ref(true);

const store = useStore();
const formOptions = computed(() => store.getters.formOptions);
const editMode = computed(() => store.getters.editMode);

const form = defineModel('modelValue');

const hotelOptions = computed(() => {
  const hotels = [{ value: '', label: 'Mi ne mendas hotelon' }];

  Object.values(formOptions.value.hotels).forEach((hotel) => {
    const newHotel = {
      value: hotel.id,
      label: `${hotel.id}: ${hotel.name}`,
      description: hotel.description,
    };
    if (fullHotels.value.includes(hotel.id)) {
      newHotel.label += ' <span style="color: #ff2626">(plena!)</span>';
    }
    hotels.push(newHotel);
  });
  return hotels;
});

const fullRooms = computed(() => {
  const full = [];
  Object.keys(rooms.value).forEach((r) => {
    if (!rooms.value[r].available && r !== props.defaultRoom) {
      full.push(r);
    }
  });
  return full;
});

const fullHotels = computed(() => {
  return Object.values(formOptions.value.hotels)
    .filter((h) => h.id !== props.defaultHotel && Object.values(h.rooms).find((r) => r.available) === undefined)
    .map((h) => h.id);
});

const rooms = computed(() => pickedHotel.value.rooms);

const pickedHotel = computed(() => (form.value.hotelo ? formOptions.value.hotels[form.value.hotelo] : null));
const pickedRoom = computed(() =>
  pickedHotel.value && form.value.hotelo_cxambro ? pickedHotel.value.rooms[form.value.hotelo_cxambro] : null,
);

const roomOptions = computed(() => {
  const options = {};
  Object.keys(rooms.value).forEach((r) => {
    options[r] = `${rooms.value[r].roomname} – ${rooms.value[r].price} €`;
    if (rooms.value[r].people > 1) {
      options[r] += ' p.p.';
    }
    if (fullRooms.value.includes(r)) {
      options[r] += ' <span style="color: #ff2626">(plena!)</span>';
    }
  });
  return options;
});

const alreadyBooked = computed(() => form.value.hotelo_cxefmendanto !== '');

const showRoommate2 = computed(
  () =>
    pickedRoom.value &&
    ((!pickedHotel.value.payForRoom && pickedRoom.value.people > 1) ||
      (pickedHotel.value.payForRoom &&
        (pickedRoom.value.people > 2 || (pickedRoom.value.people == 2 && !codeValid.value)))),
);

const roommate2required = computed(() => showRoommate2.value && pickedHotel.value.payForRoom);
const roommate2label = computed(() => (!roommate2required.value ? 'Mi volas loĝi kun' : null));

const roomFeedback = computed(() => {
  if (pickedHotel.value.payForRoom) {
    return 'La indikita prezo estas por 1 nokto por 1 persono, sed vi kiel mendanto pagos por la tuta ĉambro.';
  }
  if (pickedRoom.value && pickedRoom.value.people > 1) {
    return 'La indikita prezo estas por 1 persono, ne por tuta ĉambro.';
  }
  return 'La indikita prezo estas por 1 persono.';
});

const showParking = computed(() => {
  if (!form.value.hotelo) {
    return false;
  }
  return parkingByHotel.value[form.value.hotelo];
});

const parkingByHotel = computed(() => {
  const hotelsObj = {};
  Object.values(formOptions.value.hotels).forEach((h) => {
    hotelsObj[h.id] = h.parking;
  });
  if (editMode.value && props.defaultHotel && props.defaultParking) {
    hotelsObj[props.defaultHotel] = true;
  }
  return hotelsObj;
});

function ueaCodeResult(data) {
  codeValid.value = data.valid;
}

function hotelChange(newVal) {
  if (!(newVal in formOptions.value.hotels) || !(form.value.hotelo_cxambro in formOptions.value.hotels[newVal].rooms)) {
    form.value.hotelo_cxambro = null;
  }
  if (!(newVal in formOptions.value.hotels) || !parkingByHotel.value[newVal]) {
    form.value.parkloko = false;
  }
}

codeValid.value = form.value.hotelo_kunlogxanto !== '';
if (form.value.hotelo_de === '') {
  form.value.hotelo_de = formOptions.value.congressStart;
}
if (form.value.hotelo_gxis === '') {
  form.value.hotelo_gxis = formOptions.value.congressEnd;
}

const minEnd = computed(() => {
  if (form.value.hotelo_de) {
    // Add min nights to the picked start day
    let date = new Date(form.value.hotelo_de);
    date.setDate(date.getDate() + pickedHotel.value.minNights);
    return date.toISOString().split('T')[0];
  }
  return pickedHotel.value.start;
});

const maxStart = computed(() => {
  if (form.value.hotelo_gxis) {
    // Subtract min nights to the picked end day
    let date = new Date(form.value.hotelo_gxis);
    date.setDate(date.getDate() - pickedHotel.value.minNights);
    return date.toISOString().split('T')[0];
  }
  return pickedHotel.value.end;
});
</script>

<style scoped></style>
