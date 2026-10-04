(function () {
  var root = document.documentElement, saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  if (saved) root.setAttribute('data-theme', saved);

  document.addEventListener('DOMContentLoaded', function () {
    var $ = function (s) { return document.querySelector(s); };

    var themeBtn = $('#theme');
    if (themeBtn) themeBtn.addEventListener('click', function () {
      var dark = matchMedia('(prefers-color-scheme: dark)').matches;
      var cur = root.getAttribute('data-theme') || (dark ? 'dark' : 'light');
      var next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });

    document.querySelectorAll('[data-copy-text],[data-copy-fetch]').forEach(function (b) {
      var label = b.textContent;
      b.addEventListener('click', function () {
        var get = b.dataset.copyFetch
          ? fetch(b.dataset.copyFetch).then(function (r) { return r.text(); })
          : Promise.resolve(b.dataset.copyText);
        get.then(function (t) { return navigator.clipboard.writeText(t); }).then(function () {
          b.textContent = 'Copied'; b.classList.add('copied');
          setTimeout(function () { b.textContent = label; b.classList.remove('copied'); }, 1600);
        });
      });
    });

    var url = $('#url');
    if (url) url.addEventListener('focus', function () { this.select(); });

    document.querySelectorAll('form[data-confirm]').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        if (!confirm(f.dataset.confirm)) e.preventDefault();
      });
    });

    var ed = $('#editor');
    if (ed) {
      var counter = $('#counter'), max = parseInt(counter.dataset.maxKb, 10) * 1024;
      var update = function () {
        var n = new Blob([ed.value]).size;
        counter.textContent = ed.value.length + ' characters · ' + (n / 1024).toFixed(1) + ' KB';
        counter.style.color = n > max ? 'var(--danger)' : '';
      };
      ed.addEventListener('input', update); update();
      ed.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') ed.form.requestSubmit();
      });
      ed.addEventListener('dragover', function (e) { e.preventDefault(); });
      ed.addEventListener('drop', function (e) {
        var f = e.dataTransfer.files[0]; if (!f) return;
        e.preventDefault();
        f.text().then(function (t) { ed.value = t; update(); });
      });
    }
  });
})();
