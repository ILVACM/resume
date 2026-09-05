#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零依赖 Markdown -> HTML 转换器（简历专用子集）

设计要点：
1. 块引用"去前缀后递归"：strip_bq() 只吃一个 '>' 和一个可选空格，
   去前缀后把内部行重新喂给 render_blocks() 自身，使"段落→空引用行→
   嵌套列表→空引用行→段落"的复合结构自然复用同一套逻辑，消除特判。
2. breaks=False 语义：软换行折叠为空格，仅行尾 '\\' 或 >=2 尾空格才输出 <br>。
3. 行内渲染顺序不可调换：占位符 → 硬换行 → 转义 → HTML白名单还原 → 链接 → 加粗 → 还原占位符。
   （行内代码必须先于硬换行判断，否则母版中 `\\ 层级路径 会被误切）

用法：
    python md2html.py input.md -o output.html
    python md2html.py input.md --selftest
    python md2html.py input.md              # 输出到 stdout
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 正则常量

RE_HTML_BLOCK = re.compile(r'^\s*<(/?)(h[1-6]|div|p|br|hr)([^>]*)>(.*?)(</\1>)?\s*$', re.I)
RE_ATX = re.compile(r'^(#{1,6})\s+(.*)$')
RE_LI = re.compile(r'^(\s*)([-*+])\s+(.*)$')
RE_CODE = re.compile(r'`([^`]+)`')
RE_LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
RE_BOLD = re.compile(r'\*\*([^*\n]+)\*\*')
RE_HARD_BREAK = re.compile(r'(?:\\| {2,})$')
# 白名单内联 HTML 标签（转义后再还原，避免被当作文本）
RE_HTML_INLINE_OK = re.compile(
    r'&lt;(/?)(h[1-6]|b|i|u|em|strong|br|hr|sub|sup|span|code)(\s[^&]*?)?&gt;', re.I)

PLACEHOLDER = '\x00CODE%d\x00'

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
STYLES_DIR = SCRIPT_DIR / 'styles'
USER_CSS = ROOT / 'PDF-styles.css'


# ---------------------------------------------------------------- 工具

def read_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def strip_bq(s):
    """去掉块引用前缀：只吃一个 '>' 和一个可选空格，保留后续缩进供列表层级判定。"""
    return re.sub(r'^\s*>\s?', '', s, count=1)


# ---------------------------------------------------------------- 阶段 1：块切分

def split_blocks(lines):
    """行序列 -> 块序列。块类型：raw / heading / quote / list / para"""
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]

        if ln.strip() == '':
            i += 1
            continue

        # (a) 内联 HTML 块（母版仅 L1 的 <h1 align="center">）
        if RE_HTML_BLOCK.match(ln):
            blocks.append(('raw', ln.rstrip()))
            i += 1
            continue

        # (b) ATX 标题
        m = RE_ATX.match(ln)
        if m:
            blocks.append(('heading', len(m.group(1)), m.group(2).strip()))
            i += 1
            continue

        # (c) 块引用：连续 '>' 行，允许空引用行与缩进续行穿插
        if ln.lstrip().startswith('>'):
            j = i
            while j < n:
                s = lines[j]
                if s.strip() == '':
                    break                                  # 真空行 -> 引用结束
                if s.lstrip().startswith('>'):
                    j += 1
                    continue
                if s[:1] in (' ', '\t') and s.strip():
                    j += 1                                 # 引用内列表的懒续行
                    continue
                break
            blocks.append(('quote', [strip_bq(s) for s in lines[i:j]]))
            i = j
            continue

        # (d) 列表：连续 marker 行（含缩进续行）；空行后仍为列表项则继续
        if RE_LI.match(ln):
            j = i
            while j < n:
                s = lines[j]
                if s.strip() == '':
                    k = j + 1
                    while k < n and lines[k].strip() == '':
                        k += 1
                    if k < n and RE_LI.match(lines[k]):
                        j = k
                        continue
                    break
                if RE_LI.match(s) or (s[:1] in (' ', '\t') and s.strip()):
                    j += 1
                    continue
                break
            blocks.append(('list', lines[i:j]))
            i = j
            continue

        # (e) 段落：连续非空行，直到空行或上述任意块起始
        j = i
        while j < n:
            s = lines[j]
            if s.strip() == '':
                break
            if (RE_ATX.match(s) or RE_LI.match(s)
                    or s.lstrip().startswith('>') or RE_HTML_BLOCK.match(s)):
                break
            j += 1
        blocks.append(('para', lines[i:j]))
        i = j
    return blocks


# ---------------------------------------------------------------- 阶段 2/3：块与列表渲染

def render_blocks(lines):
    return ''.join(render_block(b) for b in split_blocks(lines))


def render_block(b):
    kind = b[0]
    if kind == 'raw':
        return b[1] + '\n'
    if kind == 'heading':
        return '<h%d>%s</h%d>\n' % (b[1], inline(b[2]), b[1])
    if kind == 'quote':
        return '<blockquote>\n' + render_blocks(b[1]) + '</blockquote>\n'
    if kind == 'para':
        return '<p>' + join_lines(b[1]) + '</p>\n'
    if kind == 'list':
        return render_list(b[1])
    return ''


def join_lines(lines):
    """breaks=False 语义：软换行折叠为空格，硬换行才 <br>"""
    out = []
    for idx, raw in enumerate(lines):
        text, hard, codes = prepare_line(raw)
        out.append(inline(text, codes))
        if hard:
            out.append('<br>')
        elif idx < len(lines) - 1:
            out.append(' ')
    return ''.join(out)


def render_list(lines):
    """按 marker 缩进建树。子项缩进 >= 父 marker 宽度即可（故 2 空格成立）。"""
    items = []                                # [indent, [lines...]]
    for ln in lines:
        m = RE_LI.match(ln)
        if m:
            items.append([len(m.group(1)), [m.group(3)]])
        elif items:
            s = ln[2:] if ln.startswith('  ') else ln.lstrip()
            items[-1][1].append(s)

    root = {'indent': -1, 'children': []}
    stack = [root]
    for indent, ls in items:
        while len(stack) > 1 and indent <= stack[-1]['indent']:
            stack.pop()
        node = {'indent': indent, 'children': [], 'lines': ls}
        stack[-1]['children'].append(node)
        stack.append(node)

    def emit(node):
        if not node['children']:
            return ''
        s = '<ul>\n'
        for c in node['children']:
            inner = unwrap_single_p(render_blocks(c['lines']))
            s += '<li>' + inner + emit(c) + '</li>\n'
        return s + '</ul>\n'

    return emit(root)


def unwrap_single_p(html):
    """tight list：li 内单段落去掉 <p> 包裹，避免多余 margin"""
    s = html.rstrip('\n')
    if s.startswith('<p>') and s.endswith('</p>') and s.count('<p>') == 1:
        return s[3:-4]
    return html


# ---------------------------------------------------------------- 阶段 4：行内渲染

def prepare_line(raw):
    """① 抽行内代码为占位符 → ② 判行尾硬换行。顺序不可调换。"""
    codes = []

    def _sub(m):
        codes.append(m.group(1))
        return PLACEHOLDER % (len(codes) - 1)

    text = RE_CODE.sub(_sub, raw)
    hard = False
    m = RE_HARD_BREAK.search(text)
    if m:
        hard = True
        text = text[:m.start()]
    return text, hard, codes


def _escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(text, codes=None):
    """③转义(&先于<) → ④HTML白名单还原 → ⑤链接 → ⑥加粗 → ⑦还原行内代码"""
    if codes is None:
        codes = []
    text = _escape(text)
    text = RE_HTML_INLINE_OK.sub(
        lambda m: '<%s%s%s>' % (m.group(1), m.group(2), m.group(3) or ''), text)
    text = RE_LINK.sub(r'<a href="\2">\1</a>', text)
    text = RE_BOLD.sub(r'<strong>\1</strong>', text)
    for i, c in enumerate(codes):
        text = text.replace(PLACEHOLDER % i, '<code>' + _escape(c) + '</code>')
    return text


# ---------------------------------------------------------------- 阶段 5：HTML 骨架

PAGE_CSS = """
@page { size: A4; margin: 1.5cm 1cm 1cm 1cm; }
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
}
"""


def wrap_html(body, title):
    layers = []
    for name in ('markdown.css', 'tomorrow.css', 'markdown-pdf.css'):
        p = STYLES_DIR / name
        if p.exists():
            layers.append(read_text(p))
        else:
            print('[warn] 缺少样式层: %s' % p, file=sys.stderr)
    if USER_CSS.exists():
        layers.append(read_text(USER_CSS))
    else:
        print('[warn] 缺少样式层: %s' % USER_CSS, file=sys.stderr)
    layers.append(PAGE_CSS)

    styles = '\n'.join('<style>\n%s\n</style>' % css for css in layers)
    return (
        '<!DOCTYPE html>\n<html>\n<head>\n'
        '<meta http-equiv="Content-type" content="text/html;charset=UTF-8">\n'
        '<title>%s</title>\n%s\n</head>\n<body>\n%s</body>\n</html>\n'
        % (title, styles, body)
    )


def convert(md_text):
    body = render_blocks(md_text.splitlines())
    return body


# ---------------------------------------------------------------- 自检

def selftest(md_text, html):
    src = md_text.splitlines()
    checks = []

    def chk(name, actual, expect):
        ok = actual == expect
        checks.append((ok, name, actual, expect))

    def count(pat, s=None):
        return len(re.findall(pat, s if s is not None else html))

    def count_nested_ul(fragment):
        """用栈统计 ul 的嵌套次数（在已有 ul 内再开 ul 的次数）"""
        depth = nested = 0
        for m in re.finditer(r'<ul>|</ul>', fragment):
            if m.group(0) == '<ul>':
                if depth > 0:
                    nested += 1
                depth += 1
            else:
                depth -= 1
        return nested

    # 固定断言（母版结构特征，不随项目数量变化）
    # blockquote 共 3 个：L5-11 个人信息块(7行) / L56-79 机场物流(24行) / L102-121 省自然(20行)
    chk('<blockquote> 数量', count(r'<blockquote>'), 3)
    # br 共 5 个：L5-8 行尾反斜杠 4 个 + L27「通过 CET-4  」行尾双空格 1 个
    chk('<br> 数量（硬换行）', count(r'<br>'), 5)
    chk('邮箱尖括号已转义', count(r'&lt;3347620766@qq\.com&gt;'), 1)
    chk('教育&amp;专业背景 转义', count(r'教育&amp;专业背景'), 1)
    chk('<h1 align = "center"> 原样透传', count(r'<h1 align = "center">'), 1)
    chk('无重复转义 &amp;lt;', count(r'&amp;lt;'), 0)
    chk('无占位符残留 \\x00', count('\x00'), 0)

    # 自适应断言（随母版内容变化，与源文件保持一致即为正确）
    for lvl in (1, 2, 3, 4, 5, 6):
        pat = r'^#{%d}\s' % lvl
        expect = sum(1 for ln in src if re.match(pat, ln))
        chk('<h%d> 数量' % lvl, count(r'<h%d>' % lvl), expect)
    chk('<code> 数量', count(r'<code>'), md_text.count('`') // 2)

    # 块引用内部结构：机场物流 6 个 ul（一期/二期列表 1 个 + 核心工作外层 1 个 + 4 个子列表）
    #                 省自然 5 个 ul（外层 1 个 + 4 个子列表）
    bqs = re.findall(r'<blockquote>(.*?)</blockquote>', html, re.S)
    chk('blockquote 内 <ul> 总数', sum(b.count('<ul>') for b in bqs), 11)
    chk('blockquote 内嵌套列表数', sum(count_nested_ul(b) for b in bqs), 8)

    width = max(len(c[1]) for c in checks)
    failed = 0
    for ok, name, actual, expect in checks:
        if not ok:
            failed += 1
        print('%-4s %-*s  actual=%-6s expect=%s'
              % ('OK' if ok else 'FAIL', width, name, actual, expect))
    print('\n%d/%d passed' % (len(checks) - failed, len(checks)))
    return failed == 0


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description='零依赖 Markdown -> HTML（简历专用子集）')
    ap.add_argument('input', help='输入 .md 文件')
    ap.add_argument('-o', '--output', help='输出 .html 文件（默认 stdout）')
    ap.add_argument('--body-only', action='store_true', help='只输出 body 片段，不包裹 HTML 骨架')
    ap.add_argument('--selftest', action='store_true', help='运行结构断言')
    args = ap.parse_args()

    md_text = read_text(args.input)
    body = convert(md_text)

    if args.selftest:
        html = body
        ok = selftest(md_text, html)
        sys.exit(0 if ok else 1)

    out = body if args.body_only else wrap_html(body, Path(args.input).stem)
    if args.output:
        with open(args.output, 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print('written: %s' % args.output, file=sys.stderr)
    else:
        sys.stdout.write(out)


if __name__ == '__main__':
    main()
