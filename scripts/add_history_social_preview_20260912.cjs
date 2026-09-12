const fs=require('fs');
const file='bhoc/historical-evolution/index.html';
let s=fs.readFileSync(file,'utf8');
const image='https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png?v=20260912-history';

s=s.replace('<meta property="og:title" content="Historical Evolution | From Bloodletting to Oxygen Therapeutics">','<meta property="og:title" content="BHOC Historical Evolution: From Bloodletting to Oxygen Therapeutics">');
s=s.replace('<meta property="og:description" content="A source-linked historical perspective on transfusion, donor blood, artificial blood, HBOCs and the evolution toward oxygen-delivery function.">','<meta property="og:description" content="From transfusion and blood groups to HBOCs, Hemopure, Oxyglobin and Precision Oxygen Therapeutics. A source-linked BHOC historical review.">');
if(!s.includes('property="og:image"')){
  s=s.replace('<meta property="og:url" content="https://bhoctherapeutics.com/bhoc/historical-evolution/">',`<meta property="og:url" content="https://bhoctherapeutics.com/bhoc/historical-evolution/">\n  <meta property="og:image" content="${image}">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="BHOC Therapeutics - Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics">`);
}
s=s.replace('<meta name="twitter:card" content="summary">','<meta name="twitter:card" content="summary_large_image">');
s=s.replace('<meta name="twitter:title" content="Historical Evolution | From Bloodletting to Oxygen Therapeutics">','<meta name="twitter:title" content="BHOC Historical Evolution: From Bloodletting to Oxygen Therapeutics">');
s=s.replace('<meta name="twitter:description" content="How medicine moved from removing blood to transfusion, donor systems, artificial blood, HBOCs and function-first oxygen therapeutics.">',`<meta name="twitter:description" content="From transfusion and blood groups to HBOCs, Hemopure, Oxyglobin and Precision Oxygen Therapeutics.">\n  <meta name="twitter:image" content="${image}">\n  <meta name="twitter:image:alt" content="BHOC Therapeutics - Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics">`);
fs.writeFileSync(file,s);
