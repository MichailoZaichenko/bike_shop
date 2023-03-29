const cookieBanner = document.getElementById('cookie-banner');
const acceptButton = document.getElementById('accept-cookie');
const rejectButton = document.getElementById('reject-cookie');

// Функция для проверки, принял ли пользователь cookie
function checkAcceptedCookie() {
    return localStorage.getItem('cookieAccepted') === 'true';
}

// Отображение формы куки, если пользователь ещё не принимал куки
if (!checkAcceptedCookie()) {
    cookieBanner.style.display = "block";
}

// Обработчик события клика на кнопку принятия cookie
acceptButton.addEventListener("click", function() {
    localStorage.setItem('cookieAccepted', 'true');
    cookieBanner.style.display = "none";
});

// Обработчик события клика на кнопку отклонения cookie
rejectButton.addEventListener("click", function() {
    localStorage.setItem('cookieAccepted', 'false');
    window.location.href = "https://google.com"; // замените ссылкой на свой сайт
});