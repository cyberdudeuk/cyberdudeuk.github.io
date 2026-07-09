const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('#nav-links');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!isOpen));
    navLinks.classList.toggle('open', !isOpen);
  });
}

const filter = document.querySelector('#toolkit-filter');
const items = Array.from(document.querySelectorAll('.toolkit-item'));

if (filter) {
  filter.addEventListener('change', (event) => {
    const value = event.target.value;
    items.forEach((item) => {
      const visible = value === 'all' || item.dataset.category === value;
      item.classList.toggle('hidden', !visible);
    });
  });
}

const accordion = document.querySelector('[data-accordion]');

if (accordion) {
  const buttons = Array.from(accordion.querySelectorAll('button'));
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const isExpanded = button.getAttribute('aria-expanded') === 'true';

      buttons.forEach((otherButton) => {
        const otherPanel = document.getElementById(otherButton.getAttribute('aria-controls'));
        otherButton.setAttribute('aria-expanded', 'false');
        if (otherPanel) otherPanel.hidden = true;
      });

      button.setAttribute('aria-expanded', String(!isExpanded));
      if (panel) panel.hidden = isExpanded;
    });
  });
}
