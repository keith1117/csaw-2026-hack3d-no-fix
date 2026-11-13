# No Fix 提交指南

团队名填写 **No Fix**。

根据你提供的截图，三个文件栏分别上传：

| 表单栏 | 本地文件 | 内容 |
| --- | --- | --- |
| Team Report | `submission/No_Fix_Team_Report.pdf` | 2026 年 11 月 13 日重写的最终版英文第一人称报告，共 18 页、9 个章节 |
| Code Upload | `submission/No_Fix_Code.zip` | Python 分析代码、原始输入、全部五份恢复文件（含两份 G-code）、结果及英文复现说明 |
| Any additional supporting files | `submission/No_Fix_Supporting.zip` | 演讲 PDF、恢复的 CAD、Pawn 原始装配 PDF 和关键证据 |

报告和代码包分别低于 100 MB，supporting 包低于 10 MB。确切字节数及 SHA-256 见 `submission/manifest.json`。

题目 PDF 内嵌的表单链接为 [CSAW Final 提交表单](https://forms.gle/37FnBhtgzwHsPjmM9)。我没有填写或提交表单。

## 演讲文件

使用当前保存的演讲文件 `presentation/output/No_Fix_presentation.pptx`。共 12 页，notes 依据最新 18 页报告组织，用口语表达连接句子，说明每一步的依据及其与下一页的关系，另有同名 PDF 作为显示备用。正式安排为 **7 分钟演讲 + 3 分钟评委提问**，四位成员每人约 1 分 45 秒。原 PPT 和原讲稿保留。

每页 speaker notes 均包含对应的英文稿、中文稿、承接逻辑、指图提示和问答资料。完整分人讲稿见 `presentation/SPEAKER_SCRIPTS_NATURAL_EN_ZH.md`，排练说明见 `presentation/REHEARSAL_ZH.md`。承接逻辑和问答资料供排练与备答使用，不计入朗读。A 负责第 1-3 页，B 第 4-6 页，C 第 7-9 页，D 第 10-12 页；在 1:45、3:30、5:15 交接，7:00 结束。中英文现场选择一种语言。

本次提交仅包含演讲 PDF，已加入 supporting 包；原生 PPTX 保留本地用于演讲。两份原始 G-code 完整保留在代码包中。

## 题目所说的单一 ZIP

题目 PDF 还写了团队名 ZIP 的要求。`submission/No Fix.zip` 是总包，包含报告、代码包、supporting 包和幻灯片 PDF；内附英文 README。它用于比赛方要求一个总 ZIP 的情况。截图中的三个独立栏优先按上表分别上传。

## 提交内容中的实际限制

- Knight G-code 为原文件：只找到 78 个编号层段，头部声明为 177。末尾的备用链接恢复了完整 Knight STEP，已一并提供。
- King G-code 有结束指令，但头部 337 与实际 336 个编号层段相差 1。
- 棋盘的六个目标高度、原始 CAD 尺寸和文件内的打印设置已分开记录。
- 没有声称完成实体打印、机构装配或公差测试。

所有原始输入和恢复文件都保留了校验值。正式提交前可运行 `python src/verify_delivery.py`，检查压缩包和文件校验值。

## 提交包清理

所有提交 ZIP 均排除中文提交指南、排练稿及双语演讲稿文件。代码包使用独立的英文 README。`results/presentation_checks.json` 与 `results/report_typography.json` 是内部排版检查记录，保留在本地，不进入提交包。解码、源文件哈希、G-code 和 CAD 验证记录继续提交。
