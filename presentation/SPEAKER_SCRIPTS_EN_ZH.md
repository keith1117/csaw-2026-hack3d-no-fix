# No Fix 四人中英文演讲稿

12 页 PPT，7 分钟演讲，3 分钟评委提问。四人各 1 分 45 秒，包含翻页、指图和交接。中英文是同一套内容的两个版本，现场选择一种语言。

## 成员 A：第 1-3 页，0:00-1:45

### 第 1 页，0:00-0:15（15 秒）

**English**

Hi, we are No Fix. We investigated a chess assembly to recover hidden manufacturing information. We will explain our approach, the problems we encountered, and how we checked our results.

**中文**

大家好，我们是 No Fix。我们检查了一份国际象棋装配模型，寻找里面隐藏的制造信息。下面会介绍解题方法、遇到的问题，以及我们如何验证结果。

指图提示（不朗读）：简短开场，不解释所有文件名。

### 第 2 页，0:15-0:50（35 秒）

**English**

We started with a STEP assembly, a problem statement, and an encrypted Pawn ZIP. The clues formed separate branches. Board patterns led to the material, dimensions, and Knight file. The rook supplied a ZIP password, and the king contained another file link. We checked each branch against its own source.

**中文**

我们拿到三个文件：STEP 装配、题目说明和加密的兵零件压缩包。线索分成几条独立分支：棋盘中的图案分别对应材料、尺寸和马的文件，车内刻字提供压缩包密码，王内部则藏着另一个文件链接。我们对每条分支分别验证，最后再汇总成制造信息。

指图提示（不朗读）：沿图从左往右指，说明各分支独立；马的原始模型是在后续文件中恢复的。

### 第 3 页，0:50-1:45（55 秒）

**English**

Our first text search found part names, but no plaintext answer. We then imported the STEP and inspected 129 solid instances, including 37 pawns. Outer surfaces hid several clues. We separated bodies and exported internal faces, as this king cutaway shows. We read enlarged lettering by eye and used scripts for grid sampling and decoding. We checked links, archive contents, and CAD imports to confirm the results. Our next speaker will explain the board clues.

**中文**

首先我们搜索 STEP 文本，只找到零件名称，没有找到明文答案。于是我们导入模型，检查了 129 个实体实例，其中有 37 个兵。一些外壳挡住了线索，我们便分离实体、导出内部平面，左侧王的剖视图就是例子。几何刻字先放大，再由我们人工转录；脚本负责采样和解码。最后，我们用链接实际指向、压缩包校验和 CAD 导入结果来确认判断。接下来由第二位成员介绍棋盘线索。

指图提示（不朗读）：强调 129 是实例数，包含重复件和刻字小实体；人工转录与程序计算各自负责什么。

## 成员 B：第 4-6 页，1:45-3:30

### 第 4 页，1:45-2:20（35 秒）

**English**

The QR pattern inside the board did not scan because gaps separated the physical squares. We sampled the twenty-five by twenty-five module centers, filled the cells, and added a white border. The restored code led to the official AlF357 material sheet, including machine parameters and heat treatment.

**中文**

棋盘内部的二维码一开始无法扫描，因为实体小方块之间留有间隙。我们按二十五乘二十五的网格采样每个模块的中心，再填满模块，并加上白色边框。恢复后的二维码指向官方 AlF357 材料说明书。我们由此取得合金信息，并记录对应机器的参数和热处理过程。

指图提示（不朗读）：先指原始间隙，再指恢复后的二维码，最后指材料结果。参数表供评委看，不逐项朗读。

### 第 5 页，2:20-2:50（30 秒）

**English**

We read the Pawn positions as binary: occupied means one, empty means zero. The first row order gave the wrong result. We checked the engraved rank labels, then read rank eight first and A through H across each row. All thirty-seven pawns mapped to different squares.

**中文**

我们把兵的位置转成二进制：有兵记作一，空格记作零。第一次采用的行顺序得到错误结果。于是我们回到模型，核对刻在边缘的行号，确认从第八横排开始，每行按 A 到 H 读取。三十七个兵分别对应不同格子，最终得到六十四位数据。

指图提示（不朗读）：指向第一行，示范从左到右读取。不要把 rank 8 误说成图中最靠摄像机的一边。

### 第 6 页，2:50-3:30（40 秒）

**English**

The inscription said six at a time, and the board supplied a sixty-four-character alphabet. We divided the bits into six-bit groups and counted the alphabet positions from zero. The first group equals seven and selects H. Ten groups gave the suffix shown here. Four zero bits remained, which we recorded separately. The working link opened the Knight G-code. Our next speaker will explain the dimensions and Pawn files.

**中文**

刻字提示每六位一组，旁边还给出了包含六十四个字符的字母表。我们将数据分成六位一组，转成数值，再从零开始查字母表。例如第一组等于七，对应字母 H。十组数据得到屏幕上的链接后缀，还剩四个零，我们将它们单独记录，没有补造新位数。链接成功打开马的 G-code。接下来介绍尺寸和兵的文件。

指图提示（不朗读）：讲清六位数值是查表索引，索引从零开始。指向完整结果，不逐字拼读后缀。

## 成员 C：第 7-9 页，3:30-5:15

### 第 7 页，3:30-4:00（30 秒）

**English**

The bottom of the board had six labeled binary rows. We read shallow squares as one and deep squares as zero. The ruler supplied centimeters. The King's row gives nine centimeters, or ninety millimeters. A nearby note says the prototype geometry may differ from the final sizes.

**中文**

棋盘底部有六行带棋子标签的二进制方格。我们把浅格读作一、深格读作零，再按行转换成数值。旁边标有厘米的尺子给出了单位。例如王这一行得到九厘米，也就是九十毫米。附近的说明还提醒，原型零件可能不反映最终尺寸，因此我们把目标高度与原始 CAD 尺寸分开记录。

指图提示（不朗读）：只示范 King 的 8+1=9，其他高度让观众看表。

### 第 8 页，4:00-4:40（40 秒）

**English**

For the Pawn ZIP, guesses based on dimensions and earlier links failed. Inside the rook, we found a coded sentence. Shifting each letter back three places revealed a question about Pawn promotion. We tried Queen, with a capital Q. Both files extracted and passed their CRC checks, confirming the exact password.

**中文**

兵的压缩包需要密码。我们先尝试尺寸数字和前面得到的链接文字，都失败了。后来在车的内部找到一句密文，把字母逐个向前移三位，就得到一个关于兵升变的问题。我们尝试首字母大写的 Queen。压缩包中的两个文件都成功解出，并通过 CRC 校验，因此确认了这个精确密码。

指图提示（不朗读）：用 Zkdw 变成 What 的示例讲位移，强调 Queen 的 Q 要大写。

### 第 9 页，4:40-5:15（35 秒）

**English**

The archive contained a STEP model and an exploded Queen-Pawn drawing. We imported thirty-one solid instances. The drawing's twenty-one labels include repeated quantities that also total thirty-one body pieces. It also specifies the magnets, springs, and pins shown here. We recovered the parts and arrangement, while physical fit and motion remain untested. Our next speaker will discuss the manufacturing files.

**中文**

压缩包里包含 STEP 模型和一张 Queen-Pawn 爆炸装配图。我们导入了三十一个实体实例。图纸虽然只有二十一个零件标签，但把重复数量计算进去，同样得到三十一个主体零件。图纸还列出了磁铁、弹簧和销钉的规格与数量。这样我们恢复了零件组成和装配位置，实际配合与运动仍需要实物测试。接下来由第四位成员介绍制造文件。

指图提示（不朗读）：区分零件标签和实际数量。表格是额外五金，不能加进 31 个主体件的核对中。

## 成员 D：第 10-12 页，5:15-7:00

### 第 10 页，5:15-5:50（35 秒）

**English**

The king's internal inscription linked to this G-code. An enlarged view helped us correct an ambiguous file ID. The file reaches its stated maximum Z and has heater-off commands, but we found 336 numbered sections against 337 declared. We recorded that mismatch. The inscription mentions metal, while the linked file contains filament commands.

**中文**

王内部的刻字指向这份 G-code。最初有几个文件 ID 字符难以辨认，我们通过放大视图修正了链接。文件中的最高运动 Z 与头部一致，也有关闭加热器的指令。不过我们只找到三百三十六个编号层段，头部则声明三百三十七。我们保留了这个差异。另外，刻字提到金属生产，实际文件却包含耗材挤出指令，这个矛盾也如实记录。

指图提示（不朗读）：不要把正常结束等同于完整打印验证，也不要把这份 G-code 称为已验证的金属打印文件。

### 第 11 页，5:50-6:35（45 秒）

**English**

The Knight file declared 177 layers, but contained only 78, and its motion stopped below the header's maximum Z. It also lacked shutdown commands, despite an ending comment. A recovery note linked to the original model. We followed it and opened 61 solid instances. We preserved the partial G-code beside the recovered STEP. Adding an ending alone would not recover the missing upper layers.

**中文**

马的 G-code 声明了一百七十七层，实际只有七十八个编号层段，最高运动 Z 也低于头部声明值。虽然保留了结束注释，却缺少关闭加热器的指令。我们在末尾找到恢复提示和原始模型链接，跟进后成功打开了包含六十一个实体实例的 STEP 装配。我们同时保留不完整的 G-code 和恢复后的模型。只补一个结束段，无法重建丢失的上层路径；原始模型才是重新切片的依据。

指图提示（不朗读）：按左侧检查、中央恢复提示、右侧 STEP 的顺序指图。不要声称已经重新生成或打印了替代路径。

### 第 12 页，6:35-7:00（25 秒）

**English**

We recovered the material, target heights, Pawn assembly, and King and Knight files. We verified the decodes, ZIP contents, CAD imports, and source hashes. Manufacturing and fit remain untested. Thank you. We welcome your questions.

**中文**

最后，我们恢复了材料说明、目标高度、兵的装配资料，以及王和马的文件。我们通过解码结果、ZIP 校验、CAD 导入和源文件哈希来核对这些结果。剩余位数和文件矛盾也都有记录，实际制造与配合仍未测试。谢谢各位，欢迎提问。

指图提示（不朗读）：7:00 结束，在这一页停留，进入三分钟提问。
