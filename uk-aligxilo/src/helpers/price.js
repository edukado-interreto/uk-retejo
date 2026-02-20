/**
 * @param {string} birthdayStr
 * @param {boolean} showPersonalData
 * @param {string} memberAgeGroup
 * @param {array} formOptions
 * @param {boolean} strict
 * @returns true if the user is a youth. If strict is false, returns true if the user can be a youth.
 */
export const isYouth = (birthdayStr, showPersonalData, memberAgeGroup, formOptions, strict = false) => {
  if (!showPersonalData) {
    if (memberAgeGroup === 'youth' || memberAgeGroup === 'membershipyouth') {
      return true;
    }
    if (memberAgeGroup !== null) {
      return false;
    }
  }
  if (!birthdayStr) {
    return !strict;
  }
  const birthday = new Date(birthdayStr);
  const child = new Date(formOptions.childBirthDate);
  const youth = new Date(formOptions.youthBirthDate);
  return birthday.getTime() >= youth.getTime() && birthday.getTime() < child.getTime();
};

/**
 * @param {string} birthdayStr
 * @param {boolean} showPersonalData
 * @param {string} memberAgeGroup
 * @param {array} formOptions
 * @param {boolean} strict
 * @returns true if the user is a youth. If strict is false, returns true if the user can be a youth.
 */
export const isYouthForMembership = (birthdayStr, showPersonalData, memberAgeGroup, formOptions, strict = false) => {
  if (!showPersonalData) {
    if (memberAgeGroup === 'membershipyouth') {
      return true;
    }
    if (memberAgeGroup !== null) {
      return false;
    }
  }
  if (!birthdayStr) {
    return !strict;
  }
  const birthday = new Date(birthdayStr);
  const child = new Date(formOptions.childBirthDate);
  const youth = new Date(formOptions.membershipYouthBirthDate);
  return birthday.getTime() >= youth.getTime() && birthday.getTime() < child.getTime();
};

/**
 * @param {string} birthdayStr
 * @param {boolean} showPersonalData
 * @param {string} memberAgeGroup
 * @param {array} formOptions
 * @param {boolean} strict
 * @returns true if the user is a child. If strict is false, returns true if the user can be a child.
 */
export const isChild = (birthdayStr, showPersonalData, memberAgeGroup, formOptions, strict = false) => {
  if (!showPersonalData) {
    if (memberAgeGroup === 'child') {
      return true;
    }
    if (memberAgeGroup !== null) {
      return false;
    }
  }
  if (!birthdayStr) {
    return !strict;
  }
  const birthday = new Date(birthdayStr);
  const child = new Date(formOptions.childBirthDate);
  return birthday.getTime() >= child.getTime();
};

function membershipPrice(form, formOptions, countryMembershipCategory, showPersonalData, memberAgeGroup) {
  if (
    form.membreco === formOptions.boolValues.yes ||
    form.volas_membrigxi !== formOptions.boolValues.yes ||
    form.membreco_tipo === undefined
  ) {
    return 0;
  }
  let type = form.membreco_tipo;
  if (type === 'MB') {
    if (isChild(form.naskigxdato, showPersonalData, memberAgeGroup, formOptions, true)) {
      type = 'MB75';
    } else if (isYouthForMembership(form.naskigxdato, showPersonalData, memberAgeGroup, formOptions, true)) {
      type = 'MB50';
    }
  }
  return formOptions.membershipPrice[countryMembershipCategory][type];
}

export const calculatePrice = (
  form,
  pricesList,
  countryMembershipCategory,
  discount,
  formOptions,
  showPersonalData,
  memberAgeGroup,
) => {
  if (form.kotizo === null) {
    return null;
  }

  const aligxkotizo = pricesList[form.kotizo].price;
  const membrokotizo = membershipPrice(form, formOptions, countryMembershipCategory, showPersonalData, memberAgeGroup);
  let total = aligxkotizo + membrokotizo;
  const price = {
    aligxkotizo: aligxkotizo,
    sum: total,
  };

  if (membrokotizo > 0) {
    price.membrigxo = membrokotizo;
  }

  for (const field in form) {
    if (field.startsWith('donaco_')) {
      if (parseFloat(form[field]) !== 0 && form[field] !== null) {
        price[field] = form[field];
        total += form[field];
      }
    }
  }
  if (discount !== 0 && aligxkotizo > discount) {
    price.discount = -discount;
    total -= discount;
  }
  total = Math.round(total * 100) / 100;
  price.sum = total;
  return price;
};
