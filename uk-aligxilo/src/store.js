import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state() {
    return {
      basicFields: [],
      allFields: [],
      editMode: false,
      countries: [],
      formOptions: [],
      detectedCountry: null,
      prices: [],
      currentPeriod: 0,
      registrationPeriods: [],
      key: null, // Admin key
      userCountry: null,
    };
  },
  actions: {
    async loaddata(context) {
      await axios
        .get('/loaddata')
        .then((response) => {
          context.commit('setBasicFields', response.data.basicFields);
          context.commit('setAllFields', response.data.allFields);
          context.commit('setDetectedCountry', response.data.detectedCountry);
          context.commit('setUserCountry', response.data.detectedCountry);
          context.commit('setCountries', response.data.countries);
          context.commit('setFormOptions', response.data.formOptions);
          context.commit('setPrices', response.data.prices);
          context.commit('setCurrentPeriod', response.data.currentPeriod);
          context.commit('setRegistrationPeriods', response.data.registrationPeriods);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    login(context, payload) {
      context.commit('setKey', payload);
    },
    logout(context) {
      context.commit('setKey', null);
    },
    setEditMode(context, payload) {
      context.commit('setEditMode', payload);
    },
    setUserCountry(context, payload) {
      context.commit('setUserCountry', payload);
    },
  },
  mutations: {
    setBasicFields(state, payload) {
      state.basicFields = payload;
    },
    setAllFields(state, payload) {
      state.allFields = payload;
    },
    setEditMode(state, payload) {
      state.editMode = payload;
    },
    setCountries(state, payload) {
      state.countries = payload;
    },
    setUserCountry(state, payload) {
      state.userCountry = payload;
    },
    setDetectedCountry(state, payload) {
      state.detectedCountry = payload;
    },
    setFormOptions(state, payload) {
      state.formOptions = payload;
    },
    setPrices(state, payload) {
      state.prices = payload;
    },
    setCurrentPeriod(state, payload) {
      state.currentPeriod = payload;
    },
    setRegistrationPeriods(state, payload) {
      state.registrationPeriods = payload;
    },
    setKey(state, payload) {
      state.key = payload;
    },
  },
  getters: {
    fields(state) {
      return state.editMode ? state.allFields : state.basicFields;
    },
    editMode(state) {
      return state.editMode;
    },
    countries(state) {
      return state.countries;
    },
    detectedCountry(state) {
      return state.detectedCountry;
    },
    formOptions(state) {
      return state.formOptions;
    },
    prices(state) {
      return state.prices;
    },
    currentPeriod(state) {
      return state.currentPeriod;
    },
    registrationPeriods(state) {
      return state.registrationPeriods;
    },
    key(state) {
      return state.key;
    },
    isLoggedIn(state) {
      return state.key !== null;
    },
  },
});

export default store;
