#!/usr/bin/env python3
"""
BatchRename Pro — 智能批量文件重命名工具
版本: 1.0.0
作者: Claw Agent
用途: 批量重命名文件，支持多种模式，安全预览，一键撤销

使用方法:
  python batchrename.py preview   <目录> <模式> <参数>  # 预览不改
  python batchrename.py execute   <目录> <模式> <参数>  # 执行改名
  python batchrename.py undo      <目录>               # 撤销上次操作

模式:
  prefix   添加前缀         例: python batchrename.py execute ./files prefix "project_"
  suffix   添加后缀         例: python batchrename.py execute ./files suffix "_final"
  replace  替换文字         例: python batchrename.py execute ./files replace "old" "new"
  number   数字序号         例: python batchrename.py execute ./files number "photo_"
  regex    正则替换         例: python batchrename.py execute ./files regex "(\\d+)" "img_\\1"
  extension  改扩展名       例: python batchrename.py execute ./files extension .jpg .png
"""

import os
import sys
import re
import json
import datetime
from pathlib import Path

UNDO_FILE = ".batchrename_undo.json"


def get_files(directory):
    """获取目录中所有文件（非目录）"""
    path = Path(directory)
    if not path.exists():
        print(f"错误: 目录不存在: {directory}")
        sys.exit(1)
    files = [f for f in path.iterdir() if f.is_file() and f.name != UNDO_FILE]
    return sorted(files, key=lambda f: f.name)


def save_undo(directory, changes):
    """保存撤销信息到文件"""
    undo_path = Path(directory) / UNDO_FILE
    with open(undo_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.datetime.now().isoformat(),
            "changes": changes
        }, f, ensure_ascii=False, indent=2)


def load_undo(directory):
    """读取撤销信息"""
    undo_path = Path(directory) / UNDO_FILE
    if not undo_path.exists():
        print(f"没有可撤销的操作记录: {directory}")
        return None
    with open(undo_path, "r", encoding="utf-8") as f:
        return json.load(f)


def preview_changes(files, new_names):
    """显示预览"""
    print(f"\n{'='*60}")
    print(f"待处理文件: {len(files)} 个")
    print(f"{'='*60}")
    for old, new in zip(files, new_names):
        flag = " ✓" if old.name != new else ""
        print(f"  {old.name}  →  {new}{flag}")
    print(f"{'='*60}\n")


def mode_prefix(files, prefix):
    return [f"{prefix}{f.name}" for f in files]


def mode_suffix(files, suffix):
    names = []
    for f in files:
        stem, ext = os.path.splitext(f.name)
        names.append(f"{stem}{suffix}{ext}")
    return names


def mode_replace(files, old, new):
    return [f.name.replace(old, new) for f in files]


def mode_number(files, prefix="", start=1, digits=3):
    names = []
    for i, f in enumerate(files):
        ext = os.path.splitext(f.name)[1]
        num = str(start + i).zfill(digits)
        names.append(f"{prefix}{num}{ext}")
    return names


def mode_regex(files, pattern, replacement):
    try:
        compiled = re.compile(pattern)
    except re.error as e:
        print(f"正则表达式错误: {e}")
        sys.exit(1)
    return [compiled.sub(replacement, f.name) for f in files]


def mode_extension(files, old_ext, new_ext):
    names = []
    for f in files:
        stem, ext = os.path.splitext(f.name)
        if ext.lower() == old_ext.lower() or ext == old_ext:
            names.append(f"{stem}{new_ext}")
        else:
            names.append(f.name)
    return names


def cmd_preview(args):
    if len(args) < 2:
        print("用法: python batchrename.py preview <目录> <模式> [参数...]")
        sys.exit(1)
    directory = args[0]
    mode = args[1]
    mode_args = args[2:]
    
    files = get_files(directory)
    new_names = apply_mode(mode, files, mode_args)
    preview_changes(files, new_names)
    
    changes = [{"old": f.name, "new": n} for f, n in zip(files, new_names) if f.name != n]
    print(f"实际会改动的文件: {len(changes)} 个")
    return changes


def cmd_execute(args):
    if len(args) < 2:
        print("用法: python batchrename.py execute <目录> <模式> [参数...]")
        sys.exit(1)
    directory = args[0]
    mode = args[1]
    mode_args = args[2:]
    
    files = get_files(directory)
    new_names = apply_mode(mode, files, mode_args)
    
    changes = []
    renamed = 0
    for f, new_name in zip(files, new_names):
        if f.name != new_name:
            new_path = f.parent / new_name
            if new_path.exists():
                print(f"跳过 (目标文件已存在): {new_name}")
                continue
            os.rename(f, new_path)
            changes.append({"old": f.name, "new": new_name})
            renamed += 1
            print(f"  ✓ {f.name} → {new_name}")
    
    if changes:
        save_undo(directory, changes)
        print(f"\n成功重命名 {renamed} 个文件。")
        print(f"如需撤销，运行: python batchrename.py undo {directory}")
    else:
        print("没有文件被改动。")


def cmd_undo(args):
    if not args:
        print("用法: python batchrename.py undo <目录>")
        sys.exit(1)
    directory = args[0]
    data = load_undo(directory)
    if not data:
        return
    
    changes = data["changes"]
    print(f"撤销 {len(changes)} 个文件的改名 (来自 {data['timestamp'][:19]})...")
    for ch in changes:
        old_name = ch["old"]
        new_name = ch["new"]
        old_path = Path(directory) / old_name
        new_path = Path(directory) / new_name
        if new_path.exists() and not old_path.exists():
            os.rename(new_path, old_path)
            print(f"  ↩ {new_name} → {old_name}")
        else:
            print(f"  跳过 (文件状态异常): {new_name}")
    
    undo_file = Path(directory) / UNDO_FILE
    undo_file.unlink(missing_ok=True)
    print("撤销完成。")


def apply_mode(mode, files, args):
    mode_map = {
        "prefix": mode_prefix,
        "suffix": mode_suffix,
        "replace": mode_replace,
        "number": mode_number,
        "regex": mode_regex,
        "extension": mode_extension,
    }
    
    if mode not in mode_map:
        print(f"未知模式: {mode}")
        print("可用模式: prefix, suffix, replace, number, regex, extension")
        sys.exit(1)
    
    return mode_map[mode](files, *args)


def cmd_interactive():
    """交互模式"""
    print("\n" + "="*50)
    print("  BatchRename Pro — 交互模式")
    print("="*50 + "\n")
    directory = input("目标目录: ").strip()
    if not directory:
        print("已取消")
        return
    
    print("\n选择模式:")
    print("  1. prefix   — 添加前缀")
    print("  2. suffix   — 添加后缀")
    print("  3. replace  — 替换文字")
    print("  4. number   — 数字序号")
    print("  5. regex    — 正则替换")
    print("  6. extension— 改扩展名")
    choice = input("请输入编号 (1-6): ").strip()
    
    mode_map_ui = {"1": "prefix", "2": "suffix", "3": "replace",
                   "4": "number", "5": "regex", "6": "extension"}
    mode = mode_map_ui.get(choice)
    if not mode:
        print("无效选择")
        return
    
    extra = input("参数 (根据模式输入对应值): ").strip()
    mode_args_list = extra.split()
    
    files = get_files(directory)
    new_names = apply_mode(mode, files, mode_args_list)
    preview_changes(files, new_names)
    
    confirm = input("确认执行? (y/n): ").strip().lower()
    if confirm == "y":
        cmd_execute([directory, mode] + mode_args_list)
    else:
        print("已取消")


def main():
    if len(sys.argv) < 2:
        print("BatchRename Pro v1.0 — 智能批量文件重命名工具\n")
        print("用法:")
        print("  python batchrename.py preview   <目录> <模式> [参数]  — 预览")
        print("  python batchrename.py execute   <目录> <模式> [参数]  — 执行")
        print("  python batchrename.py undo      <目录>               — 撤销")
        print("  python batchrename.py interactive                     — 交互模式")
        print("\n模式: prefix, suffix, replace, number, regex, extension")
        print("\n示例:")
        print('  python batchrename.py preview ./photos prefix "vacation_"')
        print('  python batchrename.py execute ./docs replace "draft" "final"')
        print('  python batchrename.py execute ./files number "img_"')
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "preview":
        cmd_preview(args)
    elif cmd == "execute":
        cmd_execute(args)
    elif cmd == "undo":
        cmd_undo(args)
    elif cmd == "interactive":
        cmd_interactive()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: preview, execute, undo, interactive")


if __name__ == "__main__":
    main()
