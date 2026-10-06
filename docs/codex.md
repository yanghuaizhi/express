# 在 Codex 中安装与验证

Express 提供标准 Skill 和可选的会话启动插件。安装、规则加载与输出效果是不同层面的验证，不能互相替代。不要同时安装两个入口，否则技能选择器可能出现重复项。

若目标是日常回复默认清楚，使用下面的插件方式。共同原则在会话生命周期中加载；详细 Skill 用于复杂关系、取舍、纠正和文档表达。日常无需反复输入 `$express`，也不会每轮重新运行启动脚本。自动匹配和模型遵循仍需用实际答复检查。

## Skill 方式

将仓库中的 `skills/express` 整个目录复制到以下一种位置：

- 个人使用：`~/.agents/skills/express`。
- 仅在某个仓库使用：该仓库的 `.agents/skills/express`。

保留目录结构，不能只复制 `SKILL.md`。目标已存在时先比较版本，不直接覆盖手改文件。支持符号链接的环境也可以链接完整 Skill 目录。

在新会话中输入 `$express`。桌面客户端也可以在技能选择器中选择“Express · 清楚表达”。若没有出现，先核对目录，再重启客户端。[官方加载机制](https://learn.chatgpt.com/docs/build-skills)

自动调用由模型依据描述选择；单独安装不等于每轮调用。当前会话可明确要求持续采用该表达方式，但不应据此声称其他已打开会话也已改变。

## 插件方式

在本仓库根目录执行：

```bash
codex plugin marketplace add .
codex plugin add express@express-marketplace
```

以上命令会登记市场来源并安装插件。安装前可先查看 `.codex-plugin/plugin.json`、`hooks/hooks.json`、`hooks/session_start.py` 和 `skills/express/references/core.md`。市场入口在 `.agents/plugins/marketplace.json`，插件使用 Codex 的 `.codex-plugin/plugin.json` 清单。

安装插件后，在 Codex 原生界面审阅并信任 hook。CLI 可用 `/hooks`；启动提示也提供审阅入口。未信任时会跳过，不应把“已安装”说成“已生效”。不要通过手写信任哈希或跳过信任参数代替审阅。[官方 hook 机制](https://learn.chatgpt.com/docs/hooks)

启动 hook 使用 `python3` 命令。该命令必须在宿主运行环境的 PATH 中可用；只有 Skill 的安装方式不需要 Python。受管环境可能限制 hook，这时可先采用 Skill 方式。未经验证，不宣称所有操作系统和客户端均已支持。

## 规则怎样进入会话

1. 宿主触发 `SessionStart`。
2. 已信任的脚本读取包内 `skills/express/references/core.md`。
3. 脚本输出 `hookSpecificOutput.additionalContext`，宿主将它加入上下文。
4. 具体任务需要详细方法时，再加载 Skill 和对应参考。

在已核对的 Codex 0.159.2 定义中，启动、恢复、清空、分叉和压缩分别对应 `startup`、`resume`、`clear`、`fork`、`compact`。本项目不设置 matcher，以覆盖该事件的全部来源。这些是已核对的宿主契约；逐项端到端运行仍需实际环境验证。

hook 不读取 stdin，不打开 `transcript_path`，不访问网络、不写文件、不保留状态；它不会恢复个人记忆或任务进度。只注册 `SessionStart`，不声称覆盖所有子代理。当前用户指令、项目约定和明确的文风选择优先于默认表达规则。

`additionalContextLimit` 设为 `0`，使用该版本支持的完整注入机制；规则通过内容编辑维护，不依赖运行时截断。宿主和模型仍有各自的上下文限制。

## 检查实际生效

- **发现**：技能选择器或原生技能目录中有 Express，路径对应当前安装。
- **加载**：原生 hook 状态显示信任且执行成功。静态 `codex debug prompt-input` 可以辅助检查 Skill 目录，但不会单独执行 SessionStart，不能代替这一步。
- **效果**：开一个新会话，使用与实际工作相近的输入，检查答案、依据、必要信息与原意。不要仅询问模型“你是否加载了规则”来验收。

支持恢复或压缩的客户端，应继续验证这些事件之后的实际行为。不能根据一次启动成功推断全部客户端、旧会话及未来任务都有效。

## 更新与移除

维护打包时保留 Codex 清单入口。在已核验的 Codex 0.159.2 中，根目录的通用 `plugin.json` 会优先于 `.codex-plugin/plugin.json`，而该通用格式的加载分支会跳过插件 hook。这会造成 Skill 已发现、启动规则却缺失。未来若改格式，需要同时验证原生 Skill 目录与 hook 目录，不能只做 JSON 格式检查。

更新前保留自己的修改，比较共同原则、Skill 和 hook 的变更。使用登记的市场来源时，可刷新市场并按客户端提示更新插件：

```bash
codex plugin marketplace upgrade express-marketplace
```

核对本次实际安装的版本，再用一个代表性任务检查输出。Codex 的信任哈希对应 hook 定义；包内规则或脚本内容更新不一定触发再次确认，因此不能用“没有提示”代表“内容没变”。

插件移除使用原生插件管理功能。CLI 命令及参数以 `codex plugin remove --help` 为准；不要删除整个个人技能目录或覆盖全局配置。单独安装的 Skill 可以在保留本地修改后移除 `express` 目录。

若同时使用其他写作插件，保留各自上游安装，不修改缓存内规则来维持个人偏好。表达冲突依据当前用户要求解决；长期共存应检查两者的触发范围，不默认叠加整套流程。
