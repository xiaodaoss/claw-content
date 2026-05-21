# Claw 每日内容创作 #4

> 生成时间：2026-05-21 09:00
> 主题：Python/脚本技巧（周四轮换）
> 消耗：¥0.01
> 预期价值：¥10-30

---

## 标题（推荐）

**《5 个 Python 自动化脚本，帮你每天省出 1 小时》**

## 摘要

5 个拿来即用的 Python 脚本：批量重命名、文件夹整理、剪贴板增强、网页截图、Excel 合并。每段代码不到 20 行，复制粘贴就能跑。

---

## 正文

### 为什么你需要 Python 自动化？

作为一个开发者（或者想把编程当成工具的人），每天都有大量重复操作在悄悄吃掉你的时间——整理文件、处理 Excel、截图保存。这些事用手工做 10 分钟，用 Python 写脚本 1 分钟跑完。

下面 5 个脚本，覆盖日常最高频的自动化工况。每段都可以直接复制到 `.py` 文件里运行。

---

### 一、智能文件整理器（按类型自动归档）

```python
import os, shutil
from pathlib import Path

EXT_MAP = {
    '.jpg': '图片', '.png': '图片', '.gif': '图片',
    '.mp4': '视频', '.mkv': '视频',
    '.docx': '文档', '.pdf': '文档', '.txt': '文档',
    '.zip': '压缩包', '.rar': '压缩包',
}

def organize(folder='.'):
    for f in Path(folder).iterdir():
        if f.is_file() and f.suffix.lower() in EXT_MAP:
            dest = Path(folder) / EXT_MAP[f.suffix.lower()]
            dest.mkdir(exist_ok=True)
            shutil.move(str(f), str(dest / f.name))
            print(f'  → {dest.name}/{f.name}')

organize()  # 放在下载目录运行，一键归类
```

**怎么用：** 把文件扔到要整理的文件夹里，`python organize.py` 回车。它会自动创建「图片」「文档」「视频」等文件夹，把文件移进去。

---

### 二、Ctrl+C 增强版（自动保存剪贴板历史）

```python
import pyperclip, time, json
from datetime import datetime

HISTORY_FILE = 'clipboard_history.json'
try:
    history = json.load(open(HISTORY_FILE))
except: history = []

last = ''
while True:
    current = pyperclip.paste()
    if current != last and len(current) > 5:
        entry = {'text': current, 'time': datetime.now().isoformat()}
        history.append(entry)
        json.dump(history[-50:], open(HISTORY_FILE, 'w'))  # 保留最近 50 条
        print(f'✓ 已保存 ({len(history)} 条)')
        last = current
    time.sleep(1)
```

**怎么用：** 先 `pip install pyperclip`，然后后台跑这个脚本。你复制的任何文本都会自动记录到 `clipboard_history.json`，再也不会弄丢复制内容。

---

### 三、批量网页截图（验证布局、存档用）

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URLS = [
    'https://your-site.com/page1',
    'https://your-site.com/page2',
]

opts = Options()
opts.add_argument('--headless')
driver = webdriver.Chrome(options=opts)

for url in URLS:
    driver.get(url)
    name = url.split('/')[-1] or 'index'
    driver.save_screenshot(f'{name}.png')
    print(f'✓ {name}.png')

driver.quit()
```

**怎么用：** 先 `pip install selenium`，安装 ChromeDriver。把要截图的 URL 填进列表，跑一次能批量截几十个页面。适合网站改版前的页面存档、竞品监控。

---

### 四、Excel 合并工具（把多个表格统成一个）

```python
import pandas as pd
from pathlib import Path

folder = Path('.')
dfs = []
for f in folder.glob('*.xlsx'):
    df = pd.read_excel(f)
    df['来源文件'] = f.name        # 标记来源，方便追踪
    dfs.append(df)
    print(f'  + {f.name} ({len(df)} 行)')

merged = pd.concat(dfs, ignore_index=True)
merged.to_excel('合并结果.xlsx', index=False)
print(f'✓ 共合并 {len(dfs)} 个文件，{len(merged)} 行数据')
```

**怎么用：** 把同类 Excel 扔到一个文件夹，`pip install pandas openpyxl`，跑脚本。自动合并成一个文件，还多了一列「来源文件」让你知道每行从哪儿来的。

---

### 五、文件去重器（重复文件一键清理）

```python
import os, hashlib
from pathlib import Path

def file_hash(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

seen = set()
for f in Path('.').rglob('*'):
    if f.is_file() and f.stat().st_size > 0:
        h = file_hash(str(f))
        if h in seen:
            print(f'⚠ 重复: {f}')
            # os.remove(f)  # 确认后再取消这行注释
        else:
            seen.add(h)

print(f'✓ 扫描完成，发现 {len(seen)} 个唯一文件')
```

**怎么用：** 在你感觉有重复文件的目录跑一遍，它会列出所有重复文件。**先看列表确认没问题**，再把注释掉的 `os.remove` 行打开。

---

### 组合使用小技巧

把这 5 个脚本放在 `~/scripts/` 目录下，需要的时候拿出来改两行就能用。也可以这样：

```bash
# 一键归档桌面文件
cd ~/Desktop && python ../scripts/organize.py

# 截完图发到 Telegram / Slack（配合 webhook 脚本）
```

---

### 延伸阅读

| 场景 | 推荐库 | 一句话用途 |
|------|--------|------------|
| 批量 PDF 处理 | PyMuPDF | 提取文字、合并拆分、加水印 |
| 文件监听 | watchdog | 文件变化时自动触发脚本 |
| 批量发邮件 | yagmail | 3 行代码发一封带附件的邮件 |
| 定时任务 | schedule | `schedule.every().day.at("09:00").do(job)` |

---

## 一句话分享

> "写脚本不是为了省 5 分钟，而是为了以后再也不做这件事。"

---

## 发布后检查清单

- [x] 文章已保存到本地
- [ ] 已推送到 GitHub pages
- [ ] 钱包已记账
