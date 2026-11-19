# -*- coding: utf-8 -*-
from pathlib import Path
import re, hashlib, json, collections, sys
ROOT=Path(r'D:\VMShare\芯片底层软件40周')
BACKUP=Path(r'D:\VMShare\芯片底层软件40周-修改前备份-20261117')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
docs=[p for p in ROOT.rglob('*.md') if p.name!='原手册-完整版.md']
weeks=[p for p in ROOT.rglob('W*.md') if '02-每周计划' in str(p) and re.match(r'W\d\d-',p.name)]
weeknums=[int(re.match(r'W(\d\d)-',p.name).group(1)) for p in weeks]
errors=[]; warning=[]; links=0
if len(weeks)!=40 or sorted(weeknums)!=list(range(1,41)):errors.append('40 weeks count/unique fail')
for n in range(1,41):
    pn=ROOT/f'04-笔记/W{n:02d}/note.md'
    pr=ROOT/f'04-笔记/W{n:02d}/report.md'
    if not pn.is_file() or not pr.is_file():errors.append('missing note/report W'+str(n))
    matching=[p for p in weeks if p.name.startswith(f'W{n:02d}-')]
    if len(matching)==1:
        txt=matching[0].read_text(encoding='utf-8')
        for t in ['深化与故障定位','D1','D6','调试','一手资料']:
            if t not in txt: errors.append(f'W{n:02d} missing {t}')
        if '## 问题定位' not in pr.read_text(encoding='utf-8'):
            errors.append(f'report W{n:02d} missing issue section')
        if '## 学习记录' not in pn.read_text(encoding='utf-8'):
            errors.append(f'note W{n:02d} missing learning section')
        if not (ROOT/f'code/w{n:02d}/README.md').is_file():
            errors.append(f'code W{n:02d} navigation missing')
# Markdown links (path may contain spaces and parentheses - this is simple path check)
for p in docs:
    raw=p.read_text(encoding='utf-8-sig')
    for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)',raw):
        url=target.strip().split(' "')[0].strip('<>')
        if url.startswith(('https://','http://','mailto:','data:','#','app://')):continue
        if url.startswith('file:'):continue
        url=url.split('#')[0].split('?')[0]
        if not url:continue
        links+=1
        dest=p.parent/url
        if not dest.exists():errors.append(f'broken internal: {p.relative_to(ROOT)} -> {url}')
assert (ROOT/'00-总览与规则/原手册-完整版.md').exists()
if sha(ROOT/'00-总览与规则/原手册-完整版.md')!=sha(BACKUP/'00-总览与规则/原手册-完整版.md'):
    errors.append('original full text CHANGED')
for t in ['W25-轻量周-机制复盘与展示-C.md','W39-专项机制深入-三选一.md']:
    if not list(ROOT.rglob(t)):errors.append(f'new week filename missing {t}')
for t in ['W25-轻量周-岗位核对与展示-C.md','W39-岗位专项选修-三选一.md']:
    if list(ROOT.rglob(t)): errors.append(f'old week filename exists {t}')
# Detect actual outdated career homework, not negative policy statements or source symbols like start_kernel
residual=[]
for p in docs:
    if '02-每周计划' not in str(p) or not re.match(r'W\d\d-',p.name):continue
    txt=p.read_text(encoding='utf-8')
    for i,line in enumerate(txt.splitlines(),1):
        if line.lstrip().startswith('| D') and re.search('收集招聘|简历素材|更新简历|招聘信息|学历要求|STAR 格式',line):
            residual.append(f'{p.relative_to(ROOT)}:{i} {line[:140]}')
if residual:errors.append('outdated career homework remains')
report={'errors':errors,'error_count':len(errors),'warnings':warning,'internal_links_checked':links,'weekly_plans':len(weeks),'reports':40,'original_sha256':sha(ROOT/'00-总览与规则/原手册-完整版.md'),'residual_legacy_count':len(residual),'residual_legacy':residual[:60]}
print(json.dumps(report,ensure_ascii=True,indent=2))
sys.exit(1 if errors else 0)
