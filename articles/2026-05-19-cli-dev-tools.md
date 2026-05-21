# Claw 每日内容创作 #3

> 生成时间：2026-05-19 09:00
> 主题：效率工具推荐（周二轮换）
> 消耗：¥0.01
> 预期价值：¥10-30

---

## 标题（推荐）

**《4 个命令行效率工具，让你的开发速度翻倍（附 AI 提示词模板）》**

## 摘要

4 个让你相见恨晚的 CLI 工具：fzf、ripgrep、bat、jq。每个附安装命令、实用示例和 AI 提示词模板，看完就能用。

---

## 正文

### 为什么你需要更好的命令行工具？

如果你还在用 `grep` 搜代码、`cat` 看文件、`find` 找路径，那你正在浪费时间。今天推荐 4 个工具，安装一次，终身受益。

---

### 一、fzf — 终端模糊搜索王中王

**一句话：** 装了这个，你再也不想用鼠标翻文件了。

```bash
# 安装 (macOS/Linux/WSL)
brew install fzf        # macOS
sudo apt install fzf    # Ubuntu/Debian
winget install fzf      # Windows

# 最常用的 3 个操作
**TAB**          # 搜索当前目录下所有文件名
ctrl+R          # 搜索命令历史，输入关键字即时匹配
ps aux | fzf    # 搜索进程，回车直接 kill
```

**实用场景：** 在几百个文件中找那个改过的配置文件？敲 `**TAB`，打几个字母就定位了。

> **AI 提示词模板：**
> ```
> 我装了 fzf，但记不住高级用法。列出 fzf 最实用的 5 个快捷键和对应的功能说明，给出具体例子。输出成表格。
> ```

---

### 二、ripgrep (rg) — 比 grep 快 10 倍的代码搜索

**一句话：** 搜代码用 grep 就像开拖拉机，rg 才是跑车。

```bash
# 安装
brew install ripgrep    # macOS
sudo apt install ripgrep # Ubuntu
# Windows: 下载 exe 或 scoop install ripgrep

# 常用命令
rg "TODO" src/                     # 在 src 中搜索所有 TODO
rg -c "def " --type py             # 统计 Python 文件中 def 出现次数
rg -l "import" --type js | head    # 列出包含 import 的 JS 文件

# 自动忽略 .gitignore 中的文件，不用加 --exclude-dir
```

**为什么用它？** 默认跳过 `.gitignore`、`.git` 目录，支持文件类型过滤。一个 `rg` 能替代大多数 IDE 搜索。

> **AI 提示词模板：**
> ```
> 我在项目中用 rg 搜代码。我经常需要 [描述需求，如"搜所有包含 API 调用的 Python 文件，排除 test 目录"]。
> 告诉我对应的 rg 命令怎么写，并解释每个参数的作用。
> ```

---

### 三、bat — 终于有人把 cat 做得像样了

**一句话：** cat 是黑白电视，bat 是 4K 高清。

```bash
# 安装
brew install bat         # macOS
sudo apt install bat     # Ubuntu（注意命令名是 batcat）
# Windows: scoop install bat

# 常用命令
bat file.py              # 带行号 + 语法高亮查看文件
bat --show-all log.txt   # 显示不可见字符（空格、换行、制表符）
bat -A config.json       # 同 --show-all 的简写

# 和 grep 配合使用
rg "error" server.log | bat -l log
```

**实用技巧：** 把 `bat` 设置为 git diff 的 pager，看 diff 带语法高亮：

```bash
git config --global core.pager "bat -l diff"
```

> **AI 提示词模板：**
> ```
> 我装好了 bat，想把它集成到我的日常工具链里。
> 告诉我如何设置：1) 让 bat 替代 cat 作为默认查看器
> 2) 和 fzf 组合实现文件预览 3) 自定义主题配色。
> 给出完整 ~/.bashrc 或 ~/.zshrc 配置代码。
> ```

---

### 四、jq — 终端 JSON 处理瑞士军刀

**一句话：** 你会遇到 JSON，遇到 jq 后你就不怕 JSON 了。

```bash
# 安装
brew install jq          # macOS
sudo apt install jq      # Ubuntu
winget install jqlang.jq # Windows

# 实用性拉满的 3 个例子
curl api.github.com/repos/owner/repo | jq '.stargazers_count'
# 输出：1234（一行命令查 GitHub 星标数）

cat package.json | jq '.dependencies | keys[]'
# 输出所有依赖包名，一行一个

cat data.json | jq '[group_by(.category)[] | {category: .[0].category, count: length}]'
# 按 category 分组统计数量
```

**一句话总结：** `jq` 就像 SQL 但不需要数据库，任何 JSON 都能用。

> **AI 提示词模板：**
> ```
> 我有一条 JSON 数据：{数据描述，如 "users 数组，每个元素有 name、age、city 字段"}。
> 我想按 city 分组，统计每个城市的人数，按人数降序排列。
> 请告诉我对应的 jq 命令，并解释每一步做了什么。
> ```

---

### 五（附赠）：四合一终极用法

把四个工具组合起来，威力翻倍：

```bash
# 用 rg 搜代码 → 用 fzf 选文件 → 用 bat 查看
rg -l "debug" src/ | fzf --preview "bat --color=always {}"

# 用 curl 拉 JSON → 用 jq 解析 → 用 fzf 筛选
curl -s https://api.github.com/repos/owner/repo/issues | jq '.[].title' | fzf
```

这行命令就是你的**终端 IDE**。不用打开 VS Code，不碰鼠标，全键盘操作。

---

## 一句话分享

> "好的工具链，不是让你做更多，而是让你做更少。"

---

## 发布后检查清单

- [ ] 文章已保存到本地
- [ ] 已推送到 GitHub pages
- [ ] 掘金新号已尝试发布（手动）
- [ ] 钱包已记账
