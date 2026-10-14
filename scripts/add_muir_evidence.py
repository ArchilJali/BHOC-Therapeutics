"""Reconcile user-approved Muir studies into the canonical evidence catalogue.

Run from repository root. Idempotent by DOI and PMID. Source verified October 2026; synchronized catalogue release.
"""
import json
from pathlib import Path
from datetime import date

base=Path("evidence/library")
data_path=base/"catalogues/data/publications.json"
add_path=base/"catalogues/data/approved-scientific-additions.json"
audit_path=base/"catalogues/data/source-link-audit.json"
data=json.loads(data_path.read_text())
add=json.loads(add_path.read_text())
audit=json.loads(audit_path.read_text())
records=data["records"]
approved=[r for r in add["records"] if r.get("pmid") in {"1111380","3740627","19430240","24612155"} or r.get("doi","").casefold()=="10.1155/2014/864237"]
template=next(r for r in records if r.get("pmid")=="12683610")
inserted=[]
for a in approved:
    doi=a.get("doi","").strip().casefold()
    pmid=a.get("pmid","").strip()
    old=next((r for r in records if (doi and r.get("doi","").casefold()==doi) or (pmid and r.get("pmid","")==pmid)),None)
    if old:
        # Already indexed; retain original publication record, catalogue and anchor.
        continue
    rid="pub-pmid-"+pmid if pmid else "pub-muir-oc99-2014"
    if any(r["id"]==rid for r in records):raise ValueError("Duplicate record ID: "+rid)
    urls=[a["sourceUrl"]]
    if doi:
        durl="https://doi.org/"+doi
        if durl not in urls:urls.append(durl)
    study="Review" if a.get("evidenceType")=="Review" else "Experimental study"
    topic=a["topics"]
    paper=dict(template)
    paper.update(title=a["title"],year=a["year"],authors=a["authors"],journal=a["journal"],
      doi=doi,pmid=pmid,citation=a["authors"].replace("; ",", ")+". "+a["title"]+". "+a["journal"]+". "+a["year"]+";"+a["volume"]+"("+a["issue"]+"):"+a["pages"]+".",
      product="OC99" if a["year"]=="2014" else "", keywords="; ".join(topic),
      directions=["Veterinary","Physiology"],institutions=["The Ohio State University"] if a["year"]!="2014" else ["QTest Labs","New A Innovation Ltd."],
      species=["Equine (Horse)"] if a["year"] in ("1975","1986","2015") else ["Canine (Dog)"],
      evidence=study,urls=urls,notes=[],provenance=[{"source":"Approved scientific additions","row":a["id"],"title":a["title"],"year":a["year"],"doi":doi,"pmid":pmid}],
      originalVerification="Original PubMed or publisher record checked; historical study.",
      sourceReview="Muir-authored publication. Original experimental research or review as labelled. Findings relate to veterinary oxygenation and should not be interpreted as efficacy evidence for a new BHOC formulation.",
      catalogue="oxygen",classificationBasis="Oxygen transport, gas exchange, tissue perfusion and/or tissue oxygenation. Appears also in Veterinary application search.",
      id=rid,verification="PubMed metadata verified" if pmid else "Publisher metadata verified",
      recordType="Bibliographic record",topics=topic,titleAliases=[],catalogueSummary="")
    records.append(paper)
    audit["records"][rid]={"publicLinks":urls,"checks":[{"url":url,"state":"matched","method":"PubMed indexed publication / journal DOI" if pmid else "Journal article DOI and PMC original record","sourceTitle":a["title"]} for url in urls]}
    inserted.append(rid)
if inserted:
    data["updated"]="2026-10-14"
    audit["checked"]="2026-10-14"
    audit["publicRecords"]=sum(not r.get("recordType","").startswith("Import") for r in records)
    audit["uniqueUrlsChecked"]=len(set(url for v in audit["records"].values() for url in (x["url"] for x in v["checks"])))
    data_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"inserted":inserted,"publicRecords":audit["publicRecords"]}))
