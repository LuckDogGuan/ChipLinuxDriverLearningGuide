# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess, datetime
R=Path(r'D:\VMShare\芯片底层软件40周')
assert R.exists()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.STDOUT,text=True,encoding='utf-8').strip()
assert git('-c','core.quotepath=false','status','--porcelain') == '?? 09-维护与修订/simplify_20261118.py', '工作区有未提交的其他改动，停止自动修改'
before=git('rev-parse','HEAD')
P={}
for p in (R/'02-每周计划').rglob('W*.md'):
    m=re.match(r'W(\d\d)-',p.name)
    if m:
        k=int(m.group(1))
        assert k not in P
        P[k]=p
assert set(P)==set(range(1,41))
# Confirm all blank templates; refuse to overwrite actual user-authored notes/reports
for k in range(1,41):
    d=R/'04-笔记'/f'W{k:02d}'
    note=(d/'note.md').read_text(encoding='utf-8')
    report=(d/'report.md').read_text(encoding='utf-8')
    assert '## 每日 3 行' in note and '## 本周总结' in note and len(note.splitlines())==40, f'笔记可能已被填写: W{k:02d}'
    assert '## 2026-11-17 新增：本周根因定位卡' in report and len(report.splitlines())==33, f'周报可能已被填写: W{k:02d}'
    assert not (d/'code/README.md').exists(), f'代码 README 已存在 W{k:02d}'
def save(p,s):
    p.write_text(s.rstrip()+'\n',encoding='utf-8')
for k,plan in sorted(P.items()):
    d=R/'04-笔记'/f'W{k:02d}'
    title=re.search(r'^#\s*W\d\d\s*[　 ]*(.*)',plan.read_text(encoding='utf-8'),re.M).group(1).strip()
    link=f'../../02-每周计划/{plan.parent.name}/{plan.name}'
    n=f'''# W{k:02d} 笔记 · {title}

[本周课程]({link}) · [周报](report.md) · [代码](code/)

## 学习记录


## 疑问与资料
'''
    rep=f'''# W{k:02d} 周报 · {title}

[本周课程]({link}) · [笔记](note.md) · [代码](code/)

## 本周完成


## 问题定位


## 下周重点
'''
    code=f'''# W{k:02d} 实验代码

[本周课程](../../../02-每周计划/{plan.parent.name}/{plan.name}) · [笔记](../note.md) · [周报](../report.md)

本目录放本周的源代码、构建脚本和测试文件，直接按需要新增即可。
'''
    save(d/'note.md',n)
    save(d/'report.md',rep)
    save(d/'code/README.md',code)
    (d/'code/.gitkeep').unlink(missing_ok=True)
    s=plan.read_text(encoding='utf-8')
    hdr=f'> 笔记：[04-笔记/W{k:02d}/note.md](../../04-笔记/W{k:02d}/note.md)　｜　周报：[report.md](../../04-笔记/W{k:02d}/report.md)'
    assert hdr in s, f'week plan header format changed W{k:02d}'
    s=s.replace(hdr,hdr+f'　｜　[代码](../../04-笔记/W{k:02d}/code/)',1)
    begin=s.index('## 本周交付清单')
    end=s.find('\n\n## 本周深化与定位挑战',begin)
    assert end!=-1,f'week plan section missing W{k:02d}'
    newsec=f'''## 本周记录：笔记 · 周报 · 代码

- [ ] [笔记](../../04-笔记/W{k:02d}/note.md)
- [ ] [周报](../../04-笔记/W{k:02d}/report.md)
- [ ] [代码](../../04-笔记/W{k:02d}/code/)

截图、日志、波形可按需放入 §../../04-笔记/W{k:02d}/evidence/§；[进度总表](../../01-进度核对/进度总表.md)只作可选总览。
'''
    # convert placeholder § to markdown backtick to avoid tooling command parser conflict
    newsec=newsec.replace('§','\x60')
    s=s[:begin]+newsec+s[end:]
    save(plan,s)
# Top-level README: add a code link to every row and header
readme=R/'README.md'
s=readme.read_text(encoding='utf-8')
assert s.count('| 周次 | 课程 | 笔记 | 周报 |')==5
s=s.replace('| 周次 | 课程 | 笔记 | 周报 |','| 周次 | 课程 | 笔记 | 周报 | 代码 |')
s=s.replace('| --- | --- | --- | --- |','| --- | --- | --- | --- | --- |')
for k in range(1,41):
    pattern=re.compile(r'^(\| W'+str(k).zfill(2)+r' \|.*\|)$',re.M)
    hits=pattern.findall(s)
    assert len(hits)==1, ('README row missing',k)
    s=pattern.sub(lambda m:m.group(1)[:-1]+f' [代码](04-笔记/W{k:02d}/code/) |',s,count=1)
s=s.replace('**[从 W01 开始]','**每周只需要维护：[笔记](04-笔记/W01/note.md)、[周报](04-笔记/W01/report.md)、[代码](04-笔记/W01/code/)。课程计划是任务说明，进度表是可选总览。**\n\n**[从 W01 开始]',1)
save(readme,s)
# Progress table: preserve status, make code link an accessible column
progress=R/'01-进度核对/进度总表.md'
s=progress.read_text(encoding='utf-8')
assert s.count('| 周 | 主题 | 小阶段 | 计划 | 笔记 | 周报 | 状态 | 完成日期 |')==5
s=s.replace('| 周 | 主题 | 小阶段 | 计划 | 笔记 | 周报 | 状态 | 完成日期 |','| 周 | 主题 | 小阶段 | 计划 | 笔记 | 周报 | 代码 | 状态 | 完成日期 |')
s=s.replace('|---|---|---|---|---|---|---|---|','|---|---|---|---|---|---|---|---|---|')
for k in range(1,41):
    pat=re.compile(r'^(\| W'+str(k).zfill(2)+r' \|.+?\| \[周报\]\([^)]+\) \|)( ☐ \|)',re.M)
    assert len(pat.findall(s))==1, f'progress W{k:02d}'
    s=pat.sub(lambda m:m.group(1)+f' [代码](../04-笔记/W{k:02d}/code/) |'+m.group(2),s,count=1)
s=s.replace('> 实际开始的那一周记为 W01，日期不绑定。','> 实际开始的那一周记为 W01，日期不绑定。本表只作导航与可选进度勾选，不是每周必须填写的第四份记录。',1)
save(progress,s)
# Usage rules: one three-piece framework; otherwise do not rewrite objectives or hardware details
rules=R/'00-总览与规则/使用规则.md'
s=rules.read_text(encoding='utf-8')
a=s.index('### 笔记规则')
b=s.index('### 每个阶段末用五道门自测',a)
s=s[:a]+'''### 每周只维护三个内容

- **笔记**：学习记录、疑问与资料链接；按天或按知识点自由写，不限制格式。
- **周报**：本周完成、问题定位、下周重点；复杂故障可另附详细分析，不必每周额外填表。
- **代码**：实验源代码、构建脚本与测试，直接放 §04-笔记/Wxx/code/§。截图和日志按需放 §evidence/§，不用再做独立记录表。

三个入口在 [README](../README.md)、[进度总表](../01-进度核对/进度总表.md) 和每周计划中互相链接；进度表不强制维护。调试的重要性不变，重点写在**周报的问题定位**里。

'''.replace('§','\x60')+s[b:]
save(rules,s)
# Adjust duplicated meta guidance without modifying historical original
guide=R/'05-学习校验/调试能力贯穿40周.md'
s=guide.read_text(encoding='utf-8')
s=s.replace('至少一份简短定位卡：现象、证据、假设 A/B、验证结果、根因或阻塞、回归。','在本周 §report.md§ 的“问题定位”一节简写：现象、证据、排除过程、根因或待查、回归；无需再填额外模板。'.replace('§','\x60'))
save(guide,s)
# Revision record
log=R/'09-维护与修订/2026-11-18-三件套简化.md'
save(log,'''# 2026-11-18 记录模板简化

> 从原有 git commit 的工作区干净状态开始调整。该提交本身可作为历史备份。

## 修改原则

- **三件套**：每周只维护 §note.md§（笔记）、§report.md§（周报）、§code/§（代码）。
- 每周三个入口互联，§code/README.md§ 只用于导航、**不需要用户填写**。
- W01–W40 原有课程内容、官方文档、调试挑战、验收要求均保留；简化的是**手写记录和入口**，不是删除技术要求。
- 笔记仅保留“学习记录 / 疑问与资料”，周报仅保留“本周完成 / 问题定位 / 下周重点”。
- 不再强制每天 3 行、周报 5 项、另填根因分析卡或同步维护进度表。
- §evidence/§ 用于可选日志、波形、截图，保留目录但不作为第四项表格。
- 40 个 §code/.gitkeep§ 用更有用的 §code/README.md§ 替代。
- 老的完整手册及其技术资料不覆盖；此前的历史记录仍可从 Git 找回。

## 快速使用

进入仓库 README → 本周课程 → 点击“笔记 / 周报 / 代码”之一；在笔记、周报、代码目录里都可返回同周其他入口。

> 本次修改前各周笔记/周报经断言确认为统一空白模板；若以后写入真实内容，请不要重新运行此一次性迁移脚本。
'''.replace('§','\x60'))
print('BASE_COMMIT='+before)
print('UPDATED_WEEKS='+str(len(P)))
print('NOTE_REPORT_CODE_LINKS_ADDED=40')
print('MIGRATION=OK')
