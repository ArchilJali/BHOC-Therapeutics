#!/usr/bin/env python3
"""Read-only to GitHub: apply a minimal research CTA to a temporary main checkout,
then test exact source changes, site preservation and rendered breakpoints.
Never commit/push source, submit a contact form, or touch a private credential.
"""
import argparse
import datetime as dt
import functools
import http.server
import json
import subprocess
import threading
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

STAMP = lambda: dt.datetime.now(dt.timezone.utc).isoformat()
TARGET = "/contact/?interest=research&topic=oxygen-delivery-research"
HTML_LINK = '<a class="hero-research-link" href="/contact/?interest=research&amp;topic=oxygen-delivery-research">Discuss research collaboration →</a>'
# The compact mobile treatment preserves both current Science and Technology actions.
CSS_ADDITION = """
/* UX-01 trial only: accessible research link, evaluated against fresh main. */
.home-page .hero-copy .hero-research-link{
  display:inline-flex;align-items:center;min-height:44px;
  margin-top:7px;padding:8px 0;color:#0b377f;
  font-size:13px;font-weight:700;text-decoration:underline;text-underline-offset:3px;
}
.home-page .hero-copy .hero-research-link:focus-visible{
  outline:2px solid #d52321;outline-offset:3px;
}
@media(max-width:360px){
  .home-page .hero-copy .accent{margin-top:12px;margin-bottom:8px}
  .home-page .hero-copy .home-actions{margin-top:12px}
  .home-page .hero-copy .hero-research-link{margin-top:4px}
}
"""

def run_checks(source):
    commands = [
        ["node", "scripts/check_bhoc_content.mjs"],
        ["node", "scripts/check_site.mjs"],
        ["node", "--check", "navigation-context.js"],
        ["git", "diff", "--check"],
    ]
    results = []
    for cmd in commands:
        p = subprocess.run(cmd, cwd=source, text=True, capture_output=True, timeout=120)
        results.append({"command": " ".join(cmd), "exit": p.returncode,
                        "stdout_tail": p.stdout[-1800:], "stderr_tail": p.stderr[-1800:]})
    return results

def measure(page):
    return page.evaluate("""() => {
      const q = selector => [...document.querySelectorAll(selector)];
      const b = e => {if(!e)return null;const r=e.getBoundingClientRect();return {
        top:Math.round(r.top),bottom:Math.round(r.bottom),width:Math.round(r.width),
        height:Math.round(r.height),href:e.getAttribute('href'),text:e.textContent.trim()}};
      return {
        viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,
        h1_count:q('h1').length,
        research_links:q('.hero-copy .hero-research-link').map(b),
        science:b(q('.hero-copy a[href="/science/"]')[0]),
        technology:b(q('.hero-copy a[href="/technology/"]')[0]),
        image_count:document.images.length,
        broken_images:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),
        focusable:!!q('.hero-copy .hero-research-link')[0] && q('.hero-copy .hero-research-link')[0].tabIndex>=0
      }
    }""")

def audit_one(browser, base, out, tag):
    observations=[]
    for w,h in [(320,700),(390,844),(768,1024),(1440,1000)]:
        ctx=browser.new_context(viewport={"width":w,"height":h}, device_scale_factor=1,
                                is_mobile=w<=390,has_touch=w<=390)
        p=ctx.new_page()
        p.goto(base+"/",wait_until="networkidle",timeout=45000)
        p.wait_for_timeout(250)
        row=measure(p)
        row.update(width=w,height=h,stage=tag)
        p.screenshot(path=str(out/f"{tag}-{w}x{h}.png"))
        observations.append(row)
        ctx.close()
    return observations

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    source=Path(args.source).resolve()
    out=Path(args.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    htmlpath=source/"index.html"
    csspath=source/"homepage.css"
    original=htmlpath.read_text(encoding="utf-8")
    original_css=csspath.read_text(encoding="utf-8")
    sha=subprocess.check_output(["git","rev-parse","HEAD"],cwd=source,text=True).strip()
    status=subprocess.check_output(["git","status","--porcelain"],cwd=source,text=True).strip()
    if status:
        raise RuntimeError("Fresh main checkout is not clean; refusing to alter local source.")
    anchor='<a class="home-button" href="/technology/">Explore BHOC technology <span>→</span></a></div>'
    assert original.count(anchor)==1, "Current hero HTML differs; review before patch"
    assert 'hero-research-link' not in original and 'hero-research-link' not in original_css, "CTA already present"
    before=BeautifulSoup(original,"html.parser")
    assert len(before.select(".hero-copy h1"))==1
    old_href={a.get("href") for a in before.select("a[href]")}
    old_img=[(i.get("src"),i.get("alt"),i.get("width"),i.get("height")) for i in before.select("img")]
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(source))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    base="http://127.0.0.1:"+str(server.server_port)
    result={"checked_at":STAMP(),"source_main_sha":sha,"status":"started",
            "production_changes":0,"canonical_changes":0,"approved_text_removed":0}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            baseline=audit_one(browser,base,out,"before")
            patched=original.replace(anchor,anchor+HTML_LINK)
            htmlpath.write_text(patched,encoding="utf-8")
            csspath.write_text(original_css+"\n"+CSS_ADDITION,encoding="utf-8")
            after=BeautifulSoup(patched,"html.parser")
            assert len(after.select(".hero-copy .hero-research-link"))==1
            assert len(after.select("h1"))==len(before.select("h1"))
            assert [(i.get("src"),i.get("alt"),i.get("width"),i.get("height")) for i in after.select("img")]==old_img
            assert old_href.issubset({a.get("href") for a in after.select("a[href]")})
            assert after.select_one(".hero-copy .hero-research-link").get("href")==TARGET
            patched_rows=audit_one(browser,base,out,"after")
            for prev,cur in zip(baseline,patched_rows):
                assert cur["h1_count"]==prev["h1_count"]==1
                assert cur["image_count"]==prev["image_count"]
                assert not cur["broken_images"], (cur["width"],cur["broken_images"])
                assert cur["scrollWidth"]<=cur["viewport"]+1,(cur["width"],cur["scrollWidth"])
                assert len(cur["research_links"])==1
                assert cur["research_links"][0]["height"]>=44
                assert cur["focusable"]
                assert cur["science"]["href"]==prev["science"]["href"]=="/science/"
                assert cur["technology"]["href"]==prev["technology"]["href"]=="/technology/"
                # Existing action positions must be stable except the intended 320px compact spacing.
                tolerance=20 if cur["width"]==320 else 3
                assert abs(cur["science"]["top"]-prev["science"]["top"])<=tolerance
                assert abs(cur["technology"]["top"]-prev["technology"]["top"])<=tolerance
                if cur["width"] in (320,390):
                    assert cur["research_links"][0]["bottom"]<=cur["height"]-15,\
                        "Research CTA is too close to the viewport bottom"
            # Verify the actual source URL preselects research and shows the topic, no submission.
            ctx=browser.new_context(viewport={"width":390,"height":844})
            contact=ctx.new_page()
            response=contact.goto(base+TARGET,wait_until="networkidle",timeout=45000)
            selection=contact.locator('select[name="area"]').input_value()
            note=contact.locator("[data-enquiry-topic]").inner_text()
            assert response.status==200
            assert selection=="Research collaboration",(selection,note)
            assert note=="Topic: Oxygen delivery research",note
            result["contact_test"]={"http":response.status,"interest":selection,"topic":note,
                                    "form_submitted":False}
            ctx.close()
            browser.close()
        tests=run_checks(source)
        result["checks"]=tests
        assert all(x["exit"]==0 for x in tests),"Repository preservation check failed"
        diff=subprocess.run(["git","diff","--","index.html","homepage.css"],cwd=source,
                            text=True,capture_output=True,check=True).stdout
        (out/"preview-source.diff").write_text(diff,encoding="utf-8")
        result["screenshots"]=8
        result["baseline"]=baseline
        result["patched"]=patched_rows
        result["status"]="passed"
        print("UX01_SOURCE_PATCH_TEST="+json.dumps(
            {"status":result["status"],"source_main_sha":sha,
             "screens":[{"width":x["width"],"h1":x["h1_count"],
                         "research_bottom":x["research_links"][0]["bottom"],
                         "viewport_height":x["height"]} for x in patched_rows],
             "checks":[{"command":x["command"],"exit":x["exit"]} for x in tests]},
            ensure_ascii=False))
    except Exception as exc:
        result["status"]="failed"
        result["error"]=str(exc)
        print("UX01_SOURCE_PATCH_TEST_FAILED="+str(exc))
        raise
    finally:
        (out/"result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        server.shutdown()
        # Ephemeral GitHub Actions worktree only; do not create a commit or alter main remotely.

if __name__=="__main__":
    main()
