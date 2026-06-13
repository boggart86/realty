document.addEventListener('DOMContentLoaded', () => {
  // Favorite toggle on catalog page (AJAX)
  document.querySelectorAll('.btn-fav').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const pk = btn.dataset.pk;
      const url = typeof TOGGLE_URLS !== 'undefined' && TOGGLE_URLS[pk];
      if (!url) return;

      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
      });
      const data = await res.json();
      const icon = btn.querySelector('i');

      if (data.is_favorite) {
        btn.classList.add('active');
        icon.className = 'bi bi-heart-fill';
        btn.title = 'Убрать из избранного';
      } else {
        btn.classList.remove('active');
        icon.className = 'bi bi-heart';
        btn.title = 'В избранное';
      }
    });
  });

  // Carousel thumb sync
  const carousel = document.getElementById('photoCarousel');
  if (carousel) {
    carousel.addEventListener('slid.bs.carousel', (e) => {
      document.querySelectorAll('.thumb').forEach((t, i) => {
        t.classList.toggle('active', i === e.to);
      });
    });
  }
});
