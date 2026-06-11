---
name: /design-doc-reconstruction
id: design-doc-reconstruction
category: Documentation
description: 后端微服务知识返构中的设计文档生成规则 v2；直接从代码返构生成类似 设计文档V6.md 结构的完整设计文档。无用户输入，全自动从代码提取代码增量清单、数据模型、接口设计、业务规则、核心链路、前端规格、测试策略、枚举配置、需求映射等章节。
---

## 目标

- **全自动化**：从代码仓库扫描、分析、提取、结构化输出。
- **多服务覆盖**：自动识别涉及的多个微服务，按服务分组输出。
- **严格事实模式**：所有结论必须有代码证据支撑，禁止推测。

### 输入来源（全自动识别）

| 优先级 | 来源 | 用途 |
|--------|------|------|
| P0 | Git 变更记录（git diff / git log） | 代码增量清单 |
| P1 | Controller / Service / Domain / Repository / Mapper / Entity 代码 | 业务链路、数据模型、接口设计、规则提取 |
| P2 | 数据库 Schema / DDL / Flyway / Liquibase | 表结构、字段约束 |
| P3 | 前端代码（Vue/React 组件、TypeScript） | 前端设计规格 |
| P4 | 测试代码（单元测试、集成测试） | 测试策略 |
| P5 | 国际化配置文件（messages_zh_CN.properties / i18n ts/js） | 枚举、常量与配置 |

---

## 文档结构（固定顺序，对齐 V6）

生成的设计文档必须严格按以下章节顺序组织：

```markdown
# {模块/功能名称} — 开发设计文档

> 适用范围：功能点描述
> 基线分支：{branch}

---

## 0. 需求映射

| 需求编号 | PRD章节 | 需求描述 | 对应设计章节 |
|---------|---------|---------|------------|
| REQ-001 | 3.1 | 描述 | 第2章、第4章、第5.1-5.3节 |

---

## 1. 代码增量清单

### 1.1 {service-name} 服务（新增 N 文件/修改 M 文件）

| 文件路径 | 变更类型 | 核心功能 |
|---------|---------|---------|
| `path/to/File.java` | 新增/修改/删除 | 一句话描述 |

---

## 2. 数据模型

> **所属服务**：{service-name}

### 2.1 Domain 层 DTO/实体

| DTO/实体名称 | 用途 | 核心字段 | 约束 |
|-------------|------|---------|------|
| XxxDTO | 描述 | field1, field2 | field1∈[1,10] |

### 2.2 跨服务 DTO（如有）

```java
class CrossServiceDTO {
    // 字段定义
}
```

### 2.3 存量表复用

| 表名 | 复用字段 | 存储内容 |
|------|---------|---------|
| xxx_table | field_type, ext_attr | 描述 |

### 2.4 编码规范

**编码规则**：`{PREFIX}_{parentCode}_{id}`

**编码解析工具**：
```java
XxxUtil.parseFieldId(fieldId) // 返回 Optional<String[parentCode, id]>
```

---

## 3. 接口设计

> **所属服务**：{service-name}

### 3.1 {模块名} 接口

| 接口 | 方法 | 路径 | 变更类型 |
|------|------|------|---------|
| 接口名称 | POST | /api/xxx?operation=create | 新增Table字段校验 |

**关键设计**：
- 字段编码规则：...
- 拦截逻辑：...

### 3.2 跨服务 Feign/HTTP/RPC 接口

| 调用方向 | 方法 | 响应 | 用途 |
|---------|------|------|------|
| serviceA → serviceB | `methodName()` | `ReturnType` | 描述 |

---

## 4. 业务规则与校验

> **所属服务**：{service-name}

### 4.1 {规则分类} 规则

| 规则编号 | 规则描述 | 错误码 | 实现位置 |
|---------|---------|--------|---------|
| TBL-001 | 描述规则内容 | ERROR_CODE | XxxUtil.validate() |
| MUT-001 | 描述互斥规则 | ERROR_CODE | XxxAbility.validate() |

### 4.2 安全解析要求（如适用）

**适用范围**：...

**安全解析原则**：
1. **空值检查**：...
2. **异常捕获**：...
3. **降级策略**：...
4. **日志记录**：...
5. **字段缺失容错**：...

---

## 5. 核心业务链路

> **所属服务**：{service-name}

### 5.1 {链路名称}

**参与方**：

| 角色 | 类名 | 职责 |
|------|------|------|
| 入口 | XxxController | 接收请求，参数校验 |
| 编排 | XxxService | 业务编排，事务控制 |
| 领域 | XxxAbility | 业务规则校验 |
| 持久化 | XxxGatewayImpl | 数据解析与持久化 |

**数据流向**：
```
XxxDTO
→ XxxController.method()
→ XxxService.method()
→ XxxAbility.method()
→ XxxGatewayImpl.method()
→ DB.operation(table)
```

**关键决策**：
1. 决策点 1：...
2. 决策点 2：...

**处理逻辑**（详细步骤）：
1. 步骤 1：...
2. 步骤 2：...
3. 步骤 3：...

**示例**（如有）：
```
输入：...
输出：...
```

---

## 6. 前端设计规格（如适用）

### 6.1 组件架构

```
ParentComponent.vue
├─ ChildComponent.vue
│ ├─ ...
```

### 6.2 关键组件接口

**ComponentName.vue**：

| 接口项 | 说明 |
|--------|------|
| **Props** | `prop: Type`（描述） |
| **Events** | `event`（描述） |
| **职责** | 描述 |
| **约束** | 描述 |

### 6.3 工具库

| 导出项 | 类型 | 说明 |
|--------|------|------|
| `constName` | 常量 | 描述 |
| `functionName()` | 函数 | 描述 |

### 6.4 数据格式约定

```typescript
interface XxxConfig {
  field: string;
}
```

---

## 7. 枚举、常量与配置

### 7.1 枚举定义

**XxxEnum（扩展）**：

| 新增枚举值 | code | i18nKey | 说明 |
|-----------|------|---------|------|
| ENUM_VALUE | "code" | "XxxEnum.Value" | 描述 |

**扩展方法**：
- `methodName()`：描述

### 7.2 常量定义

**XxxConstant**：

| 常量名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| CONSTANT_NAME | String | "VALUE" | 描述 |

### 7.3 国际化词条

**{service-name} 服务**：

| Key | zh_CN | en_US | 说明 |
|-----|-------|-------|------|
| BusiError.ERROR_CODE | 中文错误信息 | English error message | 描述 |

---

## 8. 测试策略

### 8.1 单元测试

| 测试类 | 测试场景 | 验收标准 | 需求来源 |
|--------|---------|---------|---------|
| XxxTest | 场景描述 | 标准描述 | REQ-001 |

### 8.2 集成测试（如有）

| 测试类 | 测试场景 | 验收标准 | 需求来源 |
|--------|---------|---------|---------|
| ... | ... | ... | ... |

### 8.3 性能测试（如有）

| 场景 | 指标 | 目标 |
|------|------|------|
| ... | 响应时间 | < 200ms |

### 8.4 兼容性测试（如有）

| 场景 | 验证点 | 需求来源 |
|------|--------|---------|
| ... | ... | ... |

---

## 9. 需求-设计映射表

| PRD章节 | 需求描述 | 设计章节 | 实现状态 |
|---------|---------|---------|---------|
| 3.1 | 需求描述 | 第2章、第4章 | ✅ |
| 3.2 | 需求描述 | 第5.1节 | ✅ |

---

> 文档版本：V6
> 生成时间：{YYYY-MM-DD}
> 基线分支：{branch}
```

---

## 各章节生成规则

### 第0章：需求映射

**自动生成逻辑**：
1. 扫描代码中的注释、commit message、分支名称，提取需求线索
2. 若发现 PRD 文档（通过文件路径匹配 `*PRD*`、`*需求*`、`*BRD*`），自动提取 REQ-XXX 编号
3. 若无 PRD，使用代码变更范围反推需求描述
4. 每个需求映射到对应设计章节

**输出格式**：

| 需求编号 | PRD章节 | 需求描述 | 对应设计章节 |
|---------|---------|---------|------------|
| REQ-001 | 3.1 | 模板增加表格类型采集项 | 第2章（数据模型）、第4章（接口）、第5.1-5.3节（链路）、第5.8节（报告）、第8章（前端） |

**规则**：
- 需求编号格式：REQ-XXX（三位数字）
- 需求描述：一句话概括，从代码功能反推
- 对应设计章节：列出所有涉及章节编号
- 若无明确需求来源，标记 `TECH_DEBT` 或 `REFACTOR`

---

### 第1章：代码增量清单

**自动生成逻辑**：
1. 执行 `git diff --name-status {base_branch}..{current_branch}` 获取变更文件列表
2. 按服务（目录前缀）分组
3. 识别变更类型：A（新增）、M（修改）、D（删除）、R（重命名）
4. 解析文件内容，生成"核心功能"一句话描述

**输出格式**：

```md
## 1. 代码增量清单

### 1.1 {service-name} 服务（新增 N 文件/修改 M 文件）

| 文件路径 | 变更类型 | 核心功能 |
|---------|---------|---------|
| `domain/model/dto/fieldType/TableFieldExtAttrDTO.java` | 新增 | 表格字段扩展属性DTO |
| `domain/common/enums/TemplateFieldTypeEnum.java` | 修改 | 新增TABLE枚举及校验逻辑 |
```

**核心功能描述规则**：
- DTO/Entity："{业务语义}DTO/实体"
- Service："{业务操作}服务实现"
- Controller："{接口路径}入口控制"
- Mapper/Repository："{表名}数据访问"
- Util："{功能}工具方法"
- Vue/TS："{组件名}前端组件/工具"

---

### 第2章：数据模型

**自动生成逻辑**：
1. 扫描新增/修改的 DTO/Entity/VO 类文件
2. 提取类名、字段、类型、注解（@NotNull、@Size、@Pattern 等）
3. 识别跨服务 DTO（通过包路径或 import 语句）
4. 扫描 ORM 实体/Mapper，识别表名、字段、索引
5. 提取编码规范（通过字段命名模式、工具方法）

**输出格式**：

```md
## 2. 数据模型

> **所属服务**：{service-name}（主服务）、{service-name}（跨服务契约）

### 2.1 Domain 层 DTO/实体（{service-name}）

| DTO/实体名称 | 用途 | 核心字段 | 约束 |
|-------------|------|---------|------|
| TableFieldExtAttrDTO | 表格字段扩展属性 | columns: List<TableColumnDTO>, maxRows: Integer | columns∈[1,10], maxRows∈[1,20]默认12 |
```

**字段约束提取规则**：
- 从注解提取：@NotNull → 非空、@Size(min=1, max=10) → ∈[1,10]
- 从代码逻辑提取：if (columns.size() > 10) throw → ∈[1,10]
- 从注释提取：// 默认12，范围[1,20] → 默认12，∈[1,20]

---

### 第3章：接口设计

**自动生成逻辑**：
1. 扫描 Controller 类，提取 @RequestMapping / @GetMapping / @PostMapping 等注解
2. 提取方法签名、路径、HTTP 方法
3. 识别变更类型：
   - 新增：git 状态为 A 且为 Controller 方法
   - 修改：git 状态为 M 且方法体有变更
   - 删除：git 状态为 D
4. 扫描 FeignClient / @RPC 接口，识别跨服务调用
5. 提取关键设计点（从方法注释、参数校验、拦截器配置）

**输出格式**：

```md
## 3. 接口设计

> **所属服务**：{service-name}（主服务）、{service-name}（跨服务Feign调用）

### 3.1 {模块名} 接口（{service-name}）

| 接口 | 方法 | 路径 | 变更类型 |
|------|------|------|---------|
| 创建模板结构 | POST | /api/Template?operation=createTemplateStructure | 新增Table字段校验 |
| 查询模板字段列表 | GET | /api/templatefield/listByTemplateId/{templateId} | TABLE类型字段展开列维度子字段 |
```

**变更类型描述规则**：
- 新增："新增{功能点}"
- 修改："{功能点}变更"（如"TABLE类型字段展开列维度子字段"）
- 删除："删除{功能点}"

---

### 第4章：业务规则与校验

**自动生成逻辑**：
1. 扫描代码中的校验逻辑（if 判断、@Valid、Validator 实现）
2. 扫描异常抛出点（throw new BizException("ERROR_CODE")）
3. 提取错误码和错误信息（从 BusiMsgConstants、枚举、i18n 文件）
4. 按规则前缀分类编号：
   - TBL-：表格/数据结构相关校验
   - MUT-：互斥/排他规则
   - SUB-：提交/保存校验
   - AUTH-：认证鉴权
   - PERM-：权限/数据权限
   - IDEM-：幂等/防重
   - FLOW-：流程/状态机
   - VAL-：通用校验
   - INT-：集成/外部
   - SEC-：安全

**输出格式**：

```md
## 4. 业务规则与校验

> **所属服务**：{service-name}（主服务）、{service-name}（跨服务校验）

### 4.1 表格字段配置规则

| 规则编号 | 规则描述 | 错误码 | 实现位置 |
|---------|---------|--------|---------|
| TBL-001 | columns非空且数量∈[1,10] | TABLE_COLUMN_CONFIG_ERROR | TemplateStructureJsonUtil.validateTableFieldConfig() |
| TBL-002 | 列id不可重复 | TABLE_COLUMN_CONFIG_ERROR | TemplateStructureJsonUtil.validateTableFieldConfig() |
```

**规则编号分配规则**：
- 同一前缀按发现顺序编号：TBL-001、TBL-002...
- 不同前缀独立编号：TBL-001、MUT-001、SUB-001...
- 错误码从代码中提取（BizMsgConstants、BusiError 枚举、i18n 文件）

---

### 第5章：核心业务链路

**自动生成逻辑**：
1. 从 Controller 方法入口开始，递归追踪调用链：
   - Controller → Service → Domain/Ability → Repository → DB
   - 识别分支（if/switch）、循环（for/while）、异常（try-catch）
   - 识别异步调用（@Async、MQ、线程池）
   - 识别事务边界（@Transactional、TransactionTemplate）
2. 为每个链路生成：
   - 参与方表格（角色、类名、职责）
   - 数据流向（ASCII 或 Mermaid 流程图）
   - 关键决策点（设计决策及理由）
   - 处理逻辑（详细步骤）
   - 示例（输入/输出）

**输出格式**：

```md
## 5. 核心业务链路

> **所属服务**：{service-name}（主服务）、{service-name}（跨服务标记码）、{service-name}（质量步骤转移）

### 5.1 {链路名称}（{service-name}）

**参与方**：

| 角色 | 类名 | 职责 |
|------|------|------|
| 入口 | TemplateController | 接收请求，参数校验 |
| 编排 | TemplateService | 业务编排，事务控制 |
| 领域 | TemplateAbility | 互斥校验（业务规则） |
| 持久化 | TemplateGatewayImpl | 数据解析与持久化 |
| 工具 | TemplateStructureJsonUtil | JSON结构校验 |

**数据流向**：
```
TemplateCreateStructureDTO
→ TemplateController.createTemplateStructure()
→ TemplateService.createTemplateStructure()
→ TemplateAbility.createTemplateStructure()
→ TemplateGatewayImpl.updateTemplateStructureAndTemplate()
→ TemplateStructureJsonUtil.validateTableFieldConfig() // 配置校验
→ TemplateAbility.validateDuplicateAndTableMutex() // 互斥校验
→ DB.batchInsertOrUpdate(template_structure, template_field)
```

**关键决策**：
1. 配置校验 vs 互斥校验顺序：先配置校验（格式正确性），再互斥校验（业务规则）
2. 幂等控制：Redis分布式锁（key=`template:lock:{templateCode}`，过期时间2分钟）
```

**链路追踪深度要求**：
- 至少追踪到 Repository/Mapper 层
- 涉及外部调用必须标注服务名和接口名
- 涉及 MQ 必须标注 topic/queue 名
- 涉及缓存必须标注缓存 key 和失效策略

---

### 第6章：前端设计规格

**自动生成逻辑**（如代码中包含前端文件）：
1. 扫描 Vue/React 组件文件，识别组件层级
2. 提取 Props、Events、职责、约束
3. 扫描工具库（constants.ts、utils.ts）
4. 提取 TypeScript 接口定义

**输出格式**：

```md
## 6. 前端设计规格

### 6.1 组件架构

```
TemplateCreate.vue
├─ fieldsInfo.vue
│ ├─ TableFieldEditor.vue（表格字段专用编辑器，独立组件）
│ │ ├─ draggable（列拖拽排序）
│ │ ├─ el-input（列名称输入，maxlength=100）
│ │ ├─ el-checkbox（必填勾选）
│ │ └─ AiRecognitionButton + AiRecognitionDialog（列AI配置）
│ └─ 其他字段编辑器...
├─ pcReview.vue（PC预览）
│ └─ fields-pc.vue（字段预览渲染）
│   └─ el-table（表格字段预览）
└─ leftBar.vue（左侧字段库）
   └─ Table字段拖拽入口
```

### 6.2 关键组件接口

**TableFieldEditor.vue**：

| 接口项 | 说明 |
|--------|------|
| **Props** | `field: any`（输入：表格字段配置对象） |
| **Props** | `aiToolsData: AiToolRes[]`（AI工具列表） |
| **Events** | `change`（通过v-model隐式传递） |
| **职责** | 列增删、拖拽排序、名称编辑、必填配置、AI识别配置 |
| **约束** | 最少1列，最多10列；名称不可重复；maxRows∈[1,20] |
| **依赖** | `vuedraggable`、`tableField.ts` |
```

---

### 第7章：枚举、常量与配置

**自动生成逻辑**：
1. 扫描枚举类（Enum），提取全部值和含义
2. 扫描常量类（Constant），提取业务常量
3. 扫描国际化配置文件，提取新增/修改的词条
4. 识别 AI 工具库配置（如有）

**输出格式**：

```md
## 7. 枚举、常量与配置

### 7.1 枚举定义

**TemplateFieldTypeEnum（扩展）**：

| 新增枚举值 | code | i18nKey | 说明 |
|-----------|------|---------|------|
| TABLE | "Table" | "TemplateFieldType.Table" | 表格字段类型 |

**扩展方法**：
- `checkValueRule(TemplateField templateField, String jsonValue)`：新增Table类型校验逻辑
- `getValue(String fieldType, String jsonValue, String enumValue, String extAttr)`：**必须保留4个参数**

### 7.2 常量定义

**TemplateConstant**：

| 常量名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| TABLE_FIELD_COLUMN_CODE_PREFIX | String | "TABLE_" | 表格列字段编码前缀 |
| TABLE_MAX_ROWS_UPPER_LIMIT | int | 20 | 表格最大行数上限 |

### 7.3 国际化词条

**workorder 服务**：

| Key | zh_CN | en_US | 说明 |
|-----|-------|-------|------|
| TemplateFieldType.Table | 表格 | Table | 表格字段类型 |
| BusiError.TABLE_ROWS_EXCEED_LIMIT | 表格行数超过限制 | Table rows exceed limit | 行数超限错误 |
```

---

### 第8章：测试策略

**自动生成逻辑**：
1. 扫描测试类（*Test.java、*.spec.ts），识别测试场景
2. 从测试方法名和断言提取验收标准
3. 从 @PerformanceTest、@LoadTest 等注解提取性能指标
4. 从兼容性测试代码提取验证点

**输出格式**：

```md
## 8. 测试策略

### 8.1 单元测试

| 测试类 | 测试场景 | 验收标准 | 需求来源 |
|--------|---------|---------|---------|
| TemplateFieldTypeEnumTest | TABLE枚举的checkValueRule | 行数超限抛异常、必填列为空抛异常 | REQ-001 |
| TemplateUtilTest | parseTableColumnFieldId | 正确解析TABLE_parent_columnId格式 | REQ-003 |

### 8.2 前端测试

| 测试类 | 测试场景 | 验收标准 | 需求来源 |
|--------|---------|---------|---------|
| TableFieldEditor.spec.ts | 添加列 | 列数+1，新列name为空 | REQ-001 |
| OrderFields.spec.ts | 编辑模式表格填报 | 可增删行，输入单元格值 | REQ-001 |

### 8.3 性能测试

| 场景 | 指标 | 目标 |
|------|------|------|
| 查询含Table字段的工单详情 | 响应时间 | < 200ms（单表100行） |
| 标记码树查询（含Table展开） | 响应时间 | < 100ms（20个Table字段） |

### 8.4 兼容性测试

| 场景 | 验证点 | 需求来源 |
|------|--------|---------|
| 存量模板（无Table字段） | 查询、编辑、导出、导入不受影响 | REQ-003 |
| 存量工单（无Table字段） | 查询、编辑、提交不受影响 | REQ-001 |
```

---

### 第9章：需求-设计映射表

**自动生成逻辑**：
1. 汇总第0章的需求编号
2. 遍历所有设计章节，识别每个需求涉及的设计内容
3. 标记实现状态（从代码完成度判断）

**输出格式**：

```md
## 9. 需求-设计映射表

| PRD章节 | 需求描述 | 设计章节 | 实现状态 |
|---------|---------|---------|---------|
| 3.1 | 表格控件基本配置 | 第2章、第4章（TBL规则）、第5.1节、第6章 | ✅ |
| 3.1 | 列字段AI识别工具绑定 | 第6.3节、第7.4节 | ✅ |
| 3.1 | 分类可重复与表格控件互斥 | 第4.2节（MUT-001/002）、第5.1节 | ✅ |
| 3.2 | AI技术类型扩展 | 第7.4节 | ✅ |
| 3.3 | 预置标记码查询（二维） | 第5.4.1节 | ✅ |
| 3.3 | 结构化文档生成 | 第5.5节、第5.6节 | ✅ |
| 约束 | 不可跨表格选择 | 第4.2节（MUT-003）、第5.4.2节 | ✅ |
| 约束 | 不可同时选可重复和表格列 | 第4.2节（MUT-004）、第5.4.2节 | ✅ |
```

**实现状态判定规则**：
- ✅：代码已实现，有完整测试覆盖
- 🔄：代码部分实现，或有 TODO/FIXME 标记
- ⏳：代码未实现，仅预留接口
- ❌：不适用（如前端需求但纯后端服务）

---

## 严格事实模式（Strict Fact Mode，强制开启）

### 基本原则（强制）

- 只允许依据可验证代码证据输出业务结论。
- 未观察到证据的内容，必须输出 `UNKNOWN_RUNTIME`，不得补全。
- 主文档默认只收录 `EXTRACTED` 结论。
- `INFERRED` 与 `AMBIGUOUS` 仅允许写入「候选/待确认」区块，不得混入主结论。

### 输出约束（强制）

每条关键结论必须满足：
- 至少 1 个证据锚点：`file_path + symbol + evidence_type`
- 至少 1 条证据摘要：说明该证据支持了什么结论
- 置信度明确：`EXTRACTED | INFERRED | AMBIGUOUS`

若不满足则：
- 该结论标记为 `INVALID_NO_EVIDENCE`
- 不得进入主文档正文
- 必须进入 `quality-report.json` 的阻断项

### 防发散禁令（强制）

- 禁止使用「通常/一般/大概率/推测」等措辞代替证据。
- 禁止推断外部服务内部逻辑；只能描述「本服务可见调用行为」。
- 禁止将命名相似直接视为业务等价（需代码链路证据）。
- 禁止根据历史经验补全状态机、补偿逻辑、权限规则。
- 禁止在无 SQL/ORM 证据时写数据库表关系。

### 冲突与未知处理（强制）

- 证据冲突时不得自行合并，必须标记 `CONFLICT` 并并列展示。
- 运行时相关但静态不可见（配置中心、灰度开关、动态脚本）统一标记 `UNKNOWN_RUNTIME`。
- 对 `UNKNOWN_RUNTIME` 必须给出「缺失证据类型」和「建议补证路径」。

### 失败中断规则（强制）

任一方法出现以下情况，方法状态设为 `BLOCKED`：
- 找不到 Controller 到 Service 的可达链路证据
- 涉库逻辑存在但无法定位表或操作类型
- 状态机流转存在但无法定位守卫条件

`BLOCKED` 方法不得标记「返构完成」。

---

## 冲突与未知项模板

### 主文档中的未知项模板

```md
### UNKNOWN_RUNTIME
- 方法：<Controller#method>
- 未知点：<例如 动态开关控制的分支逻辑>
- 缺失证据：<配置中心键/运行时注入/环境变量来源>
- 建议补证：<配置仓库路径/运行日志字段/发布参数>
```

### 主文档中的冲突项模板

```md
### CONFLICT
- 方法：<Controller#method>
- 冲突主题：<例如 状态流转条件不一致>
- 证据 A：<file_path + symbol + 摘要>
- 证据 B：<file_path + symbol + 摘要>
- 处理策略：并列保留，待人工确认
```

### `quality-report.json` 最小字段

```json
{
  "strict_mode": true,
  "blocked_methods": [],
  "invalid_conclusions": [],
  "unknown_runtime_items": [],
  "conflict_items": [],
  "evidence_coverage": {
    "method_level": 0.0,
    "field_level": 0.0,
    "flow_chart_level": 0.0,
    "sequence_diagram_level": 0.0,
    "table_lineage_level": 0.0
  }
}
```

---

## 质量门禁

### 覆盖门禁

- Controller 方法覆盖率 = 100%
- 模块归类覆盖率 >= 98%
- 代码增量清单完整率 = 100%
- 数据模型覆盖率 >= 95%
- 需求-设计映射覆盖率 = 100%
- 业务规则分类完整率 >= 98%

### 链路门禁

- 每个方法至少 1 条完整主链到数据层或外部依赖
- 有分支必须有分支链路（表格或流程图）
- 有异常必须有异常链路（表格或时序图标注）
- 有事务必须标明事务边界和传播行为
- 涉状态机必须有状态图或流转矩阵

### 数据门禁

- 涉库方法必须标 database / schema / table / operation / 关键字段
- 使用枚举的方法必须标枚举值语义
- 使用缓存/MQ/RPC 的方法必须标调用目的与失败策略
- 高风险 SQL（批量更新、无 where 更新）必须标注并说明

### 图表门禁

- 每个方法必须包含**至少一个** Mermaid 图（流程图或时序图）
- 涉及状态流转的方法必须包含状态图
- 图表必须与代码逻辑一致，不得简化关键分支

### 严格事实门禁

- 主文档 `EXTRACTED` 结论占比 = 100%（正文部分）
- 每个方法至少一个证据锚点，否则该方法 `BLOCKED`
- `INVALID_NO_EVIDENCE` 数量必须为 0
- `CONFLICT` 与 `UNKNOWN_RUNTIME` 必须全部入附录与质量报告
- 横切能力清单中「存在项」覆盖率 = 100%
- 未覆盖项必须在 `quality-report.json` 标红并说明原因

### 新增门禁（v2）

- **业务规则编号化**：所有规则必须有唯一编号（如 TBL-001）
- **错误码完整性**：所有校验规则必须关联错误码
- **数据模型一致性**：DTO/实体/表结构必须一致，冲突必须标记
- **国际化完整性**：用户可见错误信息必须有国际化词条
- **测试策略可追踪**：每个需求至少映射一个测试场景

---

## 增量更新规则

- 变更感知粒度：模块级 + 方法级
- 当以下对象变更时触发重算：
  - Controller / Service / Repository 逻辑
  - SQL/ORM 映射
  - 枚举/常量
  - 状态机流转条件
  - 事务与异常处理
  - 代码增量（新增/修改/删除文件）
  - 数据模型（DTO/实体/表结构变更）
- 仅重生成受影响章节，不重写全文件

版本策略：
- 章节结构变化 -> `major`
- 服务新增/删除 -> `minor`
- 字段/规则/流程修订 -> `patch`

---

## CI 守护建议

建议增加自动检查：
- 新增 Controller 方法未入文档 -> fail
- 涉库方法缺失表影响 -> fail
- 新增枚举值未有语义 -> fail
- 模块归类失败（落 `misc`）超过阈值 -> fail
- 出现 `INVALID_NO_EVIDENCE` -> fail
- 出现 `BLOCKED` 且未在报告中说明 -> fail
- 主文档正文出现 `INFERRED/AMBIGUOUS` -> fail
- 方法缺失 Mermaid 图 -> fail
- 状态机方法缺失状态图 -> fail
- 业务规则无编号 -> fail
- 错误码无国际化词条 -> fail
- 需求未映射到设计章节 -> fail
- 代码增量清单缺失 -> fail

---

## 完成定义（Definition of Done）

每个微服务满足以下条件方可视为设计文档返构完成：
- 生成独立服务目录
- 仅包含一份设计文档，但已按模块细化
- Controller 方法覆盖率 100%
- 代码增量清单完整
- 数据模型覆盖 >= 95%
- 业务规则全部编号化并关联错误码
- 需求-设计映射覆盖率 100%
- 每个方法包含：
  - 主链路流程图（Mermaid）
  - 时序图（Mermaid）
  - 分支链路（表格）
  - 异常链路（表格）
  - 业务规则分类（表格，含编号）
  - 枚举与状态机（表格/状态图）
  - 数据库与表影响（表格/SQL）
  - 下游依赖与稳定性（表格）
  - 方法链路追踪（文本调用链）
- 关键结论可追溯到代码证据
- 严格事实模式检查通过（无证据结论为 0）
- 所有 Mermaid 图与代码逻辑一致

---

## 附录 A：规则编号前缀速查表

| 前缀 | 含义 | 使用场景 |
|------|------|---------|
| TBL- | 表格/数据结构规则 | 字段校验、结构约束 |
| MUT- | 互斥/排他规则 | 字段互斥、分类互斥 |
| SUB- | 提交/保存校验规则 | 保存前校验、提交校验 |
| AUTH- | 认证鉴权规则 | 登录、token、权限 |
| PERM- | 权限/数据权限规则 | 数据范围、操作权限 |
| IDEM- | 幂等/防重规则 | 重复提交、幂等控制 |
| FLOW- | 流程/状态机规则 | 状态流转、流程控制 |
| VAL- | 通用校验规则 | 格式校验、范围校验 |
| INT- | 集成/外部规则 | 外部调用、接口约束 |
| SEC- | 安全规则 | 加密、脱敏、防攻击 |

---

## 附录 B：与 V6 结构对照表

| V6 章节 | 本规则章节 | 说明 |
|---------|-----------|------|
| 0. 需求映射 | 第0章 | 全局需求映射 |
| 1. 代码增量清单 | 第1章 | 按服务分组 |
| 2. 数据模型 | 第2章 | 按服务分组 |
| 3. 接口设计 | 第3章 | 按服务分组 |
| 4. 业务规则与校验 | 第4章 | 全局规则编号化 |
| 5. 核心业务链路 | 第5章 | 按链路分组 |
| 6. 前端设计规格 | 第6章 | 如适用 |
| 7. 枚举、常量与配置 | 第7章 | 全局 |
| 8. 测试策略 | 第8章 | 全局 |
| 9. 需求-设计映射表 | 第9章 | 全局汇总 |

---
