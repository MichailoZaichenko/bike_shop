const cookieBanner = document.getElementById('cookie-banner');
const acceptButton = document.getElementById('accept-cookie');
const rejectButton = document.getElementById('reject-cookie');

// Функция для создания cookie
function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Функция для получения значения cookie
function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

// Функция для проверки, принял ли пользователь cookie
function checkAcceptedCookie() {
  var acceptedCookie = getCookie("acceptedCookie");
  return acceptedCookie == "true";
}

if (!localStorage.getItem("cookiesAccepted")) {
    cookieBanner.style.display = "block";
  }

// Отображение формы куки через 5 секунд
setTimeout(function() {
  if (!checkAcceptedCookie()) {
    document.getElementById("cookie-banner").style.display = "block";
  }
}, 5000);

// Обработчик события клика на кнопку принятия cookie
document.getElementById("accept-cookie").addEventListener("click", function() {
  setCookie("acceptedCookie", "true", 30);
  document.getElementById("cookie-banner").style.display = "none";
});

// Обработчик события клика на кнопку отклонения cookie
document.getElementById("reject-cookie").addEventListener("click", function() {
  setCookie("acceptedCookie", "false", 30);
  window.location.href = "https://google.com"; // замените ссылкой на свой сайт
});
