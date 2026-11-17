# -*- coding: utf-8 -*-
from pathlib import Path
import re, hashlib, json, collections
R=Path(r'D:\VMShare\芯片底层软件40周')
B=Path(r'D:\VMShare\芯片底层软件40周-修改前备份-20261117')
def relfiles(root):
 return {str(p.relative_to(root)).replace('\\','/'):p for p in root.rglob('*') if p.is_file()}
a=relfiles(B); b=relfiles(R)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
missing=[]; changed=[]; untouched=[]
renames={
'02-每周计划/阶段C-摄像头数据通路-W21-W25/W25-轻量周-岗位核对与展示-C.md':'02-每周计划/阶段C-摄像头数据通路-W21-W25/W25-轻量周-机制复盘与展示-C.md',
'02-每周计划/阶段E-调试与交付-W33-W40/W39-岗位专项选修-三选一.md':'02-每周计划/阶段E-调试与交付-W33-W40/W39-专项机制深入-三选一.md'}
for key,p in a.items():
 target=renames.get(key,key)
 if target not in b: missing.append(key);continue
 if sha(p)==sha(b[target]):untouched.append(key)
 else:changed.append(key)
errors=[]; warnings=[]
if missing:errors.append('original files lost: '+repr(missing))
if len(a)!=231:errors.append('backup file count expected 231 got '+str(len(a)))
for key in a:
 target=renames.get(key,key)
 if ('/code/' in key or '06-项目与代码/代码模板/' in key or key=='.gitattributes') and sha(a[key])!=sha(b[target]):
  errors.append('source/code was modified: '+key)
 if '/note.md' in key and sha(a[key])!=sha(b[target]):
  oldtext=a[key].read_text(encoding='utf-8')
  newtext=b[target].read_text(encoding='utf-8')
  for oldname,newname in [('W25-轻量周-岗位核对与展示-C.md','W25-轻量周-机制复盘与展示-C.md'),('W39-岗位专项选修-三选一.md','W39-专项机制深入-三选一.md'),('岗位核对与展示 C','机制复盘与展示 C'),('岗位专项选修：三选一','专项机制深入：三选一')]:
   oldtext=oldtext.replace(oldname,newname)
  if oldtext!=newtext:errors.append('note content beyond link/title modified: '+key)
# W01-W40: all preexisting lesson URLs preserved
for n in range(1,41):
 old=[(key,p) for key,p in a.items() if re.search(r'/W'+str(n).zfill(2)+r'-.*\.md$',key) and key.startswith('02-每周计划/')]
 new=[(key,p) for key,p in b.items() if re.search(r'/W'+str(n).zfill(2)+r'-.*\.md$',key) and key.startswith('02-每周计划/')]
 if len(old)!=1 or len(new)!=1:errors.append('week missing/duplicate '+str(n));continue
 ot=old[0][1].read_text(encoding='utf-8')
 nt=new[0][1].read_text(encoding='utf-8')
 urls=set(re.findall('https?://[^\\s)\\]]+',ot))
 for u in urls:
  if u not in nt: errors.append('original course link lost W%02d: %s'%(n,u))
 if n not in (25,39,40):
  tbl=re.search(r'(\| 日 \| 任务(?: \| 课程 / 资料)? \|.*?)(?=\n\n验收:)',ot,re.S)
  if tbl and tbl.group(1) not in nt:errors.append('original day-task content missing W%02d'%n)
 else:
  if '岗位' in '\n'.join([line for line in nt.splitlines() if line.startswith('| D')]):
   errors.append('career task remains W%02d'%n)
# key requirements
main=(R/'00-总览与规则/阶段总览.md').read_text(encoding='utf-8')
progress=(R/'01-进度核对/进度总表.md').read_text(encoding='utf-8')
for i in range(1,22):
 for name,t in [('main',main),('progress',progress)]:
  if f'| M{i} |' not in t: errors.append(f'{name} missing milestone M{i}')
for project in ['P1','P2','P3','P4']:
 if project not in (R/'06-项目与代码/四个项目说明.md').read_text(encoding='utf-8'):
  errors.append('project '+project+' missing')
if sha(B/'00-总览与规则/原手册-完整版.md')!=sha(R/'00-总览与规则/原手册-完整版.md'):
 errors.append('archived original modified')
report={'baseline_file_count':len(a),'current_file_count':len(b),'added_file_count':len(set(b)-set(a)-set(renames.values()))+len(renames),'changed_files':len(changed),'unchanged_files':len(untouched),'missing_files':missing,'critical_errors':errors,'error_count':len(errors),'note_and_code_preserved':not any('source/notes' in x for x in errors),'40week_original_video_urls_preserved':not any('course link lost' in x for x in errors),'37_nonfocus_day_tables_preserved':not any('day-task' in x for x in errors),'21_milestones_checked':True,'four_projects_checked':True}
print(json.dumps(report,ensure_ascii=True,indent=2))
if errors:exit(1)
