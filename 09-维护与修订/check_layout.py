# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess, json
R=Path(r'D:\VMShare\芯片底层软件40周')
err=[]; warnings=[]; internal=0; tables=0
def from_git(p):
    return subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R).decode('utf-8-sig')
def where(p): return p.relative_to(R).as_posix()
docs=list(R.rglob('*.md'))
docs=[p for p in docs if p.name!='原手册-完整版.md' and '.git' not in p.parts and '.gitnexus' not in p.parts]
for p in docs:
    t=p.read_text(encoding='utf-8-sig')
    for link in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',t):
        if link.startswith(('https://','http://','#','mailto:','data:')): continue
        target=link.split('#')[0].split('?')[0]
        if not target: continue
        internal+=1
        if not (p.parent/target).exists(): err.append(f'broken link {where(p)} -> {target}')
    lines=t.splitlines(); fenced=False; i=0
    while i+1<len(lines):
        line=lines[i].strip()
        if line.startswith((chr(96)*3,'~~~')):
            fenced=not fenced; i+=1; continue
        if fenced: i+=1; continue
        nxt=lines[i+1].strip()
        if line.startswith('|') and line.endswith('|') and nxt.startswith('|') and nxt.endswith('|'):
            parts=nxt.strip('|').split('|')
            if len(parts)>=2 and all(re.fullmatch(r'\s*:?-{3,}:?\s*',x) for x in parts):
                tables+=1; width=len(parts)
                if len(line.strip('|').split('|'))!=width:err.append(f'header columns {where(p)}:{i+1}')
                j=i+2
                while j<len(lines):
                    q=lines[j].strip()
                    if not (q.startswith('|') and q.endswith('|')):break
                    observed=len(q.strip('|').split('|'))
                    if observed!=width:warnings.append(f'columns {where(p)}:{j+1}: {observed}/{width}')
                    j+=1
                i=j;continue
        i+=1
s=(R/'README.md').read_text(encoding='utf-8')
if s.count('| 周次 | 本周课程 | 学习记录 |')!=5:err.append('README: 5 group headers')
r=[q for q in s.splitlines() if re.match(r'^\| W\d\d \|',q)]
if len(r)!=40:err.append('README: 40 week rows')
for n in range(1,41):
    q=next((q for q in r if q.startswith(f'| W{n:02d} |')),None)
    if not q or len(q.strip('|').split('|'))!=3 or any(f'[{label}]' not in q for label in ('笔记','周报','代码')):
        err.append(f'README malformed W{n:02d}')
prog=(R/'01-进度核对/进度总表.md').read_text(encoding='utf-8')
if prog.count('| 周次 · 小阶段 | 学习主题（点击查看课程） | 学习记录 | 状态 | 完成日期 |')!=5:
    err.append('progress: 5 group headers')
rows=[q for q in prog.splitlines() if re.match(r'^\| W\d\d · M\d+ \|',q)]
if len(rows)!=40:err.append('progress 40 weeks')
for n in range(1,41):
    q=next((x for x in rows if x.startswith(f'| W{n:02d} · ')),None)
    if not q or len(q.strip('|').split('|'))!=5 or '| ☐ |' not in q:
        err.append(f'progress malformed W{n:02d}')
for m in range(1,22):
    if not re.search(rf'^\| M{m} \|',prog,re.M):err.append(f'missing M{m}')
for n in range(1,41):
    ps=list((R/'02-每周计划').rglob(f'W{n:02d}-*.md'))
    if len(ps)!=1:err.append(f'missing/duplicate W{n:02d}');continue
    p=ps[0]; new=p.read_text(encoding='utf-8'); old=from_git(p)
    oldtasks=[x for x in old.splitlines() if re.match(r'^\| D[1-6] \|',x)]
    newtasks=[x for x in new.splitlines() if re.match(r'^\| D[1-6] \|',x)]
    # W22 fixes an unescaped table pipe without changing the --source option meaning.
    if n==22:oldtasks=[x.replace('<file|rtsp>','<file-or-rtsp>') for x in oldtasks]
    if oldtasks!=newtasks:err.append(f'lesson table changed W{n:02d}')
    for url in set(re.findall(r'https?://[^\s)\]]+',old)):
        if url not in new:err.append(f'lost lesson URL W{n:02d} {url}')
    if new.count('[← 课程目录]')!=1:err.append(f'weekly nav W{n:02d}')
    for val in [f'W{n:02d}/note.md',f'W{n:02d}/report.md',f'W{n:02d}/code/']:
        if val not in new:err.append(f'weekly link W{n:02d} {val}')
    d=R/'04-笔记'/f'W{n:02d}'
    for fn in ['note.md','report.md','code/README.md']:
        t=(d/fn).read_text(encoding='utf-8')
        if '[课程目录]' not in t or '[本周课程]' not in t:err.append(f'record nav W{n:02d} {fn}')
        if len(t.splitlines())>15:err.append(f'record length W{n:02d} {fn}')
archive=R/'00-总览与规则/原手册-完整版.md'
if archive.read_text(encoding='utf-8-sig')!=from_git(archive):err.append('historical source modified')
deletions=subprocess.run(['git','diff','--name-only','--diff-filter=D'],cwd=R,stdout=subprocess.PIPE,text=True,encoding='utf-8').stdout.strip()
if deletions:err.append('tracked files removed: '+deletions[:200])
print(json.dumps({'markdown_docs':len(docs),'tables':tables,'internal_links':internal,'weeks':40,'milestones':21,'warnings':warnings[:35],'warning_count':len(warnings),'errors':err[:35],'error_count':len(err)},ensure_ascii=True,indent=2))
if err or warnings:raise SystemExit(1)
