const duiRegExp = /(^\d{8})-(\d$)/;
const mobilePhoneRegExP = /^[67]\d{3}-\d{4}$/;
const residentialPhoneRegExP = /^2\d{3}-\d{4}$/

export function isDUI(dui) {
    if (!duiRegExp.test(dui)) return false;

    let sum = 0;
    const [digits, verifier] = dui.split('-');
    for (let i = 0; i < digits.length; i++) {
        sum += Number(digits[i]) * (digits.length + 1 - i);
    }

    return Number(verifier) === (10 - (sum % 10)) % 10 && sum > 0;
}

export function isPhoneNumber(phone) {
    return phone.match(mobilePhoneRegExP) || phone.match(residentialPhoneRegExP);
}