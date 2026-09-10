#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 回归校验：页数 / Producer / 字体集合 / 块引用背景与边框

用法：
    python scripts/pdf-check.py Resume.pdf [--max-pages N]

判据说明：
  - Producer 应为 Skia/PDF m15x（Chromium 打印引擎签名），证明走的是 Edge/Chrome 路线
  - 出现 ArialMT  = 页眉页脚未去掉（页眉页脚模板固定用 Arial）
  - 出现 KaiTi    = 字体 fallback 与既有 PDF 不一致，标题字形变宽会导致页数变化
  - 缺 .498/.4784 = 块引用的灰底与蓝色左边框未绘制（printBackground 未生效）
"""

import re
import sys
import zlib

# 既有 PDF 的基准字体集合（去页眉页脚后）
EXPECTED_FONTS = {'TimesNewRomanPSMT', 'TimesNewRomanPS-BoldMT', 'FangSong', 'Consolas'}


def extract_streams(data):
    streams = []
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
        try:
            streams.append(zlib.decompress(m.group(1)))
        except Exception:
            pass
    return streams


def main():
    if len(sys.argv) < 2:
        print('用法: python scripts/pdf-check.py <file.pdf>', file=sys.stderr)
        return 1

    path = sys.argv[1]

    # 可选页数上限：仅当显式传入 --max-pages N 时判定（母版多页不受影响）
    max_pages = None
    if '--max-pages' in sys.argv:
        i = sys.argv.index('--max-pages')
        try:
            max_pages = int(sys.argv[i + 1])
        except (IndexError, ValueError):
            print('用法错误: --max-pages 需要一个整数参数', file=sys.stderr)
            return 1

    data = open(path, 'rb').read()

    counts = re.findall(rb'/Count\s+(\d+)', data)
    pages = int(counts[-1]) if counts else 0

    m = re.search(rb'/Producer\s*\(([^)]*)\)', data)
    producer = m.group(1).decode('latin-1') if m else '(未知)'

    # 子集嵌入的字体名形如 BAAAAA+FangSong，需剥离前缀后再比对
    def strip_subset(name):
        return name.split('+', 1)[1] if '+' in name else name

    fonts = sorted(set(strip_subset(f.decode('latin-1'))
                       for f in re.findall(rb'/BaseFont\s*/([A-Za-z0-9+\-,_#]+)', data)))

    streams = extract_streams(data)
    has_gray_bg = any(b'.498' in s for s in streams)      # rgba(127,127,127,.1) 灰底
    has_blue_border = any(b'.4784' in s for s in streams)  # rgba(0,122,204,.5) 蓝色左边框

    print('文件     : %s' % path)
    print('页数     : %d' % pages)
    print('Producer : %s' % producer)
    print('字体     : %s' % ', '.join(fonts))
    print('块引用   : 灰底=%s 蓝框=%s' % ('有' if has_gray_bg else '无',
                                     '有' if has_blue_border else '无'))
    print('-' * 60)

    problems = []
    warnings = []

    if pages == 0:
        problems.append('未能解析页数，PDF 可能损坏')
    if max_pages is not None and pages > max_pages:
        problems.append('页数 %d 超过上限 %d（字数闸门可能失效，请复核字数预算）' % (pages, max_pages))
    if 'Skia/PDF' not in producer:
        warnings.append('Producer 不是 Skia/PDF，可能不是 Chromium 打印产物（%s）' % producer)
    if not has_gray_bg or not has_blue_border:
        problems.append('块引用灰底/蓝框缺失 -> printBackground 未生效，'
                        '请检查 CSS 中的 print-color-adjust 规则')

    font_set = set(fonts)
    if 'ArialMT' in font_set:
        warnings.append('出现 ArialMT -> 页眉页脚未去掉')
    if any('KaiTi' in f for f in font_set):
        warnings.append('出现 KaiTi -> 字体 fallback 与既有 PDF 不一致，'
                        '标题字形变宽可能导致页数变化')
    unexpected = font_set - EXPECTED_FONTS - {'ArialMT'}
    unexpected = {f for f in unexpected if 'KaiTi' not in f}
    if unexpected:
        warnings.append('出现预期外字体: %s' % ', '.join(sorted(unexpected)))

    for w in warnings:
        print('[WARN ] %s' % w)
    for p in problems:
        print('[ERROR] %s' % p)

    if problems:
        print('\n校验失败')
        return 1
    if warnings:
        print('\n通过（有 %d 条警告）' % len(warnings))
    else:
        print('\n通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
