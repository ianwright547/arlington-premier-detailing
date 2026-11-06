/* Quote form. Leads go nowhere silently: with no WEBHOOK set, the request opens
   in the customer's email app, addressed to the shop.
   To connect a CRM, paste its webhook URL into WEBHOOK below. */
(function () {
  var WEBHOOK = '';
  var EMAIL = 'support@tabmotorsarlington.com';
  var form = document.getElementById('quoteForm');
  if (!form) return;
  var state = { vehicle: '', details: '', service: '' };
  var history = ['1'];
  var bar = document.getElementById('qfProgressBar');
  var txt = document.getElementById('qfProgressText');

  function show(step, back) {
    form.querySelectorAll('.qf-step').forEach(function (s) {
      s.classList.toggle('qf-step-active', s.getAttribute('data-step') === step);
    });
    if (!back) history.push(step);
    var n = step === 'success' ? 3 : Number(step);
    if (bar) bar.style.width = (n / 3) * 100 + '%';
    if (txt) txt.textContent = step === 'success' ? 'Done' : 'Step ' + n + ' of 3';
  }
  show('1', true);

  var next = document.getElementById('qfStep1Next');
  form.querySelectorAll('[data-type]').forEach(function (b) {
    b.addEventListener('click', function () {
      form.querySelectorAll('[data-type]').forEach(function (x) { x.classList.remove('qf-choice-selected', 'selected'); });
      b.classList.add('qf-choice-selected', 'selected');
      state.vehicle = b.getAttribute('data-type');
      next.disabled = false;
    });
  });
  next.addEventListener('click', function () {
    state.details = document.getElementById('qfVehicleDetails').value.trim();
    show('2');
  });
  form.querySelectorAll('[data-service]').forEach(function (b) {
    b.addEventListener('click', function () { state.service = b.getAttribute('data-service'); show('3'); });
  });
  form.querySelectorAll('.qf-back').forEach(function (b) {
    b.addEventListener('click', function () {
      history.pop();
      show(history[history.length - 1], true);
    });
  });

  document.getElementById('qfSubmit').addEventListener('click', function () {
    var nameEl = document.getElementById('qfName');
    var phoneEl = document.getElementById('qfPhone');
    var name = nameEl.value.trim();
    var phone = phoneEl.value.trim();
    if (phone.replace(/\D/g, '').length < 10) {
      phoneEl.focus();
      phoneEl.style.borderColor = '#ff5a5a';
      return;
    }
    if (WEBHOOK) {
      var fd = new FormData();
      fd.append('name', name); fd.append('phone', phone); fd.append('vehicle', state.vehicle);
      fd.append('details', state.details); fd.append('service', state.service);
      fd.append('source', location.pathname);
      fetch(WEBHOOK, { method: 'POST', body: fd, mode: 'no-cors' }).catch(function () {});
      document.getElementById('qfSuccessText').textContent = 'Thanks, we have your request and will follow up during shop hours.';
    } else {
      var subject = 'Detailing quote request: ' + state.service;
      var body = 'Name: ' + name + '\nPhone: ' + phone + '\nVehicle: ' + state.vehicle +
        (state.details ? ' (' + state.details + ')' : '') + '\nPackage: ' + state.service;
      window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    }
    show('success');
  });
})();
