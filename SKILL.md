---
name: daily-brief
description: 每日自动抓取 VC/投资圈、科技与 AI 领域的情报，整合官方新闻、Reddit 热门讨论和知名投资人/创业者的 Twitter/X 动态，生成结构化日报。当用户要求生成每日简报、投资圈日报、VC 情报、科技动态、或调用 daily-brief 时触发。支持中文、英文、双语输出，以及多种语言风格。
---

# Daily Brief · VC & 科技情报日报

每日整合三类来源，生成一份结构化情报简报：官方新闻、社区讨论、一线投资人与创业者动态。

---

## 调用流程

每次调用时，**先完成以下两步交互确认，再执行搜索**：

### 第一步：语言偏好

向用户提问：

> 请选择输出语言：
> 1. 中文
> 2. English
> 3. 中英双语（重要内容双语呈现）

等待用户回复后继续。

### 第二步：风格偏好

向用户提问：

> 请选择简报风格：
> 1. **简报体** — 每条一句话，适合快速扫读
> 2. **深度分析** — 带背景与判断，适合深入理解
> 3. **新闻体** — 正式新闻写作，适合对外分享
> 4. **对话体** — 轻松口语化，像朋友帮你整理

等待用户回复后，进入执行阶段。

---

## 信息来源配置

### 一、官方新闻来源

**英文媒体（优先）：**
- `techcrunch.com` — 早期融资、创业公司动态
- `fortune.com/tag/term-sheet` — 每日融资简报
- `axios.com/pro/private-deals` — PE/VC 专项
- `news.crunchbase.com` — 融资数据与分析
- `pitchbook.com/news` — 数据驱动融资报道
- `strictlyvc.com` — VC 圈访谈与动态
- `bloomberg.com/technology` — 宏观资金与大盘

**中文媒体（优先）：**
- `36kr.com` — 国内融资、创投动态
- `latepost.com` — 深度独家报道
- `investorchina.cn` — 机构动态、LP 市场
- `huxiu.com` — 商业分析、行业趋势
- `yicai.com` — 宏观政策、产业资本

### 二、Reddit 社区

- `r/venturecapital` — VC 从业者讨论
- `r/startups` — 创始人视角，融资真实经历
- `r/YCombinator` — YC 生态与创业经验
- `r/artificial` — AI 赛道讨论与融资事件
- `r/SaaS` — SaaS 赛道创始人与投资人
- `r/techstartups` — 科技创业动态

### 三、Twitter/X 账号监控

**顶级 VC 合伙人：**
- `@paulg` — Paul Graham，Y Combinator 创始人
- `@sama` — Sam Altman，OpenAI CEO
- `@benedictevans` — Benedict Evans，科技宏观趋势分析
- `@pmarca` — Marc Andreessen，a16z 联创
- `@chamath` — Chamath Palihapitiya，宏观经济观点
- `@bhorowitz` — Ben Horowitz，a16z 联创
- `@bgurley` — Bill Gurley，估值与市场深度研究
- `@jason` — Jason Calacanis，早期投资 + All-In 播客
- `@ericpaley` — Eric Paley，Founder Collective
- `@hunterwalk` — Hunter Walk，Homebrew VC
- `@sriramk` — Sriram Krishnan，a16z / AI 政策

**创业者 / 科技领袖：**
- `@elonmusk` — Elon Musk，Tesla/SpaceX/xAI
- `@garrytan` — Garry Tan，YC 现任 CEO
- `@andrewchen` — Andrew Chen，a16z / 增长
- `@navalmravikant` — Naval Ravikant，AngelList 创始人
- `@lennysan` — Lenny Rachitsky，产品与增长
- `@gregisenberg` — Greg Isenberg，社区产品

---

## 执行步骤

确认语言和风格后，**按顺序执行以下 5 次搜索**，不要跳过任何步骤：

### 搜索 1：今日重大融资事件

```
搜索词：site:techcrunch.com OR site:news.crunchbase.com "raises" OR "funding" [当日日期]
备用词：site:36kr.com "融资" [当日日期]
补充词：venture capital funding rounds [当日日期]
```

目标：找出当日金额 $5M+ 或赛道重要的融资事件，取 3–5 条。

### 搜索 2：官方媒体深度报道

```
搜索词：site:fortune.com OR site:axios.com OR site:pitchbook.com venture capital [当月年份]
备用词：site:latepost.com OR site:huxiu.com 投资 创业 [当月]
```

目标：找出近 48 小时内的深度报道或行业分析，取 2–3 条。

### 搜索 3：Twitter/X 投资人动态

对以下账号分组搜索：

```
搜索词（组 1）：site:x.com/paulg OR site:x.com/sama OR site:x.com/pmarca [近期]
搜索词（组 2）：site:x.com/chamath OR site:x.com/bgurley OR site:x.com/jason [近期]
搜索词（组 3）：site:x.com/garrytan OR site:x.com/navalmravikant OR site:x.com/elonmusk [近期]
```

目标：找出近 24–48 小时内上述账号的有价值观点或动态，取 3–5 条，注明账号来源。

### 搜索 4：Reddit 热门讨论

```
搜索词：site:reddit.com/r/venturecapital OR site:reddit.com/r/startups [当周]
备用词：site:reddit.com/r/artificial OR site:reddit.com/r/ycombinator hot [当周]
```

目标：找出本周上升最快或讨论最热的帖子，取 2–3 条，注明子版块来源。

### 搜索 5：热门赛道信号

```
搜索词：top funded sectors AI startups [当月年份] venture capital
备用词：最热投资赛道 AI [当月] 融资 创投
```

目标：识别本周最活跃的 1–3 个投资赛道，并找到具体事件佐证。

---

## 输出模板

搜索完成后，根据用户选择的**语言**和**风格**，从以下模板中选择对应版本输出。

### 简报体

```
📊 Daily Brief · [日期]

━━━━━━━━━━━━━━━━━━
💰 今日融资速览
━━━━━━━━━━━━━━━━━━
• [公司名]（[地区]）完成 [金额] [轮次] | 赛道：[X] | 投资方：[X]
• [重复，共 3–5 条]

━━━━━━━━━━━━━━━━━━
📰 媒体深度
━━━━━━━━━━━━━━━━━━
• [一句话标题] — [来源媒体]
• [重复，共 2–3 条]

━━━━━━━━━━━━━━━━━━
🎙️ 投资人在说什么
━━━━━━━━━━━━━━━━━━
• @[账号]：[观点，一句话]
• [重复，共 3–5 条]

━━━━━━━━━━━━━━━━━━
💬 社区热议
━━━━━━━━━━━━━━━━━━
• [话题摘要，一句话] — r/[子版块]
• [重复，共 2–3 条]

━━━━━━━━━━━━━━━━━━
🔥 今日赛道信号
━━━━━━━━━━━━━━━━━━
• [赛道名]：[一句佐证]

━━━━━━━━━━━━━━━━━━
📌 编辑观察
━━━━━━━━━━━━━━━━━━
[2–3 句，今日最值得关注的一个信号，有判断，不废话]

─────────────────
数据来源：公开网络信息汇总 · 仅供参考
```

### 深度分析体

在简报结构基础上，每条信息附加：
- **背景**：为什么这条值得关注
- **判断**：这对市场或赛道意味着什么
- **延伸**：值得继续跟踪的方向

### 新闻体

使用正式新闻写作语言，每个板块用 2–4 句段落代替要点列表，标注所有信息来源，使用第三人称。

### 对话体

用口语化表达，像朋友帮你整理一样：
- 使用"今天有个事挺有意思的"、"这个人说了个挺有意思的观点"等引导
- 每条信息配一句个人评论
- 整体轻松，不刻板

---

## 质量控制规则

- **时效性**：融资信息必须是近 48 小时内的。若当日信息不足，注明"以下为近 48 小时动态"。
- **信息不足**：某板块无结果时，写"今日暂无重要动态"，**不捏造信息**。
- **来源透明**：投资人观点必须注明账号和来源平台；Reddit 内容注明子版块。
- **金额统一**：中英文混排时统一标注（$10M / ¥1亿）。
- **不确定信息**：无法确认真实性的信息直接跳过，不猜测或补全。
- **信噪比**：@elonmusk 等高流量账号优先选取与投资/科技/AI 直接相关的内容，过滤无关话题。

---

## 调用示例

**在 OpenClaw / Claude Code 中触发：**

```
/daily-brief
```

```
帮我生成今天的 VC 日报
```

```
今天投资圈有什么值得看的
```

**交互示例：**

```
用户：/daily-brief

Assistant：
好的，开始生成今日 Daily Brief。

请选择输出语言：
1. 中文
2. English
3. 中英双语

用户：1

请选择简报风格：
1. 简报体 — 每条一句话，快速扫读
2. 深度分析 — 带背景与判断
3. 新闻体 — 正式，适合对外分享
4. 对话体 — 轻松口语化

用户：2

好的，正在抓取今日情报，请稍候……
[执行 5 次搜索后输出完整日报]
```
