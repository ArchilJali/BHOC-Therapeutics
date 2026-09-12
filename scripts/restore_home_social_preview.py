from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove current OG/Twitter social tags we are about to replace.
for pat in [
    r'<meta property="og:title"[^>]*>',
    r'<meta property="og:description"[^>]*>',
    r'<meta property="og:url"[^>]*>',
    r'<meta property="og:image"[^>]*>',
    r'<meta property="og:image:secure_url"[^>]*>',
    r'<meta property="og:image:type"[^>]*>',
    r'<meta property="og:image:width"[^>]*>',
    r'<meta property="og:image:height"[^>]*>',
    r'<meta property="og:image:alt"[^>]*>',
    r'<meta name="twitter:card"[^>]*>',
    r'<meta name="twitter:title"[^>]*>',
    r'<meta name="twitter:description"[^>]*>',
    r'<meta name="twitter:image"[^>]*>',
    r'<meta name="twitter:image:alt"[^>]*>',
]:
    s=re.sub(pat,'',s,count=1)
anchor='<meta property="og:site_name" content="BHOC Therapeutics"><meta property="og:locale" content="en_US"><meta property="og:type" content="website">'
preview=(
    '<meta property="og:title" content="BHOC Therapeutics | Precision Oxygen Therapeutics">'
    '<meta property="og:description" content="Blood is a system. Oxygen delivery is a function. Explore BHOC across science, technology, applications, evidence and biodiversity protection.">'
    '<meta property="og:url" content="https://bhoctherapeutics.com/">'
    '<meta property="og:image" content="https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png">'
    '<meta property="og:image:secure_url" content="https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png">'
    '<meta property="og:image:type" content="image/png">'
    '<meta property="og:image:width" content="1200">'
    '<meta property="og:image:height" content="630">'
    '<meta property="og:image:alt" content="BHOC Therapeutics - Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics">'
    '\n<meta name="twitter:card" content="summary_large_image">'
    '<meta name="twitter:title" content="BHOC Therapeutics | Precision Oxygen Therapeutics">'
    '<meta name="twitter:description" content="Blood is a system. Oxygen delivery is a function. Explore BHOC across science, technology, applications, evidence and biodiversity protection.">'
    '<meta name="twitter:image" content="https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png">'
    '<meta name="twitter:image:alt" content="BHOC Therapeutics - Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics">'
)
if anchor not in s:
    raise SystemExit('OG anchor not found')
s=s.replace(anchor,anchor+preview,1)
p.write_text(s,encoding='utf-8')
