// Sticky nav
var nav = document.getElementById('nav');
window.addEventListener('scroll', function () { nav.classList.toggle('scrolled', window.scrollY > 50); });

// Scroll animations
if ('IntersectionObserver' in window) {
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) { if (entry.isIntersecting) entry.target.classList.add('visible'); });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.fade-up').forEach(function (el) { observer.observe(el); });
} else {
  document.querySelectorAll('.fade-up').forEach(function (el) { el.classList.add('visible'); });
}

// Hamburger menu
(function () {
  var btn = document.getElementById('navMenuToggle');
  var menu = document.getElementById('navMenu');
  if (!btn || !menu) return;
  function close() { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  var c = document.getElementById('navMenuClose');
  if (c) c.addEventListener('click', close);
  menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', close); });
  menu.querySelectorAll('.nav-submenu-toggle').forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.stopPropagation();
      t.setAttribute('aria-expanded', t.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
    });
  });
})();

// Sticky mobile action bar
(function () {
  var bar = document.createElement('div');
  bar.className = 'mobile-bar';
  bar.innerHTML = '<a class="mb-call">Call</a>' +
    '<a class="mb-text" href="https://www.google.com/maps/search/?api=1&query=TAB+Motors+Arlington+4035+Old+Dominion+Dr+Arlington+VA+22207" target="_blank" rel="noopener">Directions</a>' +
    '<a class="mb-quote" href="/contact/#quote">Quote</a>';
  bar.querySelector('.mb-call').href = nav.querySelector('.btn-nav').href;
  document.body.appendChild(bar);
})();
