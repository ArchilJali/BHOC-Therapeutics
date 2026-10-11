"""Check original spreadsheet rows against imports and retained provenance."""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'evidence/library'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def clean(value):
    return html.unescape(re.sub('<[^>]+>', '', str(value or ''))).strip()

def sheet(path, name):
    with zipfile.ZipFile(path) as z:
        shared = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in z.namelist() else []
        rel = {x.get('Id'): x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        workbook = ET.fromstring(z.read('xl/workbook.xml'))
        selected = next(x for x in workbook.find('s:sheets', NS) if x.get('name') == name)
        target = rel[selected.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
        target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
        rows = []
        for row in ET.fromstring(z.read(target)).findall('.//s:sheetData/s:row', NS):
            cells = {}
            for cell in row:
                column = re.sub(r'\d+', '', cell.get('r'))
                value = cell.find('s:v', NS)
                cells[column] = shared[int(value.text)] if cell.get('t') == 's' else ''.join(cell.find('s:is', NS).itertext()) if cell.get('t') == 'inlineStr' else value.text if value is not None else ''
            rows.append(cells)
        return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=Path, required=True)
    args = parser.parse_args()
    records = json.loads((BASE / 'catalogues/data/publications.json').read_text())['records']
    indexed = {}
    for record in records:
        for source in record['provenance']:
            key = (source['source'], str(source['row']))
            assert key not in indexed, f'Repeated source row: {key}'
            indexed[key] = (record, source)
    inputs = []
    def check(source, rows, title_key, row_ids):
        expected = {(source, str(row_id)): clean(row[title_key]) for row_id, row in zip(row_ids, rows)}
        assert len(expected) == len(rows)
        actual = {key: clean(value[1]['title']) for key, value in indexed.items() if key[0] == source}
        assert actual == expected, f'Missing or changed source rows: {source}'
        inputs.append({'source': source, 'rows': len(rows), 'retainedRows': len(actual), 'missingRows': 0})
    for source, filename, title in [
        ('Master Catalogue', 'master-extracted.json', 'Title'),
        ('Oxygen Master', 'BHOC_Oxygen_Master_243_records.json', 'title'),
    ]:
        rows = json.loads((args.input_dir / filename).read_text())
        check(source, rows, title, range(2, len(rows) + 2))
    for source, filename in [
        ('Veterinary base', 'veterinary/Vet-publications.json'),
        ('Human Use', 'human/BHOC-Human-publications.json'),
        ('Transplant', 'transplant/Transplant-publications.json'),
        ('Veterinary curated additions', 'veterinary/Vet-publications-curation.json'),
        ('transplant/related/data/related-evidence.json', 'transplant/related/data/related-evidence.json'),
        ('transplant/Transplant-relevant-evidence.json', 'transplant/Transplant-relevant-evidence.json'),
    ]:
        data = json.loads((BASE / filename).read_text())
        rows = data if isinstance(data, list) else data.get('records', data.get('additions'))
        if source == 'Veterinary base':
            overrides = json.loads((BASE / 'veterinary/Vet-publications-curation.json').read_text())['overrides']
            rows = [{**row, **overrides.get(row['id'], {})} for row in rows]
        check(source, rows, 'title', [row['id'] for row in rows])
    workbooks = []
    for filename, name, source, column in [
        ('HBOC_Publications_by_Direction_Updated_2026-10-11.xlsx', 'Master Catalogue', 'Master Catalogue', 'B'),
        ('Oxygen_MASTER_ONE_PUBLICATION_EACH_2026(1).xlsx', 'PUBLICATIONS ONE EACH', 'Oxygen Master', 'C'),
    ]:
        path = args.input_dir / filename
        rows = sheet(path, name)[1:]
        for ordinal, row in enumerate(rows, 2):
            assert clean(row[column]) == clean(indexed[(source, str(ordinal))][1]['title']), f'Workbook row mismatch: {source} {ordinal}'
        assert len(rows) == sum(key[0] == source for key in indexed)
        workbooks.append({'filename': filename, 'sheet': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'rows': len(rows), 'retainedRows': len(rows), 'missingRows': 0})
    public = [r for r in records if not r['recordType'].startswith('Import')]
    report = {
        'checked': '2026-10-11', 'sources': inputs, 'workbooks': workbooks,
        'sourceOccurrences': len(indexed), 'retainedRecordsIncludingFragments': len(records),
        'repeatedSourceOccurrences': len(indexed) - len(records),
        'incompleteSourceFragments': len(records) - len(public), 'publicRecords': len(public),
        'catalogues': dict(Counter(r['catalogue'] for r in public)), 'missingSourceRows': 0,
        'calculation': f'{len(indexed)} source occurrences - {len(indexed)-len(records)} repeated occurrences - {len(records)-len(public)} incomplete fragments = {len(public)} public records',
        'note': 'This verifies coverage of the supplied files. It does not claim that this collection contains every publication in the scientific literature.',
    }
    (BASE / 'catalogues/data/source-coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
