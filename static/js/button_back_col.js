const toggleButton = document.getElementById('toggle-theme');
const bodyElement = document.body;

toggleButton.addEventListener('click', () => {
  bodyElement.classList.toggle('light-theme');
  bodyElement.classList.toggle('dark-theme');
});
