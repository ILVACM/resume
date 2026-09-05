# 操作日志

> 本文件记录仓库的所有重要操作。Agent 每次文件操作后**必须**追加一行（规则见 `AGENTS.md` §3.4）；人工操作建议同步记录，便于对账。新条目追加在表格底部。

| 日期时间             | 操作者   | 操作                                                                                                                                                                        | 涉及路径                                                                   | 备注                                                 |
| ---------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------- |
| 2026-09-05 21:35 | 人工    | 重命名 `资料/` 为 `docs/`，删除根目录 `PDF-styles.css`                                                                                                                                | docs/、PDF-styles.css                                                   | md2html.py 对后者有优雅降级，构建链路不受影响                       |
| 2026-09-05 21:35 | Agent | 目录重整收尾：git 层面确认 rename；`scripts/` 移入 `_temp/scripts/` 并修正构建脚本路径；创建本日志                                                                                                     | docs/、\_temp/scripts/、AGENTS.md、README.md、Projects-Index.md、.gitignore | 按 AGENTS.md 目录职责规定执行                               |
| 2026-09-05 21:50 | Agent | 目录职责重整落地：AGENTS.md「其他目录」改为目录职责表格、新增 §3.4 操作日志与 §6 图表规范、删除 §7 版本记录、ASCII 图改 mermaid、全文 `资料/`→`docs/`、`scripts/`→`_temp/scripts/`；README.md、Projects-Index.md、.gitignore 同步 | AGENTS.md、README.md、Projects-Index.md、.gitignore                       | 方案经人工确认（选 a：scripts 不入库）；AGENTS.md 字符数 4321 < 8000 |
| 2026-09-05 22:53 | Agent | 重命名 Projects-Index.md → docs/INDEX.md，扩展为统一索引台账（§1 项目成果 / §2 子版本简历实例仅记 md / §3 投递 tag 台账，迁入原 AGENTS.md §4.2）；AGENTS.md 引用路径与 Tag 规范指向同步 | docs/INDEX.md、AGENTS.md | 用户指令：PDF 产物不入账；README.md 已被人工删除，不在本轮范围 |
| 2026-09-05 23:59 | Agent | 精简 AGENTS.md：删派生关系文字行（mermaid 已表达）、三层说明压缩为一句核心约束、删 §5「索引先行」「只读敬畏」重复条、写权限隔离收短、删 §3.1 第 5 步（§4.3 已覆盖）、gitignore 说明压缩、清理 DocAgent 过时 README 引用 | AGENTS.md | 用户批准 A 级方案；4219→3918 字符，零语义损失 |

