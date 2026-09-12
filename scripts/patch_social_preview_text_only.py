from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Keep SEO title/description/canonical untouched; only make social previews compact and text-only.
s=re.sub(r'<meta property="og:image"[^>]*>','',s)
s=re.sub(r'<meta property="og:image:secure_url"[^>]*>','',s)
s=re.sub(r'<meta property="og:image:type"[^>]*>','',s)
s=re.sub(r'<meta property="og:image:width"[^>]*>','',s)
s=re.sub(r'<meta property="og:image:height"[^>]*>','',s)
s=re.sub(r'<meta property="og:image:alt"[^>]*>','',s)
s=re.sub(r'<meta name="twitter:image"[^>]*>','',s)
s=re.sub(r'<meta name="twitter:image:alt"[^>]*>','',s)
s=s.replace('<meta name="twitter:card" content="summary_large_image">','<meta name="twitter:card" content="summary">')
s=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="BHOC Therapeutics">',s,count=1)
s=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics.">',s,count=1)
s=re.sub(r'<meta name="twitter:title" content="[^"]*">','<meta name="twitter:title" content="BHOC Therapeutics">',s,count=1)
s=re.sub(r'<meta name="twitter:description" content="[^"]*">','<meta name="twitter:description" content="Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics.">',s,count=1)
p.write_text(s,encoding='utf-8')
