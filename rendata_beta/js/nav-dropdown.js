/* Dropdown nav: click toggle (móvil) + clic-fuera cierra. Hover sigue funcionando vía CSS. */
(function () {
  function init() {
    var dropdowns = document.querySelectorAll('.nav-dropdown');
    if (!dropdowns.length) return;
    dropdowns.forEach(function (dd) {
      var btn = dd.querySelector('.nav-drop-btn');
      if (!btn) return;
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var wasOpen = dd.classList.contains('open');
        document.querySelectorAll('.nav-dropdown.open').forEach(function (o) { o.classList.remove('open'); });
        if (!wasOpen) dd.classList.add('open');
      });
    });
    document.addEventListener('click', function (e) {
      document.querySelectorAll('.nav-dropdown.open').forEach(function (o) {
        if (!o.contains(e.target)) o.classList.remove('open');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.nav-dropdown.open').forEach(function (o) { o.classList.remove('open'); });
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
