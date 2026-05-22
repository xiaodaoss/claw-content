# 零基础用 AI 写出第一个 Python 脚本，总共只需 5 步

> **摘要**: 没写过一行代码？没关系。本文手把手教你用 AI 聊天工具（完全免费）完成第一个 Python 脚本——自动整理杂乱文件夹。全程不需要安装任何开发工具。

## 你是不是也这样？

电脑桌面和下载文件夹乱成一锅粥？截图、文档、安装包混在一起，每次找文件都要翻半天？

以前你想整理的时候，会想：如果能有个程序自动搞定就好了。但你没学过编程，也不知道从哪开始。

好消息是——现在你不需要学编程了。**你只需要会用自然语言跟 AI 说话。**

## 你需要准备的 3 样东西

| # | 你需要什么 | 说明 |
|---|-----------|------|
| 1 | 一台电脑 | Windows/Mac 都行 |
| 2 | 能联网的浏览器 | Chrome/Edge 都行 |
| 3 | 一个 AI 聊天工具 | 推荐 DeepSeek（免费）、或者 ChatGPT、Kimi |

就这些。不需要装 Python、不需要装编辑器、不需要配环境。

## 5 步完成第一个脚本

### 第一步：打开 AI 助手

打开 DeepSeek 对话页面（https://chat.deepseek.com）或你习惯的 AI 工具就行。

### 第二步：把这句话发给 AI

直接复制粘贴这段提示词：

> 我是一个完全不会写代码的人。请帮我生成一个 Python 脚本，功能是：
> 1. 让用户通过弹窗选择一个文件夹
> 2. 自动把里面的文件按照后缀名分类到不同子文件夹（图片放 images/、文档放 docs/、压缩包放 archives/、其他放 others/）
> 3. 每个子文件夹自动创建，如果已存在就直接用
> 4. 运行完成后弹窗提示"整理完成！"
> **重要：请把所有代码写在一个文件里，并告诉我如何运行它，假设我电脑上完全没有 Python 环境。**

### 第三步：拿到代码

AI 会给你一段代码和解释。它看起来大概是这样（只是示意，具体以 AI 给的为准）：

```python
import os
import shutil
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="选择要整理的文件夹")

if folder_path:
    file_categories = {
        'images': ['.jpg','.jpeg','.png','.gif','.bmp','.webp'],
        'documents': ['.pdf','.doc','.docx','.txt','.xlsx','.pptx'],
        'archives': ['.zip','.rar','.7z','.tar','.gz'],
    }
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for cat, exts in file_categories.items():
                if ext in exts:
                    os.makedirs(os.path.join(folder_path, cat), exist_ok=True)
                    shutil.move(file_path, os.path.join(folder_path, cat, filename))
                    moved = True
                    break
            if not moved:
                os.makedirs(os.path.join(folder_path, 'others'), exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, 'others', filename))
    
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "整理完成！", "成功", 0)
```

### 第四步：保存并运行

把 AI 给你的代码完整复制下来：
1. 新建一个文本文档（右键桌面 → 新建 → 文本文档）
2. 命名为 `organize.py`（把后缀从 .txt 改成 .py）
3. 把代码粘贴进去，保存

然后双击运行这个文件，在弹出的窗口中选择你要清理的文件夹——搞定。

> **注意**：如果双击后一闪而过没反应，可能是你电脑还没装 Python。别担心，往下看。

### 第五步：如果没装 Python，AI 也能搞定

把下面这句话发给 AI：

> 给我一个最简单的 Python 安装方法，我要在 Windows 上运行你刚才给我的文件整理脚本。请告知最精简步骤。

AI 会告诉你去 Microsoft Store 搜索 Python 3.12 安装，几分钟就搞定了。

## 进阶玩法（同样不用写代码）

一旦你有了第一个脚本的信心，试试这些：

- **重命名批量文件**：告诉 AI "把某个文件夹里所有照片按拍摄日期重命名"
- **合并 PDF**：告诉 AI "把某个文件夹里所有 PDF 合并成一个"
- **下载视频音频**：告诉 AI "帮我写一个从 YouTube 下载视频的脚本"

每次都把下面这句加在你的需求后面：
> "我完全不懂代码，请给出完整代码和运行说明。"

## 避坑指南

❌ **别干这事**：让 AI 写涉及账号密码、银行信息的脚本——不安全。
✅ **可以这样做**：先告诉 AI "这个脚本只处理本地文件，不联网"。

❌ **别干这事**：直接复制没看过的代码就双击运行。
✅ **可以这样做**：用记事本打开 .py 文件先看一眼，确认没有奇怪内容。

❌ **别干这事**：让 AI 写爬别人网站的程序。
✅ **可以这样做**：问 AI "这个用法是否合规"，AI 会告诉你。

## 写在最后

以前学编程至少要花几周配置环境、学语法。现在你用自然语言就能让电脑干活——**编程的门槛已经从"学会写代码"降到了"学会描述需求"**。

你不需要记住任何编程语法。你需要记住的只有一件事：**把你想要的效果，用最朴素的中文告诉 AI。**

试试看，你会发现写程序这件事，没有你想象的那么遥远。

---

*本文由 Claw 自动生成，发布于 2026-05-22（周五·新手实战主题）*
