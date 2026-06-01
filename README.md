# How to Learn Agent

这是一个面向中文学习者的 AI 项目与 Agent 项目教程。

当前仓库处于“课程规划与章节占位”阶段。这里暂时不追求写完正文，而是先把课程主线、章节边界、写作模板、协作规则和示例项目位置整理清楚，方便后续多人共同认领和补充。

## 项目目标

帮助读者从零开始理解并实践 AI 项目，逐步过渡到 Agent 项目。课程会按照“小白可跟上”的顺序组织：

1. 先理解 AI 项目是什么。
2. 再学会调用和控制 LLM。
3. 然后学习 RAG、工具调用和工作流。
4. 最后进入 Agent、评估、上线和综合项目。
5. 在每章嵌入成熟项目讲解，并通过源码 Lab 把概念和产业实践连起来。

## 当前最重要的文件

- [SUMMARY.md](./SUMMARY.md)：课程目录。
- [ROADMAP.md](./ROADMAP.md)：课程路线图和章节定位。
- [CURRICULUM_STRUCTURE.md](./CURRICULUM_STRUCTURE.md)：课程重构方案和三线结构。
- [PROJECT_TRACKS.md](./PROJECT_TRACKS.md)：贯穿项目和可选项目主线。
- [OPEN_SOURCE_CASES.md](./OPEN_SOURCE_CASES.md)：产学研开源案例映射。
- [LESSON_CASE_STUDIES.md](./LESSON_CASE_STUDIES.md)：每章成熟项目讲解索引。
- [labs/README.md](./labs/README.md)：源码 Lab 总览。
- [CHAPTER_TEMPLATE.md](./CHAPTER_TEMPLATE.md)：每章写作模板。
- [STYLE_GUIDE.md](./STYLE_GUIDE.md)：写作风格与内容边界。
- [CONTRIBUTING.md](./CONTRIBUTING.md)：多人协作规则。
- [GLOSSARY.md](./GLOSSARY.md)：统一术语表。

## 目录结构

```text
.
├── lessons/              # 主线课程，每章一个文件夹
├── projects/             # 综合实战项目
├── labs/                 # 为每章成熟项目讲解服务的源码 Lab
├── examples/             # 小型示例代码
├── assets/               # 图片、图解、流程图
├── resources/            # 延伸阅读和资料索引
├── ROADMAP.md            # 课程总规划
├── CURRICULUM_STRUCTURE.md # 课程重构方案
├── CHAPTER_TEMPLATE.md   # 章节写作模板
├── STYLE_GUIDE.md        # 写作规范
└── CONTRIBUTING.md       # 贡献指南
```

## 协作原则

- 每个章节都先写清楚“本章定位、承接关系、成熟项目讲解、写作任务、不要写什么”。
- 正式正文需要等章节边界确认后再补。
- 示例代码需要和章节目标绑定，避免为了炫技而增加复杂度。
- 每次 PR 尽量只改一个章节、一个示例或一个规划文件。

## 当前状态

课程目录、章节占位、项目主线和源码 Lab 已经预制。每章已经预留“成熟项目讲解”，下一步是逐章认领，先完善每章大纲、项目切口和对应 Lab 任务，再进入正文写作。
