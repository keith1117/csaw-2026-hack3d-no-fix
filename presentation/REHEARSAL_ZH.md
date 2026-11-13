# No Fix 7 分钟排练与问答

| 成员 | 页码 | 时间 | 报告复习范围 |
| --- | --- | --- | --- |
| A | 1-3 | 0:00-1:45 | §1、§9 |
| B | 4-6 | 1:45-3:30 | §2、§3 |
| C | 7-9 | 3:30-5:15 | §4、§5、§6 |
| D | 10-12 | 5:15-7:00 | §7、§8，了解 §9 |

当前使用自然口语版 No_Fix_7_Minute_Natural_Notes.pptx。完整中英文讲稿见 SPEAKER_SCRIPTS_NATURAL_EN_ZH.md，也已写入每页 PPT 的 speaker notes。先按英文约每分钟 100-105 词排练，再依据实际指图和换人耗时调整。中文为逐页对应版本。原 SPEAKER_SCRIPTS_EN_ZH.md 保留。新增的承接逻辑是排练提示，不需要朗读。

## 排练要求

- 在 1:45、3:30、5:15 换人，7:00 结束。
- 按讲稿指图，不逐个朗读参数表和长链接。
- 第 12 页停留，进入 3 分钟提问。
- 四个人都掌握整体路线；遇到技术细节时由负责该部分的成员补充。

## 逐页复习与问答依据

### 第 1 页：A simple game of Chess

简短开场，不解释所有文件名。

We recovered information from supplied files and embedded links. We did not manufacture a physical chess set.

### 第 2 页：The clue paths

沿图从左往右指，说明各分支独立；马的原始模型是在后续文件中恢复的。

The board has three clue routes. The rook and king supply two more. The Knight G-code then supplies a recovery link, giving six groups of recovered information.

### 第 3 页：Inspecting the hidden geometry

强调 129 是实例数，包含重复件和刻字小实体；人工转录与程序计算各自负责什么。

OpenCascade imports the source units as millimeters and applies placements. The scripts are specific to this assembly. They do not claim general OCR.

### 第 4 页：The QR pattern identifies AlF357

先指原始间隙，再指恢复后的二维码，最后指材料结果。参数表供评委看，不逐项朗读。

The QR lies at Y=3.175 mm, with 14.2875 mm module pitch. The alloy is a beryllium-free A357 derivative, AlSi7Mg0.6. The sheet gives 20-90 micrometer powder, part density 2.67 g/cm3, nitrogen, 30 micrometer layers and 5.8 mm3/s on M 290, and 60 micrometer layers and 17 mm3/s on M 400. Heat treatment: 30 minutes at 540 +/- 6 C, immediate room-temperature water quench, then 6 hours at 165 +/- 6 C and air cooling; start aging within 40 hours. These are manufacturer specifications, not measurements from our parts.

### 第 5 页：The rank labels fix the reading order

指向第一行，示范从左到右读取。不要把 rank 8 误说成图中最靠摄像机的一边。

Rank 8 lies at negative Z in the imported frame. Wrong rank order produced YPu63d0kpx with residual 1101. The correct occupancy has 37 ones and 27 zeros. Maximum axis offset from a nearest square center was about 5.21 mm, below half the 42.8625 mm grid pitch.

### 第 6 页：Six-bit groups reveal the Knight link

讲清六位数值是查表索引，索引从零开始。指向完整结果，不逐字拼读后缀。

The result is the case-sensitive Hack3d26-2. The alphabet is ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_. Ten complete groups use 60 bits. Four trailing zeros remain unexplained; the clue did not authorize appending two more zeros, which would add A. The live destination agreed with the Knight clue.

### 第 7 页：The bottom grid gives the target heights

只示范 King 的 8+1=9，其他高度让观众看表。

Target heights in mm: King 90, Queen 80, Rook 50, Bishop 70, Knight 60, Pawn 50. Face levels are Y=-1.905 mm and -3.175 mm. Inverse polarity gives 246, 247, 250, 248, 249, 250 cm. Source note: Final sizes may not be reflected in prototype parts. Uniform scaling would also change hardware fits, so we preserved the source geometry.

### 第 8 页：The rook inscription unlocks the Pawn ZIP

用 Zkdw 变成 What 的示例讲位移，强调 Queen 的 Q 要大写。

Cipher: Zkdw lv wkh ehvw slhfh iru d sdzq wr wxuq lq wr? Shift -3 gives What is the best piece for a pawn to turn in to? Earlier guesses 985765, Hack3d26, Hack3d26-2, and AlF357 failed. CRCs and byte comparisons verify both extracted members. We used the archive's accepted password rather than asserting Queen is the best promotion in every chess position.

### 第 9 页：The recovered files describe a mechanism

区分零件标签和实际数量。表格是额外五金，不能加进 31 个主体件的核对中。

The drawing credits Works by Design. Q1 and Q3 each appear twice; Q6 and Q13 each appear five times; the remaining 17 labels appear once. Thus 2+2+5+5+17=31. Hardware: two N52 magnets 1/4 x 3/16 inch, two 0.3 x 3 x 5 mm springs, one 0.6 x 8 x 50 mm spring, five 1.5 x 6 mm pins, and two 1.5 x 18 mm pins. Magnet dimensions convert to 6.35 x 4.7625 mm. The spring dimension convention is not specified.

### 第 10 页：The King file contains filament commands

不要把正常结束等同于完整打印验证，也不要把这份 G-code 称为已验证的金属打印文件。

File ID: 1Kk8K4bplqJWDCqiRtARlxXEeBVDJ-CKM. The first transcription returned 404. Both header and observed maximum Z are 67.15 mm. Marked layers are 0-335. End commands include M104 S0, M140 S0, M107, M84. Saved settings: Prusa i3 MK2, Cura, 0.2 mm layers, 215 C extruder, 80 C bed, 10% infill, five top and bottom layers, tree supports, brim, estimated 7105 seconds and 4.34366 m filament.

### 第 11 页：The Knight file leads to the original model

按左侧检查、中央恢复提示、右侧 STEP 的顺序指图。不要声称已经重新生成或打印了替代路径。

Knight marked sections 0-77 are contiguous. Header MAXZ=34.95 mm; maximum observed motion Z=15.75 mm. It lacks M104 S0 and M140 S0. It retains an End of Gcode comment. Lines 353917-353918 contain the un-commented recovery note and original-model link. Knight STEP has 61 placed instances from 24 manifold solid definitions. Original model ID: 1b94MhZaxK8I5xzezqY1e8n1fdASWHZjL. We did not infer truncation by comparing G-code Z with the final 60 mm height.

### 第 12 页：Recovered information and verification

7:00 结束，在这一页停留，进入三分钟提问。

We verified eight original and recovered file hashes, three fresh STEP imports with counts 129/31/61, two encrypted ZIP member CRCs, both short-link destinations, and the geometric decodes. Remaining limits include four unused board bits, the King's one-layer mismatch and metal wording, and untested physical printing, fit, motion, and final-size adjustments.
