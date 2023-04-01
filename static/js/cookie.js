// const cookieBanner = document.getElementById('cookie-banner');
// const acceptButton = document.getElementById('accept-cookie');
// const rejectButton = document.getElementById('reject-cookie');
//
// // Функция для проверки, принял ли пользователь cookie
// function checkAcceptedCookie() {
//     return localStorage.getItem('cookieAccepted') === 'true';
// }
//
// // Отображение формы куки, если пользователь ещё не принимал куки
// if (!checkAcceptedCookie()) {
//     cookieBanner.style.display = "block";
// }
//
// // Обработчик события клика на кнопку принятия cookie
// acceptButton.addEventListener("click", function() {
//     localStorage.setItem('cookieAccepted', 'true');
//     cookieBanner.style.display = "none";
// });
//
// // Обработчик события клика на кнопку отклонения cookie
// rejectButton.addEventListener("click", function() {
//     localStorage.setItem('cookieAccepted', 'false');
//     window.location.href = "https://google.com"; // замените ссылкой на свой сайт
// });

document.addEventListener("DOMContentLoaded", function() {
  const cookieBanner = document.getElementById("cookie-banner");
  const acceptCookie = document.getElementById("accept-cookie");
  const rejectCookie = document.getElementById("reject-cookie");

  function setCookie(name, value, days) {
    let expires = "";
    if (days) {
      let date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1, c.length);
      }
      if (c.indexOf(nameEQ) == 0) {
        return c.substring(nameEQ.length, c.length);
      }
    }
    return null;
  }

  function eraseCookie(name) {
    document.cookie = name + "=; Max-Age=-99999999;";
  }

  function hideCookieBanner() {
    cookieBanner.style.display = "none";
  }

  function acceptCookieBanner() {
    setCookie("cookie_accepted", true, 365);
    hideCookieBanner();
  }

  function rejectCookieBanner() {
    eraseCookie("cookie_accepted");
    hideCookieBanner();
  }

  if (getCookie("cookie_accepted")) {
    hideCookieBanner();
  } else {
    acceptCookie.addEventListener("click", acceptCookieBanner);
    rejectCookie.addEventListener("click", rejectCookieBanner);
  }
});
