---
name: code-reconstruction-workflow
version: 1.0.0
description: 使用智能体团队（Agent Team）从微服务源代码中逆向构建产品文档（功能清单、PRD、接口文档和详细设计文档）的工作流技能。
emoji: "🔄"
requires:
  env:
    - CODE_ROOT
    - RULES_ROOT
    - OUTPUT_ROOT
  bins:
    - git
envVars:
  - name: CODE_ROOT
    required: true
    description: 微服务源代码根目录的路径。
  - name: RULES_ROOT
    required: true
    description: 规则/指令模板根目录的路径（例如 commands 文件夹）。
  - name: OUTPUT_ROOT
    required: true
    description: 保存生成的知识库文档的输出目录路径。
---

# Code Reconstruction Agent Team Workflow (代码反构智能体协同工作流)

本智能体技能定义了如何通过构建智能体协同团队（Agent Team），从微服务代码库逆向构建完整的产品知识体系文档（功能清单、PRD、接口文档、详细设计文档）。

---

## 1. 基础环境与配置路径

### 1.1 物理路径配置
*   **代码根目录**：`${CODE_ROOT}`
*   **输出根目录**：`${OUTPUT_ROOT}`

### 1.2 规则文档映射 (环境变量相对路径)
所有规则文件统一存放在 `${RULES_ROOT}` 目录下：
*   **功能清单规则**：`${RULES_ROOT}/01-prd-rules/feature-list-generation-rules_v1.md`
*   **PRD 生成规则**：`${RULES_ROOT}/01-prd-rules/prd-generation_v8.md` *(含 §9.1 与《需求测试准入 DoD》对齐；定稿前自检)*
*   **PRD 审查规则**：`${RULES_ROOT}/01-prd-rules/prd-completeness-check.md` *(须执行 §2.19，与 xuqiuceshidod 对账并给出测试准入结论：通过/有条件通过/不准入)*
*   **测试准入标准**：`${RULES_ROOT}/01-prd-rules/xuqiuceshidod.md` *(作为 PRD 审查的可测性对账真源)*
*   **后端接口文档生成**：`${RULES_ROOT}/02-api-rules/api-doc-generation-rules_v1.md`
*   **后端接口文档审查**：`${RULES_ROOT}/02-api-rules/api-doc-reconstruction-review-rules_v1.md`
*   **设计文档生成规则**：`${RULES_ROOT}/03-design-rules/design-doc-reconstruction-rules_v2.md`
*   **设计文档检查规则**：`${RULES_ROOT}/03-design-rules/design-doc-reconstruction-review-rules_v2.md`

### 1.3 输出结构定义
所有反构输出文件按微服务模块隔离存放于 `${OUTPUT_ROOT}/knowledge/` 结构中：
*   **功能清单**：`${OUTPUT_ROOT}/knowledge/功能清单.md`  
    *(注：若已存在 `${OUTPUT_ROOT}/功能清单-v*.md` 且为唯一一份版本化文件，可与之对账后选用其一作为真源，并在首段「编制说明」写清以谁为准)*
*   **PRD 目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/prd-docs/`
*   **PRD 审查目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/prd-review/`
*   **接口文档目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/api-docs/`
*   **接口审查目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/api-review/`
*   **设计文档目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/design-docs/`
*   **设计审查目录**：`${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/design-review/`

---

## 2. 阶段式实施细则

### 【阶段 0 | 功能清单生成】
*   **目标**：从代码（前后端功能完整性）出发，梳理出微服务的系统框架。
*   **执行规则**：严格按 `${RULES_ROOT}/01-prd-rules/feature-list-generation-rules_v1.md` 生成或更新。
*   **输出路径**：`${OUTPUT_ROOT}/knowledge/功能清单.md`
*   **要求**：必须包含系统功能结构图谱与后续骨架，与代码、菜单、路由可对齐，并标注来源或推断依据。

### 【阶段 1 | PRD 需求文档生成】
*   **数据真源**：以阶段 0 生成的 `${OUTPUT_ROOT}/knowledge/功能清单.md` 中每个 L2【业务域】、L3【模块】及模块内可验收能力（L4/L5）为真源。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/prd-docs/{两位序号}_{模块短名}_{子模块短名}_业务需求文档.md`  
    *(注：两位序号自 `01` 起，按《功能清单》中模块出现的顺序连续编号；短名与清单标题一致，文件名需进行安全化处理，如去除非法字符、空格替换为下划线)*
*   **执行规则**：严格按 `${RULES_ROOT}/01-prd-rules/prd-generation_v8.md` 规则生成。定稿前必须执行可测性自检（红线零触发，缺项进「不明确条目」）。

### 【阶段 2 | PRD 审查与迭代】
*   **目标**：对生成的 PRD 进行质量合规性校验。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/prd-review/{两位序号}_{模块短名}_{子模块短名}_业务需求文档检查报告.md`
*   **执行规则**：针对阶段 1 的每份 PRD，执行 `${RULES_ROOT}/01-prd-rules/prd-completeness-check.md` 进行检查，并与 `${RULES_ROOT}/01-prd-rules/xuqiuceshidod.md` 进行测试准入对账。
*   **控制闸门**：若总体结论为“不通过”，**必须**修订对应 PRD 文档并重新审查，直至获得“通过”或“有条件通过”。禁止未通过即进入下一阶段。

### 【阶段 3 | 接口文档生成】
*   **前提条件**：对应子模块的“PRD + 审查报告”均已通过。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/api-docs/{两位序号}_{模块短名}_{子模块阻名}_接口文档.md`
*   **执行规则**：分析后端接口，严格按照 `${RULES_ROOT}/02-api-rules/api-doc-generation-rules_v1.md` 提取并输出接口字段、输入输出格式及调用实例。

### 【阶段 4 | 接口审查与迭代】
*   **目标**：验证接口文档的完整性与一致性。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/api-review/{两位序号}_{模块短名}_{子模块短名}_接口检查文档.md`
*   **执行规则**：执行 `${RULES_ROOT}/02-api-rules/api-doc-reconstruction-review-rules_v1.md` 检查生成报告。
*   **控制闸门**：若审查结果为“不通过”，必须重新修订接口文档并重复该审查，直至审查通过。

### 【阶段 5 | 设计文档生成】
*   **目标**：拆解后端接口的方法实现与底层技术细节。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/design-docs/{两位序号}_{模块短名}_设计文档.md`
*   **执行规则**：从各微服务代码出发，严格按照 `${RULES_ROOT}/03-design-rules/design-doc-reconstruction-rules_v2.md` 生成。

### 【阶段 6 | 设计文档审查与迭代】
*   **目标**：验证设计文档的深度与合规性。
*   **输出路径与命名**：  
    `${OUTPUT_ROOT}/knowledge/micro/{微服务名称}/design-review/{两位序号}_{模块短名}_设计检查文档.md`
*   **执行规则**：严格按照 `${RULES_ROOT}/03-design-rules/design-doc-reconstruction-review-rules_v2.md` 对设计文档执行检查并输出报告。
*   **控制闸门**：未通过审查的设计文档必须重新进行修订与验证，确保最终质量合格。

---

## 3. 智能体团队（Agent Team）协作约束

1.  **限制并行处理**：子模块较多时可分批执行，但在同一会话内必须保持顺序与编号一致。每完成一个子模块的所有阶段，再进入下一个子模块，避免并行处理导致编号及文档依赖错乱。
2.  **闭环与质量门禁**：各个阶段都有明确的质量门闸，任何未通过的步骤均属于阻塞性问题，必须完成相应修订再向前推进。
