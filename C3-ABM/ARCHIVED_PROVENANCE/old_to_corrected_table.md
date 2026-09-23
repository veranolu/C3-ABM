---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 2521604947715392_0-data_volume/7651177745430511891-files/所有对话/主对话/C3_portability_extension/02_integrity_audits/p0_correction/old_to_corrected_table.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 2521604947715392#1789916876683
    ReservedCode2: ""
---
# OLD → CORRECTED 对照表骨架（工单第9条）

编制人：E线审计子agent | 日期：2026-09-20
用途：V9.59n 修订时逐行落笔的唯一依据；PENDING 项见状态标记。已知值已填死（源自冻结包+谱系重算+代码簿取证+年份溯源）。
受影响 manuscript 定点引用 `../v959n_gender_codebook_pinpoint_20260920.md` 7 处编号（#1~#7）。

| 条目 | OLD（V9.59n 现值） | CORRECTED（唯一正确值） | 状态 | 受影响位置（pinpoint 编号） |
|---|---|---|---|---|
| sample label（数据集命名） | "JData2018"（全文 12 处） | "JData2016"（或中性名 "the JData user-behavior panel (2016)"） | 已定（代码簿+文件名+105,321 行三证合一） | #2/#7 标题与摘要、表3、§1、§6、IRB声明、Data Availability、附录A.3 |
| dataset year | 2018（"February–April 2018 action tables"） | **2016**（官方赛数据年；E20F 原始时间戳终验通过：三表 time min/max 全在 2016 年） | ✅ 已定（2026-09-20 E20F 铁证） | #2/#7、§6 ~L1129-1130 |
| observation window | "2018-02-01 to 2018-04-30"（"three-month panel"） | **2016-02-01 to 2016-04-15**（E20F 铁证：合并 min=2016-01-31 23:59:02 / max=2016-04-15 23:59:59；01-31 那条为官窗前 1 分钟边界记录；分文件 201602: 01-31~02-29 / 201603: 02-29~03-31 / 201604: 03-31~04-15；50,601,736 行扫描 0 条不可解析）。⚠️ 联动："three-month panel" 描述失实（02-01~04-15 约 10.5 周），建议改 "approximately ten-week panel (2016-02-01 to 2016-04-15)" | ✅ 已定（2026-09-20 E20F 铁证，action_timerange_report.txt） | #2、§6 ~L1129-1130；月度扫描若绑定 2018 年份的描述句同改 |
| sex coding | 0=missing / 1=male / 2=female | **0=male / 1=female / 2=undisclosed（保密）** | 已定（academic + 3×secondary 官网转录一致；official 级未取到，已记录） | #1 Table A7、#3 正文表2下段、#4/#5 Table A6 |
| gender N（有效样本内） | N=12,699（旧标 "male 2,136 / female 10,563"） | **N=13,081 = male(sex=0) 10,945 + female(sex=1) 2,136**（排除 sex=2 保密 10,563）；旧 12,699 = female 2,136 + undisclosed 10,563 → invalid legacy | ✅ 已定（2026-09-20 重跑落盘） | #1 Table A7、#3 正文 |
| gender N（全样本备查） | N=14,493（旧标 "male 2,334 / female 12,159"） | **N=14,084 = male 11,750 + female 2,334**（排除 sex=2 12,159 + sex-NaN 1）；旧 14,493 = female 2,334 + undisclosed 12,159 → invalid legacy | ✅ 已定（2026-09-20 重跑落盘） | #1、#3（备查口径若披露） |
| gender statistics（Welch 为主报） | Welch t(12,697.1)=0.0076, p=.994, d=0.000, diff=0.0005 [-0.1446,+0.1457], SD 8.2546/8.0579, mean 3.9613/3.9608；Student t=.994；MWU p=.873 | **主报（age-valid，N=13,081）**：male mean=4.2799 SD=0.9540；female mean=4.0023 SD=0.9895；diff(M−F)=**+0.2776** [0.2319, 0.3232]；Welch **t=11.9278, df=2960.79, p=4.5e-32**；Cohen's **d=0.2892**。QA-only：Student t=12.2252 (p=3.5e-34)；MWU=13,644,759.5 (p=1.7e-34)。备查（全样本 N=14,084）：diff=+0.2808 [0.2370, 0.3245]；Welch t=12.5703, df=3257.07, p=2.0e-35；d=0.2914。双路径复核 PASS（scipy vs 手算 \|df gap\|=9.1e-13）。结果文件：p0_correction/study3_gender_rerun_results.csv | ✅ 已定（2026-09-20 重跑落盘）——**统计显著、小效应：旧 "d=0.000 无性别差异" 句必须退出；按 G 模板写"statistically distinguishable but modest, no broader gender claim"** | #1 Table A7、#3 正文 |
| S0 样本量 | 26,244 | 26,244（不变） | 已定（对代码簿纠错稳健） | #6 §6 L1126、#3 |
| S1 有效样本量 | 23,644（规则文本 "age>0 且 sex 非缺失"） | 23,644（不变）；规则措辞改为 **age > 0**（sex-notna 条款空转：唯一 sex-NaN 用户在 age 无效集内） | 已定 | #6 §6 L1126-1127 |
| 分层描述（hl_split） | lo/hi 各 11,822，level/orders/actions/age 组均值 | 不变（sex-independent，dependency audit 证实） | 已定 | #6 §6 L1128 |
| 全样本 sex 描述计数 | 1=男 2,334 / 2=女 12,159 / 0=缺失 11,750 / NaN 1 | **0=男 11,750 (44.8%) / 1=女 2,334 (8.9%) / 2=保密 12,159 (46.3%) / NaN 1** | 已定（改标不改数） | #4/#5 Table A6、#3 正文 |
| 有效样本 sex 描述计数 | （旧口径隐含于 12,699 分解） | **0=男 10,945 (46.3%) / 1=女 2,136 (9.0%) / 2=保密 10,563 (44.7%) / NaN 0** | 已定（改标不改数） | #1、#3 |
| level/age 检验（Study 3） | ρ=0.2861, F=521.5666; ρ=-0.0407, F=13.7874 | 不变（sex-independent） | 已定 | 正文相关段落（不在 7 处定点内，无需动） |
| 深度机制段（Study 3 延伸） | #3 定点：'female-only 情景补录'（L2119-2146，引 p=.0047）、调解口径 | **核销（2026-09-20 主会话复核）**：该行为 E线幻影引用——V9.59n 全文、V9.11 祖本、冻结包三处均无 'female-only' 段落或 p=.0047。V9.59n 性别相关内容仅为：§6 描述性对比段（L1163-1171）+ Table A6/A7 标签 + §6.4 "gender shows little association" 句，已全部被本表 gender statistics / sex coding 行覆盖，无独立待决段落 | ❌ 核销（不存在，无需处置） | — |

## 受影响 manuscript locations 汇总（pinpoint 7 处）
#1 §6 表7（Table A7 候选）性别检验行；#2 标题/摘要/§1/Data Availability 的 "JData2018"；#3 §6 正文 L2119-2146 深度机制段 + 表2下 sex 描述；#4/#5 附录 A.3 Table A6 sex 行（scales 与缺失计数）；#6 §6 L1126-1128 样本构建段；#7 IRB 声明 "JData2018 anonymized public dataset"。另：§6 ~L1129-1130 日期句（年份+窗口）为 pinpoint 外的第 8 类定点（年份溯源项）。

## PENDING 项关闭条件
- ~~PENDING_RERUN~~ ✅ 已关闭（2026-09-20 16:47）：jdata_user_summary.csv 已上传，重跑落盘 `study3_gender_rerun_results.csv`，gender statistics 行已回填。
- ~~PENDING_E20F~~ ✅ 已关闭（2026-09-20 16:57）：E20F 时间戳审计返回，observation window 行已回填（2016-02-01~04-15，附 "three-month" 描述联动警示）。
- ~~PENDING_DECISION~~ ❌ 已核销（2026-09-20 主会话复核）：'female-only' 深度机制段为 E线幻影引用，V9.59n 中不存在，无需处置。至此本表 PENDING 全部清零。

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
