(() => {
  'use strict';
  // Preserve campaign context for a submitted enquiry even before GA4 is configured.
  // Only campaign labels and page paths are retained, for the current browser tab.
  if (window.BHOCLeadContext) return;
  const storageKey = 'bhoc-enquiry-context-v1';
  const campaignKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const clean = value => typeof value === 'string' && !value.includes('@')
    ? value.replace(/[\u0000-\u001f\u007f]/g, '').slice(0, 120) : '';
  const pagePath = window.location.origin + window.location.pathname;
  const query = new URLSearchParams(window.location.search);
  let previous = {};
  try { previous = JSON.parse(window.sessionStorage.getItem(storageKey) || '{}') || {}; } catch (_) {}
  const context = {};
  for (const key of campaignKeys) if (clean(previous[key])) context[key] = clean(previous[key]);
  const campaign = {};
  for (const key of campaignKeys) if (clean(query.get(key))) campaign[key] = clean(query.get(key));
  let referrerHost = '';
  try { referrerHost = new URL(document.referrer).hostname; } catch (_) {}
  const newCampaign = Object.keys(campaign).length > 0;
  if (newCampaign) {
    for (const key of campaignKeys) delete context[key];
    Object.assign(context, campaign);
  }
  context.landing_page = newCampaign || !previous.landing_page ? pagePath : String(previous.landing_page).slice(0, 300);
  context.referring_site = newCampaign || !previous.landing_page ? referrerHost : clean(previous.referring_site);
  try { window.sessionStorage.setItem(storageKey, JSON.stringify(context)); } catch (_) {}

  const topics = {
    'oxygen-delivery-research': 'Oxygen delivery research',
    'investment-licensing': 'Investment and licensing',
    'regional-partnership': 'Regional partnership',
    'manufacturing-regulatory': 'Manufacturing and regulatory collaboration',
    'veterinary-research': 'Veterinary research collaboration',
    'feline-transfusion': 'Feline transfusion evidence and research',
    'organ-perfusion': 'Organ perfusion research'
  };
  const interests = {
    research: ['Research collaboration', 'Veterinary research', 'Transplant research collaboration'],
    clinical: ['Clinical translation', 'Clinical collaboration'],
    partnership: ['Strategic partnership'],
    investment: ['Investment'],
    manufacturing: ['Manufacturing and regulatory'],
    perfusion: ['Organ perfusion and preservation']
  };
  const topic = topics[query.get('topic')] || '';
  const submitted = new WeakSet();
  const formId = window.location.hostname.replaceAll('.', '_') + '_contact';
  const setHidden = (form, name, value) => {
    if (!value) return;
    let input = form.querySelector('input[name="' + name + '"]');
    if (!input) {
      input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      form.appendChild(input);
    }
    input.value = value;
  };
  const prepare = () => {
    document.querySelectorAll('form[data-form-endpoint]').forEach(form => {
      for (const key of campaignKeys) setHidden(form, key, context[key]);
      setHidden(form, 'source_landing_page', context.landing_page);
      setHidden(form, 'source_referring_site', context.referring_site);
      setHidden(form, 'enquiry_topic', topic);
      const area = form.querySelector('select[name="area"]');
      const choices = interests[query.get('interest')] || [];
      if (area) {
        const match = choices.find(value => Array.from(area.options).some(option => option.value === value));
        if (match) area.value = match;
      }
      if (topic && !form.querySelector('[data-enquiry-topic]')) {
        const note = document.createElement('p');
        note.className = 'form-note bhoc-contact-note contact-full';
        note.style.gridColumn = '1 / -1';
        note.dataset.enquiryTopic = '';
        note.textContent = 'Topic: ' + topic;
        form.prepend(note);
      }
    });
  };
  window.BHOCLeadContext = {
    submitted(form) {
      if (submitted.has(form)) return;
      submitted.add(form);
      const details = {
        form_id: formId,
        lead_type: form.querySelector('select[name="area"]')?.value || 'Enquiry',
        enquiry_topic: topic
      };
      // Never send the contact's name, email, organisation or message to analytics.
      try {
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', details);
      } catch (_) { /* A tracking failure must not turn an accepted enquiry into an error. */ }
      window.dispatchEvent(new CustomEvent('bhoc:lead-submitted', {detail: details}));
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', prepare, {once: true});
  else prepare();

  // Supply only a real, verified BHOC web-stream ID. Empty deliberately means off.
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
