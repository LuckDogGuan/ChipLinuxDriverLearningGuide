# -*- coding: utf-8 -*-
"""2026-11-18 GitHub Markdown navigation/layout tidy-up. One-time migration."""
from pathlib import Path
import re, subprocess, json
R=Path(r'D:\VMShare\芯片底层软件40周')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R, encoding='utf-8', stderr=subprocess.STDOUT).strip()
assert git('-c','core.quotepath=false','status','--porcelain') == '?? 09-维护与修订/layout_20261118.py', '有非本脚本的未提交修改，停止'
original_commit=git('rev-parse','HEAD')
P={}
for p in (R/'02-每周计划').rglob('W*.md'):
    m=re.match(r'W(\d\d)-',p.name)
    if m:
        n=int(m.group(1))
        assert n not in P
        P[n]=p
assert set(P)==set(range(1,41))
def save(p, s): p.write_text(s.rstrip()+'\n',encoding='utf-8')
# 1. README: 5 malformed columns -> 3 balanced columns.
path=R/'README.md'
s=path.read_text(encoding='utf-8')
assert s.count('| 周次 | 课程 | 笔记 | 周报 | 代码 |')==5
assert s.count('| --- | --- | --- | --- | --- |')==5
s=s.replace('| 周次 | 课程 | 笔记 | 周报 | 代码 |','| 周次 | 本周课程 | 学习记录 |')
s=s.replace('| --- | --- | --- | --- | --- |','| :--- | :--- | :--- |')
pat=re.compile(r'^\| (W\d\d) \| (\[[^\]\n]+\]\([^)]+\)) \| \[笔记\]\(([^)]+)\) \| \[周报\]\(([^)]+)\)\s+\[代码\]\(([^)]+)\) \|$',re.M)
rows=pat.findall(s)
assert len(rows)==40, ('README row layout',len(rows))
s=pat.sub(lambda m:f'| {m.group(1)} | {m.group(2)} | [笔记]({m.group(3)}) · [周报]({m.group(4)}) · [代码]({m.group(5)}) |',s)
old='**每周只需要维护：[笔记](04-笔记/W01/note.md)、[周报](04-笔记/W01/report.md)、[代码](04-笔记/W01/code/)。课程计划是任务说明，进度表是可选总览。**'
new='**每周只维护笔记、周报、代码。** 点击课程学习，右侧“学习记录”可直接进入对应文件；进度表为可选总览。'
assert s.count(old)==1
s=s.replace(old,new)
# Improve overview navigation without adding badges/images/width-locked HTML.
old='**[从 W01 开始](02-每周计划/阶段A-C与用户态-W01-W10/W01-环境-数据表示-GDB-起步.md)** · **[学习进度](01-进度核对/进度总表.md)**'
new='[▶ 从 W01 开始](02-每周计划/阶段A-C与用户态-W01-W10/W01-环境-数据表示-GDB-起步.md) · [40 周进度](01-进度核对/进度总表.md) · [原厂/官方资料](03-资料链接/一手资料阅读路线.md) · [可视化工具](03-资料链接/可视化学习地图.md)'
assert s.count(old)==1
s=s.replace(old,new)
save(path,s)
# 2. Progress: 9 columns -> 5; preserve 40 topics, milestones, states and dates.
path=R/'01-进度核对/进度总表.md'
s=path.read_text(encoding='utf-8')
oldheader='| 周 | 主题 | 小阶段 | 计划 | 笔记 | 周报 | 代码 | 状态 | 完成日期 |'
assert s.count(oldheader)==5
s=s.replace(oldheader,'| 周次 · 小阶段 | 学习主题（点击查看课程） | 学习记录 | 状态 | 完成日期 |')
oldsep='|---|---|---|---|---|---|---|---|---|'
assert s.count(oldsep)==5
s=s.replace(oldsep,'| :--- | :--- | :--- | :---: | :--- |')
pat=re.compile(r'^\| (W\d\d) \| ([^\n|]+) \| (M\d+) \| \[计划\]\(([^)]+)\) \| \[笔记\]\(([^)]+)\) \| \[周报\]\(([^)]+)\) \| \[代码\]\(([^)]+)\) \| ([^|\n]+) \| ([^|\n]*) \|$',re.M)
rows=pat.findall(s)
assert len(rows)==40, ('progress row layout',len(rows))
s=pat.sub(lambda m:f'| {m.group(1)} · {m.group(3)} | [{m.group(2)}]({m.group(4)}) | [笔记]({m.group(5)}) · [周报]({m.group(6)}) · [代码]({m.group(7)}) | {m.group(8).strip()} | {m.group(9).strip()} |',s)
# Remove stale duplicative section header spacing but preserve all milestones.
s=s.replace('## 二、40 周逐周进度\n\n\n','## 二、40 周逐周进度\n\n')
s=s.replace('## 四、调试训练与官方资料核对（2026-11-17 新增）','## 四、调试训练与官方资料')
save(path,s)
# 3. Weekly plan navigation: one compact toolbar, remove duplicated three-checkbox section.
changes=[]
for n,p in sorted(P.items()):
    t=p.read_text(encoding='utf-8')
    # This navigation should be exactly once per week; retain milestone and label lines.
    navlines=[line for line in t.splitlines() if line.startswith('> 笔记：')]
    assert len(navlines)==1 and '[进度总表]' in navlines[0] and '[代码]' in navlines[0], (n,'nav')
    newnav=(f'> [← 课程目录](../../README.md) · '
            f'[笔记](../../04-笔记/W{n:02d}/note.md) · '
            f'[周报](../../04-笔记/W{n:02d}/report.md) · '
            f'[代码](../../04-笔记/W{n:02d}/code/) · '
            f'[进度](../../01-进度核对/进度总表.md)')
    t=t.replace(navlines[0],newnav,1)
    a=t.index('## 本周记录：笔记 · 周报 · 代码')
    b=t.index('## 本周深化与定位挑战',a)
    oldrecord=t[a:b]
    assert oldrecord.count('[笔记]')==1 and oldrecord.count('[周报]')==1 and oldrecord.count('[代码]')==1, (n,'records')
    t=t[:a]+f'实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W{n:02d}/evidence/)；无需额外填写记录表。\n\n'+t[b:]
    # Shorter heading; do not remove any actual learning content.
    t=t.replace('## 本周深化与定位挑战（2026-11-17 修订）','## 深化与故障定位',1)
    # Existing wording can remain historical, but clean redundant punctuation.
    t=t.replace('？。提交现象','？提交现象')
    save(p,t)
    changes.append(n)
# 4. Keep three-piece note/report/code simple, add one click back to the README.
for n in range(1,41):
    d=R/'04-笔记'/f'W{n:02d}'
    for name,rel in [('note.md','../../README.md'),('report.md','../../README.md'),('code/README.md','../../../README.md')]:
        p=d/name
        t=p.read_text(encoding='utf-8')
        lines=t.splitlines()
        assert len(lines) < 15 and lines[2].startswith('[本周课程]'), (n,name)
        lines[2]=f'[课程目录]({rel}) · '+lines[2]
        save(p,'\n'.join(lines))
# 5. A compact README of visual/layout choices and checks.
p=R/'09-维护与修订/2026-11-18-页面排版优化.md'
save(p,'''# 2026-11-18 页面排版优化

这次只调整 Markdown 的**信息层级、导航、表格列数、重复入口**，不改变 40 周内容、技术挑战或手册原文。

## 修正

- README：原有 5 列表头、4 列数据造成“周报代码”黏连；统一为 **周次 / 本周课程 / 学习记录** 三列，40 周均有三个独立链接。
- 进度表：原九列太宽，压缩成 **周次与小阶段 / 学习主题 / 学习记录 / 状态 / 日期** 五列，保留 21 个里程碑以及未填写的状态和日期。
- 每周计划：顶部集中“课程目录 / 笔记 / 周报 / 代码 / 进度”导航，去掉正文里重复的三项勾选区域，保留实验素材位置及完整的学习任务。
- 40 组笔记、周报、代码入口：增加回到课程目录的链接，不增加需要手填的字段。

## 使用

README 点击某周课程；顶部进入学习记录；每份笔记、周报、代码目录都能返回本周课程或课程目录。代码目录 README 仅为导航，不需填写。

## 保全

所有学习任务、D1–D6 课程网址、原厂资料、故障定位挑战、四个项目均保留。历史版本由 Git commit 记录，修改可比较或回退。

## 检查

参见本目录 §check_layout.py§，包括表格完整性、所有本地 Markdown 链接、40 周导航、内容变动边界与仓库状态。'''.replace('§','\x60'))
print(json.dumps({'base_commit':original_commit,'weekly_plans':len(changes),'readme_rows':40,'progress_rows':40,'updated_entry_pages':120},ensure_ascii=False))
