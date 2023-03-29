// Todo make that way that you can save theme on pages on site
const toggleButton = document.getElementById('toggle-theme');
const bodyElement = document.body;
const tableElements = document.querySelectorAll('.table');
const navElement = document.querySelector('nav');
const headerElement = document.querySelector('header');

// Получение сохраненной темы из localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
  bodyElement.classList.add(savedTheme);
  tableElements.forEach(table => {
    table.classList.add(`table-${savedTheme}`);
  });
  headerElement.classList.add(`header-${savedTheme}`);
  navElement.classList.add(`navbar-${savedTheme}`);
}

toggleButton.addEventListener('click', () => {
  const currentTheme = bodyElement.classList.contains('light-theme') ? 'light-theme' : 'dark-theme';
  const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
  bodyElement.classList.remove(currentTheme);
  bodyElement.classList.add(newTheme);
  tableElements.forEach(table => {
    table.classList.remove(`table-${currentTheme}`);
    table.classList.add(`table-${newTheme}`);
  });
  headerElement.classList.remove(`header-${currentTheme}`);
  headerElement.classList.add(`header-${newTheme}`);
  navElement.classList.remove(`navbar-${currentTheme}`);
  navElement.classList.add(`navbar-${newTheme}`);

  // Сохранение выбранной темы в localStorage
  localStorage.setItem('theme', newTheme);
});
