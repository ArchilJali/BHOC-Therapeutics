"""Owner-only UX experiment: inject a candidate research link in an isolated browser.
No source/site mutation, publication, form submission, cookies or accounts.
The base page remains https://bhoctherapeutics.com/; this is NOT a deployed preview.
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://bhoctherapeutics.com"
TARGET = "/contact/?interest=research&topic=oxygen-delivery-research"
LABEL = "Discuss research collaboration"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

MEASURE = r"""() => {
  const pick = sel => document.querySelector(sel);
  const rect = el => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return {
      text: (el.textContent || '').trim().slice(0, 95),
      top: Math.round(r.top), bottom: Math.round(r.bottom),
      width: Math.round(r.width), height: Math.round(r.height),
      display: style.display, visibility: style.visibility,
      href: el.getAttribute('href')
    };
  };
  const buttons = [...document.querySelectorAll('.hero-copy .home-actions a')];
  return {
    viewport_width: innerWidth, viewport_height: innerHeight,
    scroll_width: document.documentElement.scrollWidth,
    h1: rect(pick('main h1')),
    original_actions: buttons.map(rect),
    proposed_link: rect(pick('.hero-research-link')),
    h1_count: document.querySelectorAll('h1').length,
    image_count: document.querySelectorAll('img').length,
    anchor_count: document.querySelectorAll('a[href]').length,
    broken_images: [...document.images].filter(x => x.complete && !x.naturalWidth).map(x => x.getAttribute('src'))
  };
}"""

INJECT = r"""() => {
  const group = document.querySelector('.hero-copy .home-actions');
  if (!group || group.querySelectorAll('a').length !== 2) throw Error('Original two education actions changed; stop');
  if (document.querySelector('.hero-research-link')) throw Error('Prototype link already present');
  const link = document.createElement('a');
  link.className = 'hero-research-link';
  link.href = '/contact/?interest=research&topic=oxygen-delivery-research';
  link.textContent = 'Discuss research collaboration →';
  group.insertAdjacentElement('afterend', link);
  const css = document.createElement('style');
  css.id = 'owner-ux-cta-preview-only';
  css.textContent = [
    '.hero-copy .hero-research-link{display:inline-flex;align-items:center;min-height:44px;',
    'margin-top:7px;padding:8px 0;font-size:13px;font-weight:700;',
    'color:#0b377f;text-decoration:underline;text-underline-offset:3px;}',
    '.hero-copy .hero-research-link:focus-visible{outline:2px solid #d52321;outline-offset:3px;}'
  ].join('');
  document.head.appendChild(css);
}"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="output/research-cta-prototype")
    p.add_argument("--source", default="source")
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=args.source, text=True
    ).strip()
    result = {
        "kind": "ephemeral_dom_injection_not_deployed",
        "source_main_sha": source_sha,
        "checked_at": now(),
        "target_url": BASE + TARGET,
        "public_changes": 0,
        "viewport_tests": [],
        "contact_preselection": {},
        "limitations": [
            "DOM injection only; not a preview-branch HTML/CSS implementation.",
            "Screenshot evidence does not establish conversion improvements, indexing, AEO citations or field Core Web Vitals.",
            "No form was filled or submitted; no private account was used.",
            "All existing copy, layout assets, approved sources and links were left unchanged on the server."
        ]
    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width, height in [(320, 700), (390, 844), (1440, 1000)]:
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()
            record = {"width": width, "height": height}
            try:
                response = page.goto(BASE + "/", wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(900)
                record["http"] = response.status if response else None
                before = page.evaluate(MEASURE)
                page.screenshot(path=str(out / f"home-before-{width}x{height}.png"))
                page.evaluate(INJECT)
                after = page.evaluate(MEASURE)
                page.screenshot(path=str(out / f"home-prototype-{width}x{height}.png"))
                locator = page.locator(".hero-copy .hero-research-link")
                locator.focus()
                focusable = page.evaluate(
                    "() => document.activeElement?.classList.contains('hero-research-link') === true"
                )
                a = before["original_actions"]
                b = after["original_actions"]
                original_positions_unchanged = len(a) == len(b) == 2 and all(
                    abs(a[i]["top"] - b[i]["top"]) <= 2 and
                    abs(a[i]["bottom"] - b[i]["bottom"]) <= 2
                    for i in range(2)
                )
                link = after["proposed_link"]
                record.update(
                    baseline=before, prototype=after,
                    focusable=focusable,
                    original_actions_unchanged=original_positions_unchanged,
                    proposed_link_in_first_viewport=bool(link and link["bottom"] <= height),
                    original_actions_in_first_viewport=all(x["bottom"] <= height for x in b),
                    no_horizontal_overflow=after["scroll_width"] <= after["viewport_width"] + 1,
                    h1_preserved=before["h1_count"] == after["h1_count"] == 1,
                    only_one_link_added=after["anchor_count"] == before["anchor_count"] + 1,
                    images_unchanged=after["image_count"] == before["image_count"],
                    target_exact=link and link["href"] == TARGET,
                )
                record["basic_safety_passed"] = all(record[x] for x in [
                    "focusable", "original_actions_unchanged", "no_horizontal_overflow",
                    "h1_preserved", "only_one_link_added", "images_unchanged", "target_exact"
                ])
            except Exception as exc:
                record["error"] = str(exc)
            finally:
                result["viewport_tests"].append(record)
                page.close()
                context.close()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        try:
            resp = page.goto(BASE + TARGET, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(900)
            a = page.locator('form[data-form-endpoint] select[name="area"]')
            selected = a.input_value() if a.count() else None
            topic = page.locator("[data-enquiry-topic]")
            note = topic.first.inner_text() if topic.count() else None
            result["contact_preselection"] = {
                "http": resp.status if resp else None,
                "form_present": bool(a.count()),
                "selected_interest": selected,
                "topic_note": note,
                "verified": selected == "Research collaboration" and note == "Topic: Oxygen delivery research",
                "submitted": False
            }
            page.screenshot(path=str(out / "contact-research-preselection-390x844.png"))
        except Exception as exc:
            result["contact_preselection"] = {"error": str(exc), "verified": False, "submitted": False}
        finally:
            page.close()
            context.close()
            browser.close()
    mobile = [x for x in result["viewport_tests"] if x["width"] < 500]
    if all(x.get("basic_safety_passed") and x.get("proposed_link_in_first_viewport") and x.get("original_actions_in_first_viewport") for x in mobile) and result["contact_preselection"].get("verified"):
        result["decision"] = "option_a_eligible_for_source_preview_and_owner_review"
    else:
        result["decision"] = "option_a_not_yet_eligible_review_fallback_in_partners"
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({
        "checked_at": result["checked_at"],
        "source_main_sha": source_sha,
        "decision": result["decision"],
        "viewport_summary": [
            {
                "width": x["width"], "height": x["height"],
                "link_above_fold": x.get("proposed_link_in_first_viewport"),
                "original_above_fold": x.get("original_actions_in_first_viewport"),
                "safety_passed": x.get("basic_safety_passed"),
                "error": x.get("error")
            } for x in result["viewport_tests"]
        ],
        "contact": result["contact_preselection"],
        "production_changed": False
    }, ensure_ascii=False))
    if any(x.get("error") for x in result["viewport_tests"]) or not result["contact_preselection"].get("verified"):
        raise SystemExit("Preview experiment incomplete: inspect result.json and screenshots")

if __name__ == "__main__":
    main()
