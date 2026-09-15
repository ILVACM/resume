# Huang Bokai · Resume & Application Management System

> **Huang Bokai** (Male) | Guangdong University of Technology · School of Computer Science · Software Engineering (B.Eng., Class of 2027)
> **Career Objective**: AI Application Engineer / Backend Engineer / Software Engineer (AI + System Integration)
> **Phone**: 13600323338 | **Email**: 3347620766@qq.com | **Homepage**: [github.com/ILVACM](https://github.com/ILVACM) | [gitee.com/ILVACM](https://gitee.com/ILVACM)

## Education

**Guangdong University of Technology** | School of Computer Science | Software Engineering (B.Eng., Class of 2027) | Sep 2023 - Present

- **Algorithms**: Selected into the university ACM Algorithm Training Team in the first semester of freshman year (one of 19 admitted)
- **Hardware Extension**: Joined the university's "Huawei-Ascend" Innovation Studio (embedded systems track), focusing on hardware-system integration
- **Research Experience**: Joined the Guangdong Provincial Engineering Center for Physical Information Fusion (National-Local Joint Engineering Center) as an undergraduate researcher, advised by Associate Prof. Huang Guoheng

## Skills

| Area | Details |
|---|---|
| Languages | Python, C/C++, Java, SQL, Shell |
| AI Engineering | LangChain; hands-on delivery of RAG (retrieval-augmented generation) pipelines and Multi-Agent task orchestration; familiar with on-device deployment of computer-vision models |
| Databases & Middleware | MySQL, PostgreSQL / TimescaleDB, Redis; vector database (Milvus) API integration; JDBC / JPA backend integration |
| Systems & Edge Deployment | Linux / Windows; x86 / ARM cross-architecture adaptation; Docker containerized deployment; servers and high-performance edge computing devices |

## Experience Highlights

### Industry–Academia Collaborative Projects

**Guangzhou Power Engineering Supervision Co., Ltd. (南方电网) | Office Automation RPA Project | Oct 2024 - Jan 2025**

- Designed a JSON-based "data-template" decoupled mapping engine: template changes require only configuration edits, no code changes; integrated heterogeneous XLS/XLSX data sources
- Delivered and deployed: daily manual reporting cut from 1.5 hours to **under 3 minutes**, eliminating manual errors

**Airport Logistics Group (机场物流集团) | Smart Logistics System Iteration (Phase I/II) | Sep 2024 - Sep 2026**

- Cumulative contract value **¥900K** (Phase I ¥350K / Phase II ¥550K); independently led the full lifecycle of Phase II and **11 categories** of AI vision-based violation monitoring in the transfer area (speeding, absence from post, fainting/falls, etc.)
- Deployed models to a domestic neuromorphic edge computing box (**32 TOPS INT8**), achieving **≤200ms** single-stream latency and **≥25FPS**; built cloud-edge monitoring (Prometheus + Grafana, 15+ alert rules) with **99.5%** availability and <5 min P1 recovery

**Guangdong Jiaoke Testing Co., Ltd. (广东交科) | Rebar Diameter & Spacing Inspection Device (Prototype) | Sep 2025 - Sep 2026**

- Dual-node edge architecture (Jetson Nano for inference + OrangePi KunPeng for acquisition/conversion) with bidirectional gRPC (custom protobuf), isolating failure domains
- UNet (ResNet50) 3-class semantic segmentation + 4-channel laser ranging; pixel-to-physical conversion aligned to the 6-40mm national standard; end-to-end prototype technical validation in progress

### Academic Research Projects

**China Southern Power Grid Digital Research Institute / Jiangmen Power Supply Bureau (南网数字研究院/江门供电局) | Adaptive Target Detection & PTZ Control System for Edge Surveillance Units | Jun 2024 - Oct 2024**

- Joint research project with the China Southern Power Grid Digital Research Institute / Jiangmen Power Supply Bureau (provincially funded), targeting weak-network, GPU-less HiSilicon Hi3519DV500 NPU edge environments
- Authored the *Image Quality Assessment & Optimization Plan* (edge-side objective pre-screening + server-side Transformer NR-IQA); YOLOv8 + ByteTrack tracking with smooth PTZ control; built the WireFO-MEF dataset achieving **70%+** edge recall/precision and **80%+** subjective-objective consistency

**Guangdong Provincial Natural Science Foundation 2026 | Lightweight Diagnostic Report Generation under Modality Missing | Jun 2025 - Present**

- *Lightweight Diagnostic Report Generation under Modality Missing* (No. 2614050003331), built on a multimodal private dataset of **600+ cases** from the Sun Yat-sen University Cancer Center
- PyTorch + RAG + Multi-Agent "diagnose-verify-arbitrate" loop; independently managed the GPU server environment and the data cleaning, de-identification and ROI-cropping pipeline; assisted in drafting the grant proposal

### Internships

**Guangzhou Guangdian Information Technology Co., Ltd. (广州光点) | Python Development Intern (AI R&D Group) | Mar 2025 - Jun 2025**

- Built an all-media trending-topic tracking and AI short-video generation matrix, delivering the full "monitor → generate → compose" pipeline from scratch
- FastAPI microservices + hybrid scheduling across local vLLM and cloud APIs + Celery/Redis async orchestration; reduced per-video production from hours of manual work to **under 15 minutes**

**Guangdong Provincial Institute of Land and Resources Surveying and Mapping (广东省国土资源测绘院) | System Development Intern (Satellite Application Center) | Jul 2025 - Oct 2025**

- GDCORS intelligent knowledge base and government-enterprise on-premises RAG Q&A system over **3PB** of geospatial data, meeting strict "data never leaves the premises" compliance
- Tens of millions of document chunks stored in Milvus; HyDE + multi-route retrieval (vector + BM25) + BGE-Reranker; built an LLM-as-a-Judge evaluation system from scratch, reaching **90%+** domain Q&A accuracy

## Competitions & Honors

**2024**

- Huawei 2024 Ascend AI Innovation Competition · Most Promising Business Potential Award (University Track)
- Huawei 2024 Kunpeng Application Innovation Competition · National Semifinalist (Development Board Track)
- 17th China Collegiate Computing Competition · 3 works shortlisted at provincial level (Team Lead)
- China Southern Power Grid Internal Visual Recognition Competition (Guy-Wire Corrosion Track) · 8th Place (Team Lead)

**2023**

- PTA Ladder Team Programming Contest · 5th Place Nationwide among Universities (core member, University ACM Training Team)
- GDUT "Huawei Cup" Programming Contest · Third Prize (ranked 19th on campus; admitted to the ACM Training Team)
- 2023 "Holtek Cup" Microcontroller Application Design Competition · Provincial Second Prize
- Horse Hoof Cup (Baidu Star) Programming Contest · Provincial Third Prize

## About This Repository

A **Git-based, version-controlled resume and application management system**: `Resume.md` (the master resume, single source of truth) is the content source, from which `Resume-Lite.md` (the structural template for application instances) and per-company custom instances are derived; all PDF artifacts are output to `_output/`. Customization workflow: `docs/strategy.md`; application tag convention: `docs/tag.md`; achievements and instance ledger: `docs/INDEX.md`; target company list: `docs/TargetCompanies.md`. PDF build workflow: `docs/build-pdf.md`.

### Current Status

| Item | Status |
|---|---|
| Master resume `Resume.md` | Finalized: 7 full experiences + competitions & honors; supporting materials archived under `docs/` |
| Template `Resume-Lite.md` | Finalized: a 27-line skeleton, with project content filled from the plan library |
| Instance build plan library | **10 groups** established; the sample content is a first draft and **awaits manual review** before instances can be built |
| Custom instances | **None yet** (instance ledger empty) |
| Target companies | **203 companies / 10 groups** ready; the "Positions of Interest" column is pending |
| Output operations | **Instance build / Application snapshot / PDF build** are peer, independent; each runs only when explicitly requested |

Collaboration rules, directory responsibilities and technical details: see [`AGENTS.md`](AGENTS.md) and [`docs/`](docs/).

## License

This project adopts the open source license specified in [LICENSE](./LICENSE).

---

**Maintainer**: ILVACM | **Last Updated**: 2026
