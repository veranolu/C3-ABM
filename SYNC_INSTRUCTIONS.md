# GitHub 同步执行单（由作者在有网络与凭据的环境执行）

沙箱无法访问 GitHub（无凭据、网络不通），推送须由作者本人执行。本包已按 Coze 指定的三层结构组装完毕，内容与 V9.60B.6 封口稿同一事实版本。

## 执行步骤

```bash
# 1. 克隆现有仓库
git clone https://github.com/veranolu/C3-ABM.git
cd C3-ABM

# 2. 清空旧版内容（保留 .git），拷入本包
git rm -rf . --quiet
cp -r /path/to/C3_GITHUB_SYNC/C3-ABM/. .
# 注意：旧 README（V9.59n 时代）将被本包 README 覆盖

# 3. 提交
git add -A
git commit -m "Sync to manuscript V9.60B.6 (RED-TEAM GREEN): three-tier structure — PRIMARY_REVISED_ANALYSIS / ARCHIVED_PROVENANCE / GENERATIVE_PROBE"

# 4. 打两个锁定标签（指向同一提交）
git tag -a submission-V9.60B.6 -m "Repository state as cited in the submitted manuscript (V9.60B.6)"
git tag -a red-team-green-2026-09-23 -m "State at independent red-team GREEN sign-off"

# 5. 推送
git push origin main --tags
```

## 推送前硬性核对（30 秒）

- [ ] 包内**无** JDsearch/JData 原始数据（本包已确认：仅代码 + 派生结果表 + 文档）
- [ ] 仓库可见性为 public（Data Availability 声明其为 "publicly available"）
- [ ] 推送后浏览器打开仓库确认 README 渲染、三层目录在位、两个标签可见
- [ ] 回投稿系统前确认 Data Availability 中的 URL 与实际仓库一致：https://github.com/veranolu/C3-ABM

## 包内容清单（9 文件 + README）

- PRIMARY_REVISED_ANALYSIS/: bootstrap_cdi.py, results_study1_rewb.csv, results_study2_study3.csv, portability_multiverse_master.csv, cdi_robustness_envelope.csv, c3_portability_master_table.csv
- ARCHIVED_PROVENANCE/: old_to_corrected_table.md
- GENERATIVE_PROBE/: sim_rewb_boundary.py（v3 标签清理版）, simA_summary.csv（新版）
- README.md（V9.60B.6 口径：三层映射、probe 边界声明、数据可用性分层、冻结锚点、锁定标签说明）
