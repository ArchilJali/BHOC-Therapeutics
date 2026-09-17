import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
if(fs.existsSync(path.join(root,'bhoc/knowledge-map-baseline.json'))){
 execFileSync('python3',[path.join(root,'scripts/check_knowledge_map.py')],{cwd:root,stdio:'inherit'});
}else{await import('./check_bhoc_content_legacy.mjs');}
