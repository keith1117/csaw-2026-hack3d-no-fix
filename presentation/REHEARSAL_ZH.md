# No Fix：10 分钟演讲排练稿

幻灯片共 12 页，时间安排合计 10:00。英文正文约 1121 词。每页 PPT 的 speaker notes 也有相同讲稿和中文提示。建议第一次排练严格计时，按要点讲，不必逐字背。

| 页 | 时间 | 主题 |
| --- | --- | --- |
| 1 | 0:00-0:35 | A simple game of Chess |
| 2 | 0:35-1:15 | The starting files |
| 3 | 1:15-2:00 | Looking inside the STEP model |
| 4 | 2:00-2:45 | The QR pattern inside the board |
| 5 | 2:45-3:45 | The pawn positions form a bit stream |
| 6 | 3:45-4:35 | Six bits at a time |
| 7 | 4:35-5:15 | The final height table |
| 8 | 5:15-6:00 | The rook gives the ZIP password |
| 9 | 6:00-6:45 | The recovered Queen-Pawn assembly |
| 10 | 6:45-7:35 | The King's linked toolpath |
| 11 | 7:35-8:40 | The Knight file stops early |
| 12 | 8:40-10:00 | Our results and checks |

## 1. A simple game of Chess (0:00-0:35)

开场先介绍 No Fix。说明任务是从文件中找制造信息，不要说我们已完成实体制造。封面图来自题目说明。

英文讲稿：

Hi, we are No Fix. Our challenge was to recover manufacturing information hidden in a chess assembly. We started with a STEP model, a problem statement, and an encrypted pawn archive. We will show how we inspected those files, followed the clues, and checked the results. The images in this presentation come from the supplied files or from our analysis of their geometry and toolpaths.

## 2. The starting files (0:35-1:15)

强调三个输入文件及各自作用。文本搜索只看到名称，下一步才转向几何。不要把未成功的字符串搜索说成成功解密。

英文讲稿：

The distribution had three files. The chess STEP was our main source of clues. The PDF explained what we needed to submit, and the ZIP contained pawn files that needed a password. We first searched the STEP as text. That gave us part names and export information, but no readable password. We then inspected the geometry itself. We kept the original files unchanged and recorded hashes so that our results refer to the exact files we received.

## 3. Looking inside the STEP model (1:15-2:00)

解释为什么需要内部查看。129 是 solid instances，不等于 129 种零件。几何文字由我们读取，采样和解码由脚本完成。

英文讲稿：

Our script loaded the STEP assembly and applied its placements. It found 129 solid instances, including 37 repeated pawn shapes. Several clues sat inside the board or inside other pieces, so an outside view was not enough. We drew selected flat faces and removed covering geometry from the inspection views. This cutaway shows why that helped with the king: its outer shape hides a lattice and a narrow central body. We also kept manual transcriptions separate from the code, because our script does not automatically read every geometric letter.

## 4. The QR pattern inside the board (2:00-2:45)

指一下三个定位角。说明失败原因是物理格子之间有间隔，中心采样后才能扫。这里只讲材料名称，具体工艺表在 report。

英文讲稿：

Inside one board layer we found a pattern with three QR corner markers. A direct scan failed because the physical modules had gaps. We sampled the center of each module in a 25 by 25 grid, filled the modules, and added a white border. The restored code decoded to tinyurl dot com slash Hack3d26. We followed the redirect to the official AlF357 material sheet. We recorded that material source separately from the prototype files, and kept its original link so the full specification remains available.

## 5. The pawn positions form a bit stream (2:45-3:45)

这一页要慢一点：occupied=1，empty=0；先 rank 8，每行 A 到 H。可以指第一行 00011101。第一次方向错是实际发生的尝试。

英文讲稿：

The board's edge told us that every square had a value, whether occupied or empty. It also said to begin at the highest rank and read six at a time. That suggested binary data. We assigned one to a square with a pawn and zero to an empty square. We mapped all 37 pawn centers to the eight by eight grid and checked that no square received two pawns. Our first row direction gave an unhelpful string. We checked the engraved rank labels and found that rank eight was on the negative Z side of the imported model. Reading rank eight first, then A through H in each row, gave the bit stream shown here.

## 6. Six bits at a time (3:45-4:35)

展示一个完整例子：000111=7，索引从 0 开始，第 7 位是 H。解释总共 64 位，只使用前 60 位，末尾 0000 记录为剩余位。有效跳转确认十字符结果。

英文讲稿：

We also found an alphabet with 64 characters on the board. Six bits can represent the numbers zero through 63, so each group gave us an index into that alphabet. For example, 000111 is seven, which selects H. The next groups give a, c, and k. The first 60 bits spell Hack3d26-2. Four zero bits remain at the end of the board. Extending those into another full group would add an A. We kept the ten-character message, followed the resulting short link, and received a Knight G-code file. That actual redirect checked our interpretation.

## 7. The final height table (4:35-5:15)

按表快速读出 K9、Q8、R5、B7、Kn6、P5 cm。强调 final target 与 prototype geometry 分开，复杂机构不能盲目整体缩放。

英文讲稿：

A second binary pattern on the bottom had six labeled rows. We read shallow positions as one and deep positions as zero. The rows decoded to nine, eight, five, seven, six, and five. The labels identify the pieces, and the nearby ruler says centimeters. This gives the target heights in the table. Another note says that final sizes may not match the prototype parts. We therefore kept these target values separate from the current CAD dimensions instead of treating every bounding box as a final size.

## 8. The rook gives the ZIP password (5:15-6:00)

先指 Zkdw，再讲减 3 得到 What。Queen 要大写 Q。成功依据是两个 ZIP 成员都通过 CRC，不是只看到一个文件名。

英文讲稿：

The rook had an encrypted sentence near its base. We isolated the lettering and tried a Caesar shift. Moving each letter back three places changed Zkdw into What, and the full line asked what the best piece was for a pawn to turn into. We tried Queen, with an uppercase Q, as the archive password. Both files extracted successfully and passed their ZIP checks. This was stronger evidence than just guessing a chess word. Earlier guesses based on the heights and short links had failed.

## 9. The recovered Queen-Pawn assembly (6:00-6:45)

区分 21 个标签与 31 个实际打印件。硬件按原图抄录，磁铁为 inch，其余 mm。我们没有实际装配测试，避免宣称功能验证成功。

英文讲稿：

The archive contained a STEP assembly and this exploded drawing, labeled Queen-Pawn. The STEP opened as 31 solid instances. The drawing uses 21 part labels, with repeated quantities that also total 31 printed pieces. It adds hardware information that the simple pawn outside shape did not provide. We recorded two magnets, two small springs, one larger spring, and the two pin sizes shown in the table. We preserved the original drawing and CAD so that the assembly positions and exact source dimensions can be inspected later.

## 10. The King's linked toolpath (6:45-7:35)

区分内部链接与已下载文件。说明 King 有正常结束，但层数差 1。金属字样与 FDM 指令不一致，这个证据边界要主动讲清楚。

英文讲稿：

The king's central body carried a tiny Drive link. After enlarging the letters and correcting our first transcription, we downloaded the King G-code. This image shows its outer-wall extrusion paths reconstructed from the commands. The file uses a Prusa i3 MK2 profile, a 215 degree extruder setting, an 80 degree bed, and nominal 0.2 millimeter layers. It includes an ending with heater-off commands. We found one count mismatch: 337 layers in the header, but 336 marked sections. The inscription also mentions metal units, while the linked file contains filament extrusion commands. We report both facts without treating this as a tested metal build recipe.

## 11. The Knight file stops early (7:35-8:40)

重点讲恢复路线：发现截断，读末尾备用链接，拿到原始 STEP。不要说我们修好了 G-code。表中 King 的小差异和 Knight 的缺失要区分。

英文讲稿：

The Knight file had a larger problem. Its header declared 177 layers and a maximum Z of 34.95 millimeters. We found only 78 numbered sections, ending at layer 77, and the highest motion reached 15.75 millimeters. It also lacked the normal heater-off ending. Near the end, two plain-text lines explained what to do if the file was corrupted and supplied an original-model link. We followed that link and recovered Knight-Full Assm dot step. It opened as a full assembly with 61 solid instances. We kept the partial G-code unchanged and included that original model beside it. Adding an end command alone would not bring back the missing upper-layer geometry.

## 12. Our results and checks (8:40-10:00)

最后把结果逐项对回线索。留出几秒停顿，让观众看表。明确我们完成的是文件解题与证据整理，没有实体制造和公差验证。结尾邀请提问。

英文讲稿：

Our main result is a set of recovered sources with a clear path back to each clue. We have the alloy specification link, six target heights, the pawn CAD and drawing, the King G-code, and the Knight G-code with its original STEP recovery. We checked the short-link destinations, the binary decodes, the ZIP members, the recovered CAD imports, and the G-code contents. We also recorded attempts that failed, including a direct QR scan, the wrong row direction, and several password guesses. Our repository includes the code, evidence views, original distribution, and recovered files. The report and upload packages keep those results together. We have not manufactured a finished set, so physical fit, printing, and final-size adjustments remain untested. Thank you. We are ready for your questions.

## 问答准备

**为什么不是 64 位全部转成 11 个字符？** 前 60 位组成 Hack3d26-2，剩下四位为 0000。补成第六位会多一个 A；十字符链接实际有效。我们把剩余位记录在结果中。

**为什么密码是 Queen？** Rook 的 Caesar -3 明文是一个兵升变问题。Queen 这个大小写组合成功解密两个文件并通过 CRC。这里的成功解密比一般棋理判断更直接。

**为什么高度单位是 cm？** 六个行标签对应棋子，旁边尺子的几何文字写着 cm，另有原型与最终尺寸可能不同的说明。

**你们的代码自动读出了所有文字吗？** 没有。脚本导出几何证据视图，我们手动读取铭文。程序负责 STEP 导入、采样、二进制/QR 解码、ZIP 校验和 G-code 内容检查。手动转录单独保存为 JSON。

**King 的 G-code 可以作为金属打印参数吗？** 不能据此下结论。铭文提到金属，但链接文件是 Prusa/Cura 的挤出指令；金属材料来源是棋盘 QR 指向的数据表。我们没有做金属成形测试。

**Knight G-code 修复了吗？** 没有修改原文件。我们发现缺失层段后，通过文件末尾的备用链接恢复了原始完整 STEP。仅添加结束指令无法恢复缺失几何。

**31 与 21 为什么不同？** Queen-Pawn 图上有 21 个零件标签，但 Q1、Q3 各两件，Q6、Q13 各五件，合计 31 个打印件，也与 STEP 的 31 个实体实例相符。

**最终尺寸与复杂机构硬件怎么配合？** 我们恢复了目标高度和硬件尺寸，没有编造缩放、公差或装配测试结果；后续制造需要单独确认。

**展示的图片是实物照片吗？** 不是。它们来自题目原图、原始装配 PDF，或我们对 CAD/实际 G-code 的可视化。颜色仅帮助区分几何体。
