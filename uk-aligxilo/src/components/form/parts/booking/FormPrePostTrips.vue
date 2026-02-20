<template>
  <n-alert title="Jam mendita" type="info" v-if="alreadyBooked" style="margin-bottom: 2rem">
    {{ form[type + '_cxefmendanto_nomo'] }} jam mendis {{ type === 'ak' ? 'antaŭ' : 'post' }}kongreson por vi.
  </n-alert>
  <template v-else>
    <radio-input v-model="form[type]" :field-name="type" :options="trips" :disabled-options="fullTrips" vertical />
    <slide-transition>
      <div v-if="form[type] && Object.keys(rooms).length > 1">
        <radio-input
          v-model="form[type + '_cxambro']"
          :field-name="type + '_cxambro'"
          :options="roomOptions"
          :disabled-options="fullRooms"
          vertical
          required
          style="margin-bottom: 1.5rem"
          help="La indikita prezo estas por 1 persono, sed vi kiel mendanto pagos por la tuta ĉambro."
        />

        <slide-transition>
          <div v-if="pickedRoom && pickedRoom.people === 2">
            <uea-code-input
              v-model="form[type + '_kunlogxanto']"
              :field-name="type + '_kunlogxanto'"
              :current-user="form.uea_kodo"
              :mode="type"
              help="Se vi ne konas la UEA-kodon aŭ la persono ankoraŭ ne estas kongresano, bonvolu indiki la nomon en la sekva kampo."
              @code-checked="ueaCodeResult"
            />

            <slide-transition>
              <text-input
                v-if="showRoommate2"
                style="margin-top: 1rem"
                v-model="form[type + '_kunlogxanto2']"
                :field-name="type + '_kunlogxanto2'"
                required
              />
            </slide-transition>
          </div>
        </slide-transition>
      </div>
    </slide-transition>
  </template>
</template>

<script>
import { mapGetters } from 'vuex';
import RadioInput from '@/components/form/fields/RadioInput.vue';
import SlideTransition from '@/components/ui/SlideTransition.vue';
import UeaCodeInput from '@/components/form/fields/UeaCodeInput.vue';
import TextInput from '@/components/form/fields/TextInput.vue';

export default {
  name: 'FormPrePostTrips',
  components: { TextInput, UeaCodeInput, SlideTransition, RadioInput },
  props: {
    modelValue: Object,
    type: String,
    defaultTrip: String, // Trip already picked by user before loading the form
    defaultRoom: String, // Room already picked by user before loading the form
  },
  emits: ['update:modelValue'],
  data() {
    return {
      codeValid: false,
    };
  },
  computed: {
    ...mapGetters(['formOptions']),
    form: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
    trips() {
      const trips = { '': 'Mi ne mendas ' + (this.type === 'ak' ? 'antaŭ' : 'post') + 'kongresan ekskurson' };
      Object.values(this.formOptions.preposttrips)
        .filter((t) => t.type === this.type)
        .forEach((trip) => {
          const price = Object.keys(trip.rooms).length === 1 ? trip.rooms[''].price + ' €' : '';
          const shortId = trip.id[0] + trip.id[2];
          trips[trip.id] = `${shortId}: ${trip.name}`;
          if (price !== '') trips[trip.id] += ` – ${price}`;
          if (this.fullTrips.includes(trip.id)) {
            trips[trip.id] += ' <span style="color: #ff2626">(plena!)</span>';
          }
        });
      return trips;
    },
    fullTrips() {
      return Object.values(this.formOptions.preposttrips)
        .filter(
          (t) =>
            t.type === this.type &&
            t.id !== this.defaultTrip &&
            Object.values(t.rooms).find((r) => r.available) === undefined,
        )
        .map((t) => t.id);
    },
    fullRooms() {
      const full = [];
      Object.keys(this.rooms).forEach((r) => {
        if (!this.rooms[r].available && r !== this.defaultRoom) {
          full.push(r);
        }
      });
      return full;
    },
    rooms() {
      return this.formOptions.preposttrips[this.form[this.type]].rooms;
    },
    roomOptions() {
      const rooms = {};
      Object.keys(this.rooms).forEach((r) => {
        rooms[r] = `${this.rooms[r].roomname} – ${this.rooms[r].price} €`;
        if (this.fullRooms.includes(r)) {
          rooms[r] += ' <span style="color: #ff2626">(plena!)</span>';
        }
      });
      return rooms;
    },
    alreadyBooked() {
      return this.form[this.type + '_cxefmendanto'] !== '';
    },
    pickedRoom() {
      if (!this.form[this.type] || !this.form[this.type + '_cxambro']) {
        return null;
      }
      return this.formOptions.preposttrips[this.form[this.type]].rooms[this.form[this.type + '_cxambro']];
    },
    showRoommate2() {
      return this.pickedRoom && (this.pickedRoom.people > 2 || (this.pickedRoom.people == 2 && !this.codeValid));
    },
  },
  methods: {
    ueaCodeResult(data) {
      this.codeValid = data.valid;
    },
  },
};
</script>

<style scoped></style>
