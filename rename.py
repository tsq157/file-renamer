#!/usr/bin/env python3
"""
file-renamer — 文件批量重命名工具

一个零依赖的命令行工具，帮助你批量重命名文件。
默认是「预览模式」，只会打印将要执行的改名操作，不会真正改动文件；
只有加上 --apply 才会真正执行，避免误伤。

用法示例：
    python rename.py add-prefix "IMG_" --folder ./照片          # 加前缀
    python rename.py add-suffix "_备份" --folder ./docs         # 加后缀
    python rename.py replace " " "_" --folder ./报告            # 把空格替换成下划线
    python rename.py sequence "旅行照" --folder ./旅行          # 按序号命名：旅行照_001.jpg
    python rename.py add-prefix "IMG_" --folder ./照片 --apply  # 真正执行
"""

import argparse
import os
import sys


def list_files(folder):
    """返回指定文件夹里所有文件的文件名（不含子文件夹）。"""
    if not os.path.isdir(folder):
        print(f"错误：文件夹不存在 -> {folder}", file=sys.stderr)
        sys.exit(1)

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.sort()
    if not files:
        print(f"文件夹里没有文件：{folder}")
        sys.exit(0)
    return files


def build_plan(files, action, arg):
    """根据动作和参数，生成 [(旧名, 新名), ...] 的改名计划。"""
    plan = []
    for i, name in enumerate(files, start=1):
        base, ext = os.path.splitext(name)  # 拆成 主名 + 扩展名（如 .jpg）

        if action == "add-prefix":
            new_name = arg + name
        elif action == "add-suffix":
            new_name = base + arg + ext
        elif action == "replace":
            old, new = arg
            new_name = name.replace(old, new)
        elif action == "sequence":
            new_name = f"{arg}_{i:03d}{ext}"
        else:
            raise ValueError(f"未知动作：{action}")

        plan.append((name, new_name))
    return plan


def main():
    parser = argparse.ArgumentParser(
        description="文件批量重命名工具（默认预览，加 --apply 才真正执行）"
    )

    # 把 --folder 和 --apply 放进「公共参数」，让它们在任何位置都能被识别
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--folder", "-f", default=".", help="目标文件夹，默认当前目录")
    common.add_argument("--apply", action="store_true", help="真正执行改名（默认只预览）")

    parser.add_argument("--folder", "-f", default=".", help="目标文件夹，默认当前目录")
    parser.add_argument("--apply", action="store_true", help="真正执行改名（默认只预览）")

    sub = parser.add_subparsers(dest="action", required=True)

    p1 = sub.add_parser("add-prefix", parents=[common], help="给文件名加前缀")
    p1.add_argument("arg", help="要加的前缀，如 IMG_")

    p2 = sub.add_parser("add-suffix", parents=[common], help="给主名加后缀（扩展名之前）")
    p2.add_argument("arg", help="要加的后缀，如 _备份")

    p3 = sub.add_parser("replace", parents=[common], help="替换文件名中的字符")
    p3.add_argument("old", help="要被替换的字符")
    p3.add_argument("new", help="替换成的字符")

    p4 = sub.add_parser("sequence", parents=[common], help="按序号重命名，如 前缀_001.jpg")
    p4.add_argument("arg", help="序号前缀，如 旅行照")

    args = parser.parse_args()

    files = list_files(args.folder)

    # 组装动作参数：replace 有两个参数，其余只有一个
    if args.action == "replace":
        arg = (args.old, args.new)
    else:
        arg = args.arg

    plan = build_plan(files, args.action, arg)

    # 检查是否有重名冲突
    new_names = [new for _, new in plan]
    if len(new_names) != len(set(new_names)):
        print("警告：改名后会出现重名，已中止。请调整参数。", file=sys.stderr)
        sys.exit(1)

    print(f"共 {len(plan)} 个文件，{'真正执行' if args.apply else '预览模式（未改动任何文件）'}：\n")
    for old, new in plan:
        print(f"  {old}  ->  {new}")

    if not args.apply:
        print("\n提示：确认无误后，加 --apply 参数真正执行。")
        return

    # 真正执行改名
    done = 0
    for old, new in plan:
        old_path = os.path.join(args.folder, old)
        new_path = os.path.join(args.folder, new)
        os.rename(old_path, new_path)
        done += 1

    print(f"\n完成！已重命名 {done} 个文件。")


if __name__ == "__main__":
    main()
