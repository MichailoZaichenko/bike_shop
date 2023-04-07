document.getElementById('showPassword').addEventListener('click', function () {
    let passwordField = document.getElementById('id_password');
    if (passwordField.type === 'password') {
        passwordField.type === 'text';
    } else {
        passwordField.type = 'password';
    }
});