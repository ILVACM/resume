# strategy.md — 简历编写与投递策略

> **定位**：简历**实例**（`Resume-{目标}.md`，区别于母版 `Resume.md`）的定制操作流程唯一权威文档。
> **分工**：母版维护走 `AGENTS.md` §3.1；实例登记见 [`INDEX.md`](INDEX.md) §2；投递 tag 规范与台账见 [`TargetCompanies.md`](TargetCompanies.md)。

## 1. 定制投递流程（实例全流程）

1. **选取目标**：从 [`TargetCompanies.md`](TargetCompanies.md) 按公司性质分组选取目标公司。
2. **复制模板**：复制 `Resume-Lite.md`，重命名为 `Resume-{目标}.md`（如 `Resume-ByteDance.md`）。禁止直接改动模板。
3. **填充内容**：基于母版 `Resume.md` 的内容替换骨架条目，按目标岗位裁剪详略（实例内容偏离母版属定制的意义，结构基准仍源自模板）。
4. **构建 PDF**：`bash _temp/scripts/build-pdf.sh Resume-{目标}.md _output/Resume-{目标}.pdf`，输出至 `_output/`。
5. **登记实例**：立即在 [`INDEX.md`](INDEX.md) §2 台账登记（只记 md 源文件，PDF 产物不入账），提交 `build(resume): 生成 XX 投递版 PDF`。
6. **投递打 tag**：每次实际投递前**必须**打投递快照 tag 并在 [`TargetCompanies.md`](TargetCompanies.md) 的 tag 台账登记（格式与细则见该节）。

## 维护说明

- 新目标公司优先参考 `TargetCompanies.md` 分组与 `INDEX.md` §1「相关领域」做项目匹配。
- 实例内容偏离母版属定制的意义；结构基准仍源自母版/Lite 模板。
