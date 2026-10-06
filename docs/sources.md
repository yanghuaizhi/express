# 来源与设计边界

Express 的规则、中文示例和程序独立编写。参考项目用于比较设计，不是上游依赖，也没有复制其代码、规则正文、标准词表或评测结果作为本项目成果。

## 借鉴的机制

| 来源 | 参考版本 | 借鉴 | 不直接采用 |
|---|---|---|---|
| [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill/tree/32511c6992ecb5f1971e46a2943f2e6adceedafe) | 0.4.0，32511c6 | 稳定术语、明确动作与条件、改写保真 | 英文词数、句数和语法限制作为通用质量门槛 |
| [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish/tree/a6fcb4fde098b33617cc1578d151ebf58774b883) | 2.1.1，a6fcb4f | 同时覆盖会话与文档、按需参考、会话启动上下文 | 硬禁表示可能性的词、会话全面禁止列表表格、按格式缺陷数量代表沟通质量 |

两个项目所检查版本均使用 MIT 许可证。本项目当前没有纳入它们的实质性内容；今后如复制代码或内容，应保留适用的版权与许可声明，并标明来源。

ASD-STE100 有独立的版权和使用条件。开源项目的 MIT 许可证不代表取得标准正文或词典的再分发权。Express 不附带标准，不做符合性认证，也不声称获得 ASD 或 OpenAI 背书。[ASD 官方网站](https://www.asd-ste100.org/)

[Andrej Karpathy 的公开帖文](https://x.com/karpathy/status/2105819303471976479)也启发了本项目对理解成本的关注。核验时，X 的公开嵌入可读到开头：他谈及人们理解模型输出所花的时间，以及个人使用 ASD-STE100 提示的经验。未取得官方完整长正文，不把转载后文作为规则或效果证明。Express 的默认表达、中文适配与载体选择是本项目的设计判断。

## 中文与质量检查

英文空格分词和英文标点切句不适合作为中文质量指标。中文规则围绕读者任务、对象关系、条件与语义；不把中文字符数重新包装成硬性上限。

格式或词汇检查不能证明改写忠实。Express 的行为检查保留完整输入，核对事实、范围、建议强度和使用条件；程序检查只验证文件结构、链接和 hook 协议，不替代内容验收。

公开示例均为独立编写的虚构材料，不含个人会话、内部业务记录或私人环境信息。输入列出输出所需的依据，避免只展示漂亮的前后对照，却遗漏新增内容的来源。

## Codex 依据

- [官方 Skill 机制](https://learn.chatgpt.com/docs/build-skills)：发现、按需加载、用户级与项目级安装、调用策略。
- [官方插件打包说明](https://developers.openai.com/plugins/build/plugins)：清单、市场目录与插件内 hook。
- [官方 hook 说明](https://learn.chatgpt.com/docs/hooks)：生命周期、上下文输出与原生信任机制。
- [Codex 0.159.2 的 SessionStart 输入定义](https://github.com/openai/codex/blob/ff6aec96948b70d94983af2641a6b67c94faeff5/codex-rs/hooks/schema/generated/session-start.command.input.schema.json)：包含 startup、resume、clear、compact、fork。

这些来源说明宿主能力，不证明本项目在所有客户端、模型和会话中都已有效。实际验证范围见[评估说明](../evals/README.md)。
