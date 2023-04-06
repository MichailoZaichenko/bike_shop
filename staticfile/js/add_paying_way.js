const form = document.querySelector('form');
const cardNumberInput = document.getElementById('card_number');
const expirationDateInput = document.getElementById('expiration_date');
const cvvInput = document.getElementById('cvv');

form.addEventListener('submit', (event) => {
  event.preventDefault();

// Проверяем, что все поля заполнены
if (nameInput.value === '' || addressInput.value === '' || cardNumberInput.value === '' || expirationDateInput.value === '' || cvvInput.value === '') {
alert('Пожалуйста, заполните все поля.');
return;
}

// Проверяем, что номер карты состоит из 16 цифр
if (cardNumberInput.value.length !== 16 || isNaN(cardNumberInput.value)) {
alert('Пожалуйста, введите 16-значный номер вашей карты.');
return;
}

// Проверяем, что срок действия карты в формате ММ/ГГ
const expirationDateRegex = /^(0[1-9]|1[0-2])\/(\d{2})$/;
if (!expirationDateRegex.test(expirationDateInput.value)) {
alert('Пожалуйста, введите срок действия вашей карты в формате ММ/ГГ.');
return;
}

// Проверяем, что cvv состоит из 3 цифр
if (cvvInput.value.length !== 3 || isNaN(cvvInput.value)) {
alert('Пожалуйста, введите 3-значный код безопасности вашей карты.');
return;
}

// Если все проверки прошли успешно, отправляем форму
form.submit();
});
