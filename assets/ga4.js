(() => {
  'use strict';
  const GA4_MEASUREMENT_ID = '';
  if (!GA4_MEASUREMENT_ID) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_MEASUREMENT_ID);
  document.head.appendChild(s);
  window.gtag('js', new Date());
  window.gtag('config', GA4_MEASUREMENT_ID);
})();
