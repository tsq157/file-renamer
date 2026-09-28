# file-renamer 📁

一个零依赖的 Python 命令行工具，帮你批量重命名文件。

**特点**：默认「预览模式」只显示将要改的名字、不会真正改动文件，加上 `--apply` 才执行——新手友好，不会误伤文件。

## 安装要求

- Python 3.7+（无需安装任何第三方库）

## 快速开始

```bash
# 预览：给所有文件加前缀 IMG_（不会真的改）
python rename.py add-prefix "IMG_" --folder ./照片

# 确认无误后，加 --apply 真正执行
python rename.py add-prefix "IMG_" --folder ./照片 --apply
```

## 功能

| 命令 | 作用 | 示例 |
|------|------|------|
| `add-prefix` | 加前缀 | `python rename.py add-prefix "IMG_" -f ./照片` |
| `add-suffix` | 加后缀（扩展名之前） | `python rename.py add-suffix "_备份" -f ./docs` |
| `replace` | 替换字符 | `python rename.py replace " " "_" -f ./报告` |
| `sequence` | 按序号命名 | `python rename.py sequence "旅行照" -f ./旅行` |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--folder` / `-f` | 目标文件夹，默认当前目录 |
| `--apply` | 真正执行改名（不加则只预览） |

## 示例

把一堆照片从 `a.jpg`、`b.jpg` 改成 `旅行照_001.jpg`、`旅行照_002.jpg`：

```bash
python rename.py sequence "旅行照" --folder ./旅行 --apply
```

## License

MIT
