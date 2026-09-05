#!/usr/bin/env bash
# 简历 MD -> PDF 一键构建
#
# 用法：
#   bash scripts/build-pdf.sh Resume.md      Resume.pdf
#   bash scripts/build-pdf.sh Resume-Lite.md Resume-Lite.pdf
#
# 链路：md2html.py（零依赖 MD->HTML，注入四层 CSS）-> Edge headless 打印 -> pdf-check.py 校验
#
# 注意：Edge 必须锁定版本目录的绝对路径。现有 PDF 的 Producer 是 Skia/PDF m150/m151，
# 而系统 Edge 主程序恰为 151.0.4129.107；Chrome 是 152，跨版本会导致断行与分页漂移。

set -euo pipefail

EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/151.0.4129.107/msedge.exe"
PYTHON="C:/Users/hbk/.workbuddy/binaries/python/versions/3.13.12/python.exe"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$ROOT/_build"
PROFILE="$BUILD/.edge-profile"

if [ $# -lt 2 ]; then
  echo "用法: bash scripts/build-pdf.sh <input.md> <output.pdf>" >&2
  exit 1
fi

# Edge headless 打印是异步的：命令返回时文件往往尚未写完（甚至尚未创建）。
# 必须轮询等待文件出现且大小在两次采样间保持稳定，否则会误判为失败。
wait_for_pdf() {
  local f="$1" i cur prev=-1
  for i in $(seq 1 60); do            # 最多等 30 秒
    if [ -f "$f" ]; then
      cur=$(stat -c %s "$f" 2>/dev/null || echo 0)
      if [ "$cur" -gt 0 ] && [ "$cur" = "$prev" ]; then
        return 0
      fi
      prev=$cur
    fi
    sleep 0.5
  done
  return 1
}

MD="$1"
OUT="$2"
BASE="$(basename "${MD%.md}")"

[ -f "$MD" ] || { echo "找不到输入文件: $MD" >&2; exit 1; }
[ -x "$EDGE" ] || { echo "找不到 Edge 151: $EDGE" >&2; exit 1; }

mkdir -p "$BUILD" "$PROFILE"

echo "[1/3] MD -> HTML  $MD"
# 注意：PYTHON 是 Windows 原生程序，POSIX 路径 /d/Resume 会被误解析为 D:\d\Resume，
# 因此传给它的所有路径都必须先经 cygpath -w 转换。
"$PYTHON" -X utf8 "$(cygpath -w "$ROOT/scripts/md2html.py")" \
  "$(cygpath -w "$MD")" -o "$(cygpath -w "$BUILD/$BASE.html")"
echo "      -> $BUILD/$BASE.html"

echo "[2/3] HTML -> PDF (Edge 151 headless)"
rm -f "$OUT"
"$EDGE" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --no-first-run \
  --no-default-browser-check \
  --disable-extensions \
  --disable-background-networking \
  --user-data-dir="$(cygpath -w "$PROFILE")" \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=8000 \
  --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --print-to-pdf="$(cygpath -w "$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")")" \
  "file:///$(cygpath -m "$BUILD/$BASE.html")" \
  >/dev/null 2>&1 || true

if ! wait_for_pdf "$OUT"; then
  echo "      PDF 生成失败（等待 30 秒后仍为空或不存在）。" >&2
  echo "      常见原因：--user-data-dir 与已运行的 Edge 实例冲突。" >&2
  echo "      请执行 rm -rf '$PROFILE' 后重试。" >&2
  exit 1
fi
echo "      -> $OUT ($(stat -c %s "$OUT") bytes)"

echo "[3/3] 校验"
"$PYTHON" -X utf8 "$(cygpath -w "$ROOT/scripts/pdf-check.py")" "$(cygpath -w "$OUT")"
