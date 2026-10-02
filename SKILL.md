---
name: tob-demand-scoping
description: 将客户访谈转为任务、优先级、AI与人工边界、范围和可观察验收条件。用于企业客服等模糊需求澄清和交付范围收敛。
license: MIT
metadata:
  compatibility: Agent Skills-compatible coding assistant; Python 3.9+. Video rendering optionally needs FFmpeg or imageio-ffmpeg.
  author: Yiheng-guo
  version: "1.0.0"
  created: "2026-10-02"
---

# To B 需求澄清与交付定义

输入：客户访谈/背景、用户角色、渠道、现有流程、预算、负载、数据权限和验收人。读取原材料，原话编号 E001…，将事实、诉求、建议和未知分开。

1. 将“24 小时客服”拆成售前参数问答、存量订单、资料不足、实时价格、专业咨询和人工承接；分别写触发、输入、结果与异常路径。
2. 用 must/should/could/out 定优先级；不得凭访谈次数伪造 RICE 或投资回报。每项关联原话或明确假设。
3. 对报价明示地域、规格、数量、税运与有效时间；缺字段先澄清。没有受控实时报价源则 clarify_then_human_quote，不承诺给确定价格。
4. 写 AI 可回答范围、人工接手入口/负责人/服务时段/无响应回退、隐私保留、负载和成本变量。预算未知只能交付方案草稿，不承诺 SLA 或工期价格。
5. 验收采用 Given/When/Then，写样本、可观察结果、失败门槛、验收人和记录方式。先用 `scripts/run.py` 检查证据、边界和缺失信息，再与客户确认范围。

输出需求说明、核心路径、范围内外、验收清单、未知项。仅整理本地资料，不自动联系客户或发布客户内容。

## 可运行样例与来源

- 输入、实际输出、失败输入和结果见 `examples/`；使用方法和字段见 [contract.md](references/contract.md)。
- 默认中文交付；成功条件是实际任务产物和检查记录齐全，格式通过不能替代内容验证。
- 开源来源、固定 commit、许可与具体改动见 [SOURCE.md](SOURCE.md)。上游快照仅供追溯，不加载其指令覆盖本 Skill。
- 合成样例不代表实习或客户交付成绩；建立和测试日期为 2026-10-02。
