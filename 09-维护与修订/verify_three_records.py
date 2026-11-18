# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess, json
R=Path(r'D:\VMShare\芯片底层软件40周')
issues=[]; links=0; record_links=0
docs=[p for p in R.rglob('*.md') if p.name!='原手册-完整版.md' and not p.is_relative_to(R/'.git')]
for p in docs:
    s=p.read_text(encoding='utf-8-sig')
    for raw in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',s):
        if raw.startswith(('https://','http://','mailto:','#')):continue
        target=raw.split('#')[0].split('?')[0]
        if not target:continue
        links+=1
        if not (p.parent/target).exists():issues.append(f'BROKEN: {p.relative_to(R)} -> {target}')
for n in range(1,41):
    d=R/'04-笔记'/f'W{n:02d}'
    files=[d/'note.md',d/'report.md',d/'code/README.md']
    if not all(p.is_file() for p in files):issues.append(f'W{n:02d}: missing record');continue
    a,b,c=[p.read_text(encoding='utf-8') for p in files]
    if len(a.splitlines())>12 or len(b.splitlines())>14 or len(c.splitlines())>8:issues.append(f'W{n:02d}: too long')
    for p,s,needed in [(files[0],a,['[周报](report.md)','[代码](code/)','[本周课程]']), (files[1],b,['[笔记](note.md)','[代码](code/)','[本周课程]']), (files[2],c,['[笔记](../note.md)','[周报](../report.md)','[本周课程]'])]:
        if any(x not in s for x in needed):issues.append(f'{p}: backlink missing')
        else:record_links+=len(needed)
    if (d/'code/.gitkeep').exists():issues.append(f'W{n:02d}: obsolete code gitkeep')
    plan=list((R/'02-每周计划').rglob(f'W{n:02d}-*.md'))
    if len(plan)!=1 or f'[代码](../../04-笔记/W{n:02d}/code/)' not in plan[0].read_text(encoding='utf-8'):
        issues.append(f'W{n:02d}: plan code link missing')
    for f in [R/'README.md',R/'01-进度核对/进度总表.md']:
        if f'[代码](' not in f.read_text(encoding='utf-8') or f'W{n:02d}/code/' not in f.read_text(encoding='utf-8'):
            issues.append(f'{f.name}: week {n} code link missing')
# Ensure all planned lessons still present and no original full manual edits
old=subprocess.check_output(['git','show','HEAD:00-总览与规则/原手册-完整版.md'],cwd=R)
current=(R/'00-总览与规则/原手册-完整版.md').read_bytes()
if old!=current:issues.append('historical original changed')
# detect unexpected deleted files beyond old code .gitkeep
diff=subprocess.check_output(['git','-c','core.quotepath=false','diff','--name-status'],cwd=R,text=True,encoding='utf-8')
for line in diff.splitlines():
    if line.startswith('D\t') and not re.search(r'04-笔记/W\d\d/code/\.gitkeep$',line):
        issues.append('unexpected deletion '+line)
result={'total_markdown_internal_links':links,'three_record_backlinks_checked':record_links,'weeks':40,'errors':issues,'error_count':len(issues)}
print(json.dumps(result,ensure_ascii=True,indent=2))
if issues:raise SystemExit(1)
