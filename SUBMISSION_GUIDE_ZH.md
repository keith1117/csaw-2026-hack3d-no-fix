# No Fix 提交指南

团队名填写 **No Fix**。

根据你提供的截图，三个文件栏分别上传：

| 表单栏 | 本地文件 | 内容 |
| --- | --- | --- |
| Team Report | `submission/No_Fix_Team_Report.pdf` | 英文第一人称团队报告，共 10 页 |
| Code Upload | `submission/No_Fix_Code.zip` | Python 分析代码、原始输入、已恢复文件、结果及复现说明 |
| Any additional supporting files | `submission/No_Fix_Supporting.zip` | 恢复的 CAD、G-code、Pawn 原始装配 PDF 和关键证据 |

报告和代码包分别低于 100 MB，supporting 包低于 10 MB。确切字节数及 SHA-256 见 `submission/manifest.json`。

题目 PDF 内嵌的表单链接为 [CSAW Final 提交表单](https://forms.gle/37FnBhtgzwHsPjmM9)。我没有填写或提交表单。

## 演讲文件

使用 `presentation/output/No_Fix_10_Minute_Presentation.pptx`。共 12 页，英文讲稿和中文提示都放在每页 speaker notes 中，时间安排合计 10:00。另有同名 PDF 作为显示备用。

排练时看 `presentation/REHEARSAL_ZH.md`，其中包含逐页时间、英文讲稿、中文要点和问答准备。1121 个英文单词按约每分钟 112 个词安排，建议实际计时排练一次。

题目说明要求在 **2026 年 11 月 13 日上午 8 点前**提交 PowerPoint，并在 11 月 13 日展示。PDF 未另外说明时区，请按比赛方通知确认。截图中未显示 PPT 专用栏；如果同一表单另有演讲文件栏，上传 PPTX。如果表单只显示截图中的三个栏，请保留 supporting 包给制造证据，按比赛方给出的演讲提交方式提交 PPTX。

## 题目所说的单一 ZIP

题目 PDF 还写了团队名 ZIP 的要求。`submission/No Fix.zip` 是总包，包含报告、代码包、supporting 包、PPTX、幻灯片 PDF 和本指南。它用于比赛方要求一个总 ZIP 的情况。截图中的三个独立栏优先按上表分别上传。

## 提交内容中的实际限制

- Knight G-code 为原文件：只找到 78 个编号层段，头部声明为 177。末尾的备用链接恢复了完整 Knight STEP，已一并提供。
- King G-code 有结束指令，但头部 337 与实际 336 个编号层段相差 1。
- 棋盘的六个目标高度、原始 CAD 尺寸和文件内的打印设置已分开记录。
- 没有声称完成实体打印、机构装配或公差测试。

所有原始输入和恢复文件都保留了校验值。正式提交前可运行 `python src/verify_delivery.py`，检查压缩包和文件校验值。
