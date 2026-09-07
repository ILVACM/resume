# strategy.md — 简历编写与投递策略

> **定位**：简历**实例**（`Resume-{目标}.md`，区别于母版 `Resume.md`）的定制操作流程唯一权威文档。
> **分工**：母版维护走 `AGENTS.md` §3.1；实例登记见 [`INDEX.md`](INDEX.md) §2；投递 tag 规范见 [`tag.md`](tag.md)，日志见 [`TargetCompanies.md`](TargetCompanies.md)。

## 1. 定制投递流程（两阶段）

> **实例构建**与**投递快照**是两个相对独立的阶段：构建产出可投的实例版本；投递快照基于任一已构建的 `active` 实例执行——可重复、构建后不投也合法、投递无需重新构建。

### 阶段 A：实例构建（产出一个可投版本）

1. **选取目标**：从 [`TargetCompanies.md`](TargetCompanies.md) 按公司性质分组选取目标公司。
2. **复制模板**：复制 `Resume-Lite.md`，重命名为 `Resume-{目标}.md`（如 `Resume-ByteDance.md`）。禁止直接改动模板。
3. **填充内容**：基于母版 `Resume.md` 的内容替换骨架条目，按目标岗位裁剪详略（实例内容偏离母版属定制的意义，结构基准仍源自模板）。
4. **构建 PDF**：`bash _temp/scripts/build-pdf.sh Resume-{目标}.md _output/Resume-{目标}.pdf`，输出至 `_output/`。
5. **登记实例**：立即在 [`INDEX.md`](INDEX.md) §2 台账登记（只记 md 源文件，PDF 产物不入账，状态 `active`），提交 `build(resume): 生成 XX 投递版 PDF`。

### 阶段 B：投递快照（基于已有实例的一次投递）

前提：存在任一 `active` 状态的实例（刚构建的，或历史构建的——**无需重新构建**）。

1. **选取实例版本**：从 `INDEX.md` §2 的 `active` 实例中选定本次投递所用的文件；如需内容调整，先回阶段 A 迭代出新版本。
2. **打投递快照 tag**：`git tag v{版本}-{目标公司}-{YYYYMMDD}`——tag 粒度是**投递事件**，「目标」写实际投递的公司名（即使实例的目标指向是一类公司）；格式与铁律见 [`tag.md`](tag.md)。
3. **记录投递日志**：在 [`TargetCompanies.md`](TargetCompanies.md) 的投递日志追加一行（日期 / 简历文件 / 目标公司），不覆盖旧记录。
4. **更新状态**：公司清单中该公司的「投递简历 / 状态」列更新为最新进展（`投递中` / `一面` / `二面` / `offer` / `挂`）；`INDEX.md` §2 该实例的「对应 tag」列更新为**最新一次**投递的 tag。

## 维护说明

- 新目标公司优先参考 `TargetCompanies.md` 分组与 `INDEX.md` §1「相关领域」做项目匹配。
- 实例内容偏离母版属定制的意义；结构基准仍源自母版/Lite 模板。
