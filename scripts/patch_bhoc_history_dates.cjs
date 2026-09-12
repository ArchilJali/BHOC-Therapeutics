const fs=require('fs');
const file='bhoc/index.html';
let s=fs.readFileSync(file,'utf8');
if(!s.includes('.bhoc-date{')){
  s=s.replace('</style>',`.bhoc-date{display:inline-block;margin-top:7px;padding:3px 7px;border-radius:999px;background:#f1f4f6;color:#687683;font:800 8px/1.3 Arial,Helvetica,sans-serif;letter-spacing:.045em;text-transform:uppercase;white-space:nowrap}.bhoc-date.added{background:#e7f6f8;color:#0e718b}\n  </style>`);
}
const replacements=[
 ['<span>Open science →</span></a>','<span>Open science →</span><time class="bhoc-date" datetime="2026-09-10">Updated 10 Sep 2026</time></a>'],
 ['<span>Open technology →</span></a>','<span>Open technology →</span><time class="bhoc-date" datetime="2026-09-10">Updated 10 Sep 2026</time></a>'],
 ['<span>Open evidence →</span></a>','<span>Open evidence →</span><time class="bhoc-date" datetime="2026-09-10">Updated 10 Sep 2026</time></a>'],
 ['<span>Open archive ↗</span></a>','<span>Open archive ↗</span><time class="bhoc-date" datetime="2026-09-09">Updated 09 Sep 2026</time></a>'],
 ['<span>Open hub ↗</span></a>','<span>Open hub ↗</span><time class="bhoc-date" datetime="2026-09-09">Updated 09 Sep 2026</time></a>'],
 ['<span>Explore platform ↗</span></a>','<span>Explore platform ↗</span><time class="bhoc-date" datetime="2026-09-12">Updated 12 Sep 2026</time></a>']
];
for(const [from,to] of replacements){
  if(s.includes(from)) s=s.replace(from,to);
}
// The generic Open hub label occurs for Human, Veterinary and Transplantation. Add date to any remaining ones.
s=s.replaceAll('<span>Open hub ↗</span></a>','<span>Open hub ↗</span><time class="bhoc-date" datetime="2026-09-09">Updated 09 Sep 2026</time></a>');
fs.writeFileSync(file,s);
