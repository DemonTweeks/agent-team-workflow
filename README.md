# Agent Team Code Reconstruction Workflow (代码反构智能体协同工作流)

🔄 本项目是一个专为 **AI 智能体** 打造的 **代码反构与知识库沉淀** 工作流技能包。它指导多智能体团队（Agent Team）协同阅读微服务底层物理代码，并逆向梳理生成标准的产品知识库文档（功能清单、PRD、接口文档及详细设计文档）。

---

## 1. 目录结构说明

```text
agent-team-workflow/
├── commands/                          # 核心执行规则模板目录
│   ├── 01-prd-rules/                  # 功能清单与需求PRD生成/审查规则
│   │   ├── feature-list-generation-rules_v1.md
│   │   ├── prd-generation_v8.md
│   │   ├── prd-completeness-check.md
│   │   └── xuqiuceshidod.md
│   ├── 02-api-rules/                  # 接口文档生成与审查规则
│   │   ├── api-doc-generation-rules_v1.md
│   │   └── api-doc-reconstruction-review-rules_v1.md
│   └── 03-design-rules/               # 详细设计文档生成与审查规则
│       ├── design-doc-reconstruction-rules_v2.md
│       └── design-doc-reconstruction-review-rules_v2.md
├── reference-docs/                    # 参考文档与总览说明
│   └── workflow-overview.md           # 流程架构图及实践背景介绍
├── .gitignore                         # Git 忽略配置文件
├── .env.example                       # 环境变量配置示例
└── skill.md                           # 智能体技能核心定义文件 (包含 YAML Metadata 及中文指令)
```

---

## 2. 快速开始与配置

为了运行本工作流，您需要首先配置本地的路径环境变量：

### 第一步：创建本地配置文件
复制根目录下的 `.env.example` 并命名为 `.env`：
```bash
cp .env.example .env
```

### 第二步：配置环境变量
编辑 `.env` 文件，将其中的路径修改为您本地对应的实际路径（请使用绝对路径，以下为脱敏示例）：
*   `CODE_ROOT`：指向您本地待分析的微服务源代码物理目录（例如：`/path/to/your/source-code`）。
*   `RULES_ROOT`：指向本仓库的 `commands` 文件夹所在的绝对路径（例如：`/path/to/agent-team-workflow/commands`）。
*   `OUTPUT_ROOT`：指向用于保存生成知识库文档的输出目标绝对路径（例如：`/path/to/your/output/knowledge`）。

---

## 3. 在 AI 智能体中使用本技能

### 3.1 载入技能
根据智能体技能加载机制，该技能可以通过将 `skill.md` 放置到您的工作区技能路径中进行加载：
*   **工作区特定技能**：将此仓库或 `skill.md` 软链接至您的 `<project_root>/skills/` 下。
*   **全局技能**：放置在您的全局智能体技能目录中。

### 3.2 智能体执行过程
在智能体执行时，系统会读取 `skill.md` 中的 YAML 头部，加载所需环境变量：
*   **阶段 0**：调用功能清单规则在 `${OUTPUT_ROOT}/knowledge/功能清单.md` 生成系统全景框架。
*   **阶段 1-2**：根据功能清单，逐个模块串行逆向输出 PRD，并进行 DoD 测试准入合规性自检。
*   **阶段 3-4**：对通过 PRD 审核的模块，读取后端接口生成接口文档并开展字段级别审查。
*   **阶段 5-6**：分析底层方法链条和事务逻辑，生成微服务详细设计文档并进行审核闭环。
