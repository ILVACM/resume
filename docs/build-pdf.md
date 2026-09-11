# build-pdf.md — PDF 构建指引（独立可选操作）

> **本文档职能**：**PDF 构建操作的唯一权威文档**。凡涉及把简历 markdown 构建为 PDF 的命令、环境、参数、校验与产物落点，一律以本文件为准。
> **触发条件**：本操作**不自动触发** —— 仅当**提示词显式要求**时执行。它与「实例构建」「投递快照」**平级**，同属可选操作；体系内**不存在**"做了实例构建就必须构建 PDF""投递快照包含构建 PDF"这类关联包含关系。
> **分工**：实例构建（阶段 A）与投递快照（阶段 B）的引导见 [`strategy.md`](strategy.md)；实例登记见 [`INDEX.md`](INDEX.md) §2；投递 tag 规范见 [`tag.md`](tag.md)，台账见 [`TargetCompanies.md`](TargetCompanies.md)；协作规则见 [`AGENTS.md`](../AGENTS.md)。

## 1. 适用范围

| 输入 md | 说明 | 字数闸门 | 页数上限 |
|---|---|---|---|
| `Resume.md` | 母版（完整版，多页合法） | **自动豁免** | 不判定 |
| `Resume-Lite.md` | 基本模板 | **自动豁免** | 不判定 |
| `Resume-{目标}-{版本}-base.md` | 实例本体 | 生效（≤2200） | **≤2 页** |
| `Resume-{目标}-{版本}-{投递公司名称}-{YYYYMMDD}[-{N}].md` | 投递副本 | 生效（≤2200） | **≤2 页** |

> 豁免与页数判定均按**文件名精确匹配**（`=` 比较），实例与投递副本不会被误豁免。
> **投递副本 PDF 非必需**：投递快照（阶段 B）只产出 md 与台账，不产 PDF；投递副本的 PDF 仅在提示词显式要求「PDF 构建」时另行构建。

## 2. 单一命令

```bash
bash _temp/scripts/build-pdf.sh <input.md> <output.pdf>
```

示例：

```bash
# 实例
bash _temp/scripts/build-pdf.sh Resume-金融科技-v1.0-base.md _output/Resume-金融科技-v1.0-base.pdf
# 投递副本
bash _temp/scripts/build-pdf.sh Resume-金融科技-v1.0-招银网络-20260910.md _output/Resume-金融科技-v1.0-招银网络-20260910.pdf
# 母版（重建）
bash _temp/scripts/build-pdf.sh Resume.md _output/Resume.pdf
```

## 3. 构建链路

| 阶段 | 组件 | 作用 |
|---|---|---|
| 1/3 | `_temp/scripts/md2html.py` | 零依赖 MD→HTML，注入 CSS（styles/ 下 3 个 + 可选 `_temp/PDF-styles.css` + 内联 PAGE_CSS，最多 5 层；含打印样式） |
| 2/3 | **Edge 151 headless** | `--print-to-pdf` 打印为 PDF |
| 3/3 | `_temp/scripts/pdf-check.py` | 回归校验：页数 / Producer / 字体集 / 块引用灰底与蓝框 |

## 4. 环境前置（硬性）

脚本依赖以下三项，**环境不符时停止并报告，不得降级尝试其他版本或工具**：

| 依赖 | 要求 |
|---|---|
| **Edge** | 必须为 **151.0.4129.107**（绝对路径硬编码于脚本内）。系统 Chrome 152 会造成**断行与分页漂移** |
| **Python** | managed Python（脚本内 `$PYTHON` 绝对路径硬编码，不依赖 PATH） |
| **Git Bash** | 提供 `cygpath`（Windows 原生 Python 会把 `/d/Resume` 误解析为 `D:\d\Resume`，故所有传入 Python 的路径须先经 `cygpath -w` 转换） |

**本机实测的两条环境坑**（操作前留意）：

- **PATH 可能缺 coreutils**：若 `tr`/`wc`/`ls`/`sed`/`cygpath`/`stat` 报 `command not found`，先执行
  `export PATH="/c/Program Files/Git/usr/bin:/c/Program Files/Git/bin:$PATH"`（仅对当次调用生效）。
- **环境变量可能不被传递**：在部分工具沙箱中 `export VAR=x` 后子 shell 读不到 → 依赖环境变量的行为（如 `RESUME_MAX_CHARS` 覆盖）**可能无法在沙箱内实测**，此时改用 `bash -x` 追踪实际展开的命令行来验证分支接线。

## 5. 字数闸门（构建前）

统计口径（**唯一口径，禁止替代实现**）：

```
去空白码点数 = len(''.join(text.split()))      # Python 码点计数，含 markdown 标记
```

> **禁止使用 `tr -d '[:space:]' | wc -m`**：本机 `wc -m` 按**字节**计（中文 1 字 = 3），会得到约 **1.85 倍**偏大的数值（实测 `Resume-Lite.md`：码点 578 / 字节 1072）。

| 行为 | 表现 |
|---|---|
| 超上限 | 打印 `[拦截]` → **退出码 2**（脚本内 `exit 2`）→ **不生成 PDF** |
| **超过**上限 90%（严格大于；恰 90% 不预警） | 打印 `[WARN]` 预警，不拦截 |
| 未超限 | 打印 `[闸门] 字数 N / 上限 M`，继续构建 |
| 母版 / Lite | 打印 `[闸门] 已豁免：…`，跳过检查 |

- **上限值**：**唯一定义源**为 [`strategy.md`](strategy.md)「字数预算」表（**当前 2200**）。本文件各处的 2200 仅为便于操作而列出的**当前值**，**两者不一致时以 `strategy.md` 字数预算表为准**；修改阈值须同步脚本内默认值。
- **临时覆盖**：环境变量 `RESUME_MAX_CHARS=N`；`=0` 表示**关闭**闸门。
- **超限处置**：属预算失效的异常情况——**停止并报告人工**，由人工决定裁剪，**不自动截断**。

## 6. 页数兜底（构建后）

```bash
"$PYTHON" -X utf8 _temp/scripts/pdf-check.py <file.pdf> [--max-pages N]
```

（$PYTHON 为脚本内硬编码的 managed Python 绝对路径，见 §4 环境前置。）

- `build-pdf.sh` 对**除母版 `Resume.md` 与模板 `Resume-Lite.md` 之外的任何输入**自动追加 `--max-pages 2`（按文件名判定，**且未设 `RESUME_MAX_CHARS=0`**）；**母版与 Lite 不传**，故多页母版不会被误报。
- 页数 > N → 输出 `[ERROR] 页数 X 超过上限 N（字数闸门可能失效，请复核字数预算）`，末行「校验失败」，**退出码 1**。
- 该参数**仅在显式传入时判定**；不传则只做页数解析与展示。

## 7. 产物落点

| 产物 | 落点 | 说明 |
|---|---|---|
| **正式产物**（母版 / Lite / 实例 base / 投递副本 PDF） | **`_output/`** | `AGENTS.md` §1 规定的**唯一结果输出目录** |
| **校验用临时构建**（测试稿、页数验证稿及其 PDF/HTML） | **`_temp/build/`** | 用完**清理**：md / html / pdf 一并删除，保留 `.edge-profile` |

## 8. 退出码速查

| 码 | 含义 | 触发点 |
|---|---|---|
| `0` | 通过 | 构建成功且 pdf-check 通过 |
| `1` | 前置不符 / 生成失败 / 校验失败 | 参数不足、缺输入 md、缺 Edge 151、等待 30 秒 PDF 仍空、pdf-check 校验失败（含 `--max-pages` 非整数、页数解析为 0、块引用灰底/蓝框缺失） |
| `2` | 字数超限拦截 | 字数闸门（实例／投递副本，>2200） |

> 注：`wait_for_pdf` 内部 `return 1` 经主流程映射为 `exit 1`，不单独成码；pdf-check 通过返回 0。

## 9. 常见失败与既有告警

**PDF 生成失败**（脚本报"等待 30 秒后仍为空或不存在"）——最常见原因是 `--user-data-dir` 与已运行的 Edge 实例冲突：

```bash
rm -rf _temp/build/.edge-profile    # 清理后重试
```

**既有告警（非缺陷，校验仍通过）**：

- 构建时报 `[warn] 缺少样式层: <绝对路径>/PDF-styles.css`（脚本打印**绝对路径**）——该层为可选覆盖，其余样式层已生效；
- 校验时报 `[WARN] 出现预期外字体: SegoeUI…`——不影响分页与块引用渲染（灰底/蓝框均正常）。

## 10. 与 strategy.md 的分工

| 关注点 | 归属 |
|---|---|
| 实例内容怎么选、怎么填、怎么校验（方案选择 / 内容构建 / 实例校验） | [`strategy.md`](strategy.md) |
| 实例体量上限（字数预算，**保证一旦构建必 ≤2 页**） | [`strategy.md`](strategy.md)「字数预算」 |
| **怎么把 md 变成 PDF**（命令 / 环境 / 闸门 / 页数兜底 / 产物落点） | **本文件** |

> 顺序执行提示：Agent 可在同一提示词内依次执行「实例构建 → PDF 构建」，但这是**提示词显式要求**的结果，**不得由管理体系自行推断或级联触发**。
