# 操作日志

> 本文件记录仓库的所有重要操作。Agent 每次文件操作后**必须**追加一行（规则见 `AGENTS.md` §3.4）；人工操作建议同步记录，便于对账。新条目追加在表格底部。

| 日期时间 | 操作者 | 操作 | 涉及路径 | 备注 |
|---|---|---|---|---|
| 2026-09-05 21:35 | 人工 | 重命名 `资料/` 为 `docs/`，删除根目录 `PDF-styles.css` | docs/、PDF-styles.css | md2html.py 对后者有优雅降级，构建链路不受影响 |
| 2026-09-05 21:35 | Agent | 目录重整收尾：git 层面确认 rename；`scripts/` 移入 `_temp/scripts/` 并修正构建脚本路径；创建本日志 | docs/、_temp/scripts/、AGENTS.md、README.md、Projects-Index.md、.gitignore | 按 AGENTS.md 目录职责规定执行 |
