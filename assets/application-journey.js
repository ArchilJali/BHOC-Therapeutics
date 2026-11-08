/* Context navigation for Applications and its clinical reading routes. */
(() => {
  'use strict';
  if (!document.body.classList.contains('application-journey')) return;
  const clinicalRoot = '/evidence/library/clinical/';
  const currentPath = location.pathname.replace(/\/index\.html$/, '/');
  const labels = {
    'sickle-cell-matched-blood-oxygen-delivery.html': 'SCA / SCD',
    'sickle-cell-transfusion-compatibility.html': 'Transfusion compatibility',
    'prehospital-ems.html': 'Prehospital EMS',
    'pph-humanitarian-problem.html': 'Postpartum hemorrhage',
    'blood-collection-capacity-available-blood.html': 'Blood availability'
  };

  function enhance() {
    if (document.body.dataset.journeyReady === 'true') return;
    document.querySelector('.bhoc-shell-local-nav')?.remove();
    document.querySelector('.bhoc-shell-page-notes')?.remove();
    document.querySelectorAll('.bhoc-evidence-links').forEach(nav => nav.remove());

    const trail = document.querySelector('.bhoc-shell-trail');
    if (currentPath.startsWith(clinicalRoot)) {
      const link = [...(trail?.querySelectorAll('a') || [])].find(a => new URL(a.href).pathname.replace(/\/index\.html$/, '/') === clinicalRoot);
      if (link) { link.textContent = 'Clinical evidence'; link.title = 'Clinical evidence'; }
      const current = trail?.querySelector('[aria-current="page"]');
      const label = currentPath === clinicalRoot ? 'Clinical evidence' : labels[currentPath.split('/').pop()];
      if (current && label) { current.textContent = label; current.title = label; }
    }

    // The shared footer keeps all site-wide destinations available. Fold the
    // secondary header resources so the reader reaches this page's purpose first.
    const utility = document.querySelector('.bhoc-shell-utility');
    const resources = utility?.querySelector('.bhoc-shell-utility-inner');
    if (utility && resources) {
      const details = document.createElement('details');
      details.className = 'journey-network bhoc-shell-wrap';
      const summary = document.createElement('summary');
      summary.textContent = 'BHOC resources';
      resources.classList.remove('bhoc-shell-wrap');
      details.append(summary, resources);
      utility.replaceChildren(details);
    }

    const contents = document.querySelector('.journey-contents');
    if (contents) {
      const narrow = matchMedia('(max-width: 760px)');
      const reset = () => { contents.open = !narrow.matches; };
      reset();
      narrow.addEventListener('change', reset);
      contents.addEventListener('click', event => {
        if (narrow.matches && event.target.closest('a[href^="#"]')) contents.open = false;
      });
    }

    // Keep a direct return to an application on its selected card after the
    // shared header and local navigation have finished their layout changes.
    const alignEntry = () => {
      let id = '';
      try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) {}
      const target = id && document.getElementById(id);
      if (target) target.scrollIntoView({block: 'start', inline: 'nearest', behavior: 'instant'});
    };
    if (document.readyState === 'complete') requestAnimationFrame(alignEntry);
    else window.addEventListener('load', () => requestAnimationFrame(alignEntry), {once: true});
    document.body.dataset.journeyReady = 'true';
  }

  // The publishing workflow normalizes script order. Wait for the shared shell
  // instead of depending on which deferred file appears last in the document.
  if (document.body.classList.contains('bhoc-shell-ready')) enhance();
  else {
    const observer = new MutationObserver(() => {
      if (!document.body.classList.contains('bhoc-shell-ready')) return;
      observer.disconnect();
      enhance();
    });
    observer.observe(document.body, {attributes: true, attributeFilter: ['class']});
  }
})();
