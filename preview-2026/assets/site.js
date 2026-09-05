(() => {
  const button = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-primary-nav]');
  if (button && nav) {
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('open', !open);
    });
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) {
        button.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        button.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
        button.focus();
      }
    });
  }

  document.querySelectorAll('[data-current-year]').forEach(el => {
    el.textContent = String(new Date().getFullYear());
  });
})();
