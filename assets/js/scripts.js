(function () {
  var body = document.body;
  var menuTrigger = document.querySelector('#toggle-menu-main-mobile');
  var menuContainer = document.querySelector('#menu-main-mobile');
  var hamburger = document.querySelector('.hamburger');
  if (!menuTrigger || !menuContainer || !hamburger) return;

  function setOpen(open) {
    menuContainer.classList.toggle('open', open);
    hamburger.classList.toggle('is-active', open);
    body.classList.toggle('lock-scroll', open);
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  menuTrigger.addEventListener('click', function () {
    setOpen(!menuContainer.classList.contains('open'));
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menuContainer.classList.contains('open')) {
      setOpen(false);
      hamburger.focus();
    }
  });
})();
