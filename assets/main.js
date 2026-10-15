(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      menuButton.setAttribute('aria-label', open ? 'Open navigation' : 'Close navigation');
      nav.classList.toggle('nav-open', !open);
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      nav.classList.remove('nav-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Open navigation');
    }));
  }

  const search = document.getElementById('paper-search');
  const year = document.getElementById('year-filter');
  const area = document.getElementById('area-filter');
  const count = document.getElementById('paper-count');
  const empty = document.getElementById('no-papers');
  const reset = document.getElementById('reset-filters');
  if (!search || !year || !area || !count || !empty) return;
  const papers = Array.from(document.querySelectorAll('#publication-list .paper'));
  const apply = () => {
    const q = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const paper of papers) {
      const match = (!q || (paper.dataset.search || '').includes(q)) &&
        (year.value === 'all' || year.value === paper.dataset.year) &&
        (area.value === 'all' || area.value === paper.dataset.area);
      paper.hidden = !match;
      if (match) visible++;
    }
    count.textContent = `Showing ${visible} of ${papers.length} publications`;
    empty.hidden = visible !== 0;
  };
  [search, year, area].forEach(el => el.addEventListener(el === search ? 'input' : 'change', apply));
  if (reset) reset.addEventListener('click', () => { search.value=''; year.value='all'; area.value='all'; apply(); search.focus(); });
  apply();
})();
