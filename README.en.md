# Resume Management System (Resume)

## Project Introduction

This project is a professional personal resume management system, focusing on the Fall 2027 recruitment job search scenario. The system uses Markdown format to manage resume content, supports multi-version customized output, and provides complete application target management and collaboration standards.

## Directory Structure

```
Resume/
├── AGENTS.md              # Collaboration Norms and Workflow Description
├── Resume.md              # Master Resume
├── Resume-Lite.md         # Lite Resume
├── LICENSE                # Open Source License
├── docs/
│   ├── INDEX.md           # Achievements and Version Index
│   ├── LOG.md             # Operation Log
│   ├── TargetCompanies.md # Target Company List for Applications
│   └── strategy.md        # Job Hunting Strategy Document
└── _temp/scripts/         # Build Tools
    ├── build-pdf.sh       # PDF Build Script
    ├── md2html.py         # Markdown to HTML Tool
    ├── pdf-check.py       # PDF Check Tool
    └── styles/            # CSS Style Files
```

## Core Features

### 1. Multi-Version Resume Management

- **Master Resume (Resume.md)**: Complete version resume, containing all projects and experiences.
- **Lite Resume (Resume-Lite.md)**: Condensed version customized for different positions.

### 2. Application Target Management

The system maintains a clearly categorized list of application targets, covering multiple popular directions:

- AI / Large Language Models
- Embodied AI
- Machine Vision
- IoT / Smart Hardware
- Internet Tech Giants
- Enterprise Services / SaaS / Cloud
- Industry-Specific Software Development
- Government and Enterprise Informatization
- Financial Securities / FinTech

### 3. Version Output

Supports multiple output formats to meet different application scenario needs:

- **PDF Format**: Suitable for formal applications.
- **HTML Format**: Convenient for online viewing and sharing.

### 4. Collaboration Norms

The project establishes a complete workflow specification:

- Verification takes precedence over trust principle.
- Clear Git commit conventions.
- Tag management strategy.
- Multi-Agent collaboration guidance.

## Quick Start

### Environment Requirements

- Python 3.x
- Edge Browser (for PDF generation)

### Generate PDF Resume

```bash
# Execute build script
bash _temp/scripts/build-pdf.sh
```

### Markdown to HTML

```bash
# Use conversion tool
python _temp/scripts/md2html.py input.md output.html
```

## Usage Instructions

### Add New Projects

Add new project experience according to the workflow specifications defined in AGENTS.md.

### Customize Application Version Resumes

Based on the master resume, customize exclusive versions according to target companies and position requirements.

### Synchronize Updates

When the master resume is updated, synchronize updates for each application version according to specifications.

## Resume Content Overview

### Basic Information

- Education Background and Professional Skills
- Core Knowledge and Skill Stack

### Project Experience

**School-Enterprise Collaborative Projects:**
- Southern Power Grid RPA-Assisted Software Development Project (Core R&D)
- Airport Logistics Group Smart Logistics System Iteration (Project Lead)
- Reinforcement Steel Inspection Equipment Prototype R&D (Technical Lead)

**Academic Research Projects:**
- Edge Surveillance Sphere Adaptive Object Detection System (Core R&D)
- Guangdong Provincial Natural Science Foundation Project (Core Algorithm Development)

**Corporate Internships:**
- Guangzhou Lightpoint Information Technology (Python Development Intern)
- Guangdong Provincial Land and Resources Surveying and Mapping Institute (System Development Intern)

### Competitions and Honors

Records various competition awards and honorary qualifications.

## Maintenance Guide

### Version Index

All resume versions and deliverable change records can be viewed in `docs/INDEX.md`.

### Operation Log

Detailed operation change logs are saved in `docs/LOG.md`.

### Application Ledger

Tag management for each application version can be found in the application tag ledger in `docs/INDEX.md`.

## License

This project adopts the open source license specified in [LICENSE](./LICENSE).

---

**Maintainer**: ILVACM

**Last Updated**: 2025