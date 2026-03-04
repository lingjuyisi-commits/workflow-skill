# 端侧 AI 编码技术选型分析

> 日期：2026-03-03
> 场景：端侧 AI（on-device AI）移动端编码，不考虑性能，重点评估编码效率、可测试性、可迭代性、稳定性、质量

---

## 结论

**推荐：Kotlin**
次选 Java（历史包袱场景），Flutter 有条件采用，React Native 不推荐。

---

## 五维评分对比（等权，不含性能）

| 维度 | Kotlin | Java | Flutter (Dart) | React Native (TS) |
|------|:------:|:----:|:--------------:|:-----------------:|
| 编码效率 | ★★★★★ | ★★★ | ★★★★ | ★★★ |
| 可测试性 | ★★★★★ | ★★★★ | ★★★ | ★★★ |
| 可迭代性 | ★★★★★ | ★★★ | ★★★★ | ★★★★ |
| 稳定性 | ★★★★★ | ★★★★★ | ★★★ | ★★ |
| 质量 | ★★★★★ | ★★★★ | ★★★★ | ★★★ |
| **综合** | **96** | **78** | **70** | **59** |

---

## 各维度关键差异

### 编码效率

- **Kotlin**：`sealed class` 精确建模推理状态，协程 + Flow 天然表达异步推理，扩展函数消除 Tensor 操作样板代码
- **Flutter**：MethodChannel 跨层调用带来额外编码量，原生 AI SDK 无一等公民支持
- **RN**：JS 单线程模型与推理场景天然冲突，推理任务必须下沉原生层

### 可测试性

- **Kotlin**：`kotlinx-coroutines-test` + `MockK` + `turbine` 三件套，精确控制推理异步时序，Flow 流验证极为方便
- **Flutter**：MethodChannel Mock 链路长，CI 搭建复杂
- **RN**：原生推理模块只能整体 Mock，测试粒度粗

### 可迭代性

- **Kotlin**：`sealed interface` + `when` 穷举让模型版本切换和 Prompt 策略变更在编译期兜底，重构安全
- **Java**：无 `sealed class`，状态变更编译器无法穷举，重构成本高
- **Flutter/RN**：跨语言层接口变更（Channel 协议）需同步修改两侧，迭代摩擦大

### 稳定性

- **Kotlin**：空安全消除 NPE，结构化并发绑定组件生命周期防内存泄漏，与原生推理库直接交互无额外崩溃点
- **RN**：JS/Native GC 不同步，大 Tensor 在边界传递有内存拷贝风险，线上问题难以全量感知，端侧 AI 生产验证案例极少

### 质量

- **Kotlin**：`@JvmInline value class` 可为 Tensor 维度建立零成本类型安全抽象，Detekt + ktlint 配合 CI
- **RN**：原生模块类型定义依赖社区手写 `.d.ts`，与实现可能不同步，无法为 Tensor 操作提供编译期保护

---

## 各方案适用定位

| 方案 | 定位 | 适用前提 |
|------|------|----------|
| **Kotlin** | 首选 | 全场景，Android 原生 AI 工具链最优 |
| **Java** | 次选 | 存量 Java 代码库，新模块逐步引入 Kotlin 互操作 |
| **Flutter** | 有条件 | 双端产品 + 推理逻辑用 C++ FFI 实现，Dart 层只做业务编排 |
| **React Native** | 不推荐 | 仅作为团队无原生能力时的过渡方案 |

---

## AI 编程工具支持度

| 语言 | AI 补全质量 | 说明 |
|------|:-----------:|------|
| Python | ★★★★★ | 训练数据最多，全场景最优 |
| TypeScript | ★★★★★ | RN 业务逻辑层即纯 TS，支持完整 |
| JavaScript | ★★★★★ | - |
| Java | ★★★★ | 历史数据多，但生成风格偏老旧 |
| Kotlin | ★★★★ | Android 生态（Compose/Hilt/Flow）感知完整 |
| Dart/Flutter | ★★★ | 数据量少，较新 API 补全质量下降 |

### RN 分层说明

RN 的 AI 支持度需分层评估：

| 层 | 语言 | AI 支持 |
|---|---|---|
| 业务逻辑层 | TypeScript | ★★★★★ |
| React 组件层 | TSX | ★★★★★ |
| 原生模块桥接层 | JSI / TurboModule / C++ | ★★★ |

> RN 弱点在于跨层桥接代码（JSI/TurboModule），业务逻辑层 TS 的 AI 支持无短板。

---

## 推荐架构（Kotlin 方案）

```
app/
├── :feature-chat          # UI 层，Jetpack Compose
├── :domain                # 推理结果 UseCase，纯 Kotlin，可单独单测
├── :inference-engine      # 推理引擎抽象层
│   ├── InferenceEngine.kt       # sealed interface，屏蔽底层实现
│   ├── LiteRTEngine.kt          # LiteRT 实现
│   └── OnnxEngine.kt            # ONNX Runtime 实现
└── :model-manager         # 模型下载、版本管理、缓存
```

### 关键设计原则

- 推理引擎用 `sealed interface` 抽象，通过 Hilt 注入，测试时替换 FakeEngine
- Tensor 维度用 `@JvmInline value class` 封装，编译期防止维度混淆
- 推理任务使用 `Dispatchers.Default`，IO 任务用 `Dispatchers.IO`，禁止主线程调用推理 API
- 模型生命周期与 `viewModelScope` 绑定，`onCleared()` 中显式释放
