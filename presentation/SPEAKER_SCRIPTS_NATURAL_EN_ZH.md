# No Fix 演讲稿：自然口语版

对应 `output/No_Fix_7_Minute_Natural_Notes.pptx`。四位成员各 105 秒，共 7 分钟，之后 3 分钟提问。中英文现场选择一种。每页的 English 或中文段落是朗读正文；承接逻辑、指图提示和 Q&A 供排练与备答使用。原有讲稿和 PPT 保留。

## 成员 A：第 1-3 页，共 105 秒

### 第 1 页：A simple game of Chess

0:00-0:15，约 15 秒。

**English**

Hi everyone, we're No Fix. We recovered manufacturing information hidden inside a chess assembly, and today we'll explain how the clues led us to the files and specifications.

**中文**

大家好，我们是 No Fix。这次挑战需要我们从一份国际象棋装配模型里找回隐藏的制造信息，下面就从拿到的文件讲起，看看这些线索是怎么一步步带我们找到结果的。

承接逻辑（不朗读）：从任务进入起点：要说明怎么恢复信息，先交代手里有什么文件。

指图提示（不朗读）：开场后直接翻到文件和线索图，让观众先知道任务是什么。

### 第 2 页：The clue paths

0:15-0:50，约 35 秒。

**English**

Our starting point was three files: a STEP assembly, the problem statement, and a locked Pawn ZIP. As this map shows, the board led to material, heights, and the Knight file, while the rook supplied a password and the king had its own link. To follow those paths, though, we first needed to see the hidden geometry.

**中文**

一开始，我们手上有三个文件：STEP 装配模型、题目说明，还有一个加密的兵零件压缩包。大家可以顺着这张图看，棋盘上的线索分别指向材料、尺寸和马的文件，车里面藏着密码，王里面则有另一条链接。不过，要跟进这些线索，我们首先得看清模型内部。

承接逻辑（不朗读）：这张图是线索关系图。几条分支各有来源，共同的第一步是检查 STEP 内部。

指图提示（不朗读）：沿图说明几条路线各自解决什么问题。最后一句引向下一页的内部几何检查。

### 第 3 页：Inspecting the hidden geometry

0:50-1:45，约 55 秒。

**English**

The text search only gave us part names, so we inspected the geometry instead. There were 129 solid instances, including 37 pawns. To uncover the clues, we separated bodies and exported internal faces, like these king cutaways. Then we read the enlarged inscriptions by eye and used scripts for sampling and decoding. Inside the board, this revealed a QR pattern and written instructions, including 'Every square has a value.' Our next speaker will start with the QR.

**中文**

我们先搜索了 STEP 文本，但只找到零件名，所以接着检查了几何模型。整个装配有 129 个实体实例，其中包括 37 个兵。为了看到被挡住的线索，我们分离了实体，导出内部平面，左边这些王的剖视图就是例子。之后，细小刻字由我们放大后人工读取，采样和解码则交给脚本。这样一来，棋盘内部的二维码和文字提示就清楚了，其中一句是‘每个格子都有数值’。接下来由第二位成员先讲二维码。

承接逻辑（不朗读）：文本搜索不足，所以检查内部几何。这里先介绍发现的两条棋盘线索，为第 4 页的 QR 和第 5 页的文字提示同时铺垫。

指图提示（不朗读）：指剖视图解释为什么外观检查不够。提到二维码和文字两种发现，随后交给 B 讲二维码。

## 成员 B：第 4-6 页，共 105 秒

### 第 4 页：The QR pattern identifies AlF357

1:45-2:20，约 35 秒。

**English**

That QR wouldn't scan at first because the physical squares had gaps. So we sampled the 25-by-25 module centers, filled the cells, and added a white border. The restored code then opened the official AlF357 material sheet, including process settings. With that recorded, we returned to the board's written instructions.

**中文**

刚才提到的二维码，一开始其实扫不出来，因为模型的小方块之间有间隙。所以我们按二十五乘二十五的网格读取模块中心，再填满对应方格，并补上白色边框。处理完之后，二维码就指向了官方 AlF357 材料说明书，里面也列出了制造参数。把这些信息记下来后，我们又回到了棋盘上的文字提示。

承接逻辑（不朗读）：第 3 页发现 QR，第 4 页解决其扫描问题并取得材料。材料文件与兵位解码属于不同分支，第 5 页回到棋盘原有文字提示。

指图提示（不朗读）：指原始图案的间隙、恢复后的 QR，再指材料信息。最后一句明确返回另一条棋盘线索。

### 第 5 页：The rank labels fix the reading order

2:20-2:50，约 30 秒。

**English**

Following the board instructions, we treated occupied squares as one and empty squares as zero. Our first row order was wrong, though, so we checked the engraved rank labels. Those showed us to start at rank eight and read A to H across each row. That gave us 64 bits, which still needed decoding.

**中文**

按照棋盘上的文字提示，我们把有兵的格子记为一，空格记为零。不过，第一次的行顺序读反了，所以又回去核对了边缘的刻字行号。这才确认，要从第八横排开始，每行从 A 读到 H。这样就得到六十四位数据，下一步还要把它们转成文字。

承接逻辑（不朗读）：从文字提示得到二进制规则，再用刻字行号纠正方向。现在只有 64 位数据，还缺少位数到字符的转换规则。

指图提示（不朗读）：首句承接棋盘文字。指第八横排，示范 A 到 H 的方向，末句引出下一页的六位查表。

### 第 6 页：Six-bit groups reveal the Knight link

2:50-3:30，约 40 秒。

**English**

The same instructions also said 'six at a time,' and the board supplied a 64-character alphabet. So we used each six-bit value as an index, starting from zero. Seven, for example, selects H. Ten groups gave us this suffix, and we recorded the four leftover zeros. The link then opened the Knight G-code, so we saved it and returned to the board's height diagram.

**中文**

同一段提示里还说，每六位一组，而且棋盘上另有一个六十四字符的字母表。所以，我们就把每组六位转成数值，再从零开始查表，比如七对应的就是 H。十组数据合起来，得到屏幕上的链接后缀，剩下的四个零则单独记录。打开链接后，马的 G-code 就找到了。我们先保存这份文件，接下来再看棋盘上的高度图。

承接逻辑（不朗读）：第 5 页得到位串，第 6 页用同一文字提示的六位规则和独立刻字字母表完成解码。随后转向棋盘的另一条高度线索。

指图提示（不朗读）：用第一组示范查表，不逐字拼读后缀。说清马的文件已经下载，文件检查留到第 11 页；随后交给 C。

## 成员 C：第 7-9 页，共 105 秒

### 第 7 页：The bottom grid gives the target heights

3:30-4:00，约 30 秒。

**English**

On the board's underside, six labeled rows gave us the heights, using shallow squares as one and deep squares as zero. Since the ruler was in centimeters, nine for the King meant 90 millimeters. A nearby note warned that prototype sizes could differ. But even with those values, the Pawn ZIP was still locked.

**中文**

高度图就在棋盘底部，六行分别标着不同的棋子。把浅格记为一、深格记为零，就能算出对应数值。再看旁边的尺子，单位是厘米，所以王这一行的九，就代表九厘米，也就是九十毫米。不过，附近的说明提醒，原型尺寸可能和最终尺寸不同。到这里，高度是有了，但兵的压缩包还没有打开。

承接逻辑（不朗读）：接续第 6 页预告的高度图，使用底部独立的二进制行和 cm 尺子。高度结果没有直接解锁 ZIP，因此引向密码问题。

指图提示（不朗读）：只示范 King 的 8+1=9 和单位转换。结尾把观众带回尚未解决的 ZIP 密码。

### 第 8 页：The rook inscription unlocks the Pawn ZIP

4:00-4:40，约 40 秒。

**English**

So we tried those heights and the earlier link strings as passwords, but none worked. That led us to an inscription inside the rook. Shifting its letters back three places gave us a Pawn-promotion question, so we tried Queen, with a capital Q. This time, both files extracted and passed CRC checks, which meant we could inspect the contents.

**中文**

所以，我们试着把这些高度和前面得到的链接文字当作密码，结果都不对。于是就转去检查车的内部，找到了这行刻字。把字母逐个向前移三位后，就得到一道关于兵升变的问题。顺着这个提示，我们尝试了首字母大写的 Queen。这次，两个文件都成功解出，也通过了 CRC 校验，接着就可以检查里面的内容了。

承接逻辑（不朗读）：第 7 页留下 ZIP 未解锁的问题。本页先说明已有结果作密码为何失败，再用车内独立线索提出候选，以实际解压验证。

指图提示（不朗读）：用 Zkdw 变成 What 示范移位。Queen 的 Q 大写；解压和 CRC 通过之后才确认密码。

### 第 9 页：The recovered files describe a mechanism

4:40-5:15，约 35 秒。

**English**

Inside were a STEP model and this Queen-Pawn drawing. Although the drawing used 21 labels, its repeated quantities totaled 31 body pieces, matching the model. It also listed the magnets, springs, and pins. So we recovered the assembly information, though fit and motion still need testing. Our next speaker will follow the King's separate link.

**中文**

压缩包里是一个 STEP 模型，还有这张 Queen-Pawn 爆炸装配图。图上虽然只有二十一个标签，但把重复数量算进去，正好是三十一个主体零件，和模型的实体数一致。另外，图纸也列出了磁铁、弹簧和销钉的信息。这样，装配资料就找回来了，不过实际配合和运动还需要测试。接下来由第四位成员跟进王内部的另一条链接。

承接逻辑（不朗读）：ZIP 解锁后，才有条件检查内部 CAD 和图纸。完成 Pawn 分支后，转到独立的 King 分支，避免把 King 文件说成来自这个压缩包。

指图提示（不朗读）：对照 21 个标签与 31 个主体件，硬件另算。交给 D 时明确 King 链接来自王本身。

## 成员 D：第 10-12 页，共 105 秒

### 第 10 页：The King file contains filament commands

5:15-5:50，约 35 秒。

**English**

Enlarging the King's inscription helped us correct its file link and download this G-code. Its maximum Z matched the header, and it included heater-off commands. But it had one fewer layer section than declared, and the file used filament commands even though the inscription mentioned metal production. So we recorded both issues and applied the same checks to the Knight file.

**中文**

王内部也有一条文件链接，我们把刻字放大后，才修正了最初读错的 ID，下载到这份 G-code。检查下来，最高运动 Z 和头部一致，也有关闭加热器的指令。不过，实际编号层段比声明少了一层，而且文件用的是耗材挤出指令，和刻字里提到的金属生产对不上。所以，这两处差异都如实记录下来，之后再用同样的方法检查马的文件。

承接逻辑（不朗读）：明确 King 文件来自王的刻字。下一页通过相同的层数、Z 和结束指令检查衔接，同时需要重申 Knight 来自第 6 页的兵位链接。

指图提示（不朗读）：顺着表格比较头部与实际指令。最后一句引向共同的检查方法；下一页首句补明 Knight 文件的来源。

### 第 11 页：The Knight file leads to the original model

5:50-6:35，约 45 秒。

**English**

The Knight file came from that earlier Pawn-position link. It contained only 78 of its declared 177 layers and stopped below the header's maximum Z. And although it had an end comment, there were no heater-off commands. Its recovery note, though, linked to the original model. That gave us a STEP assembly with 61 solid instances, which we kept alongside the partial G-code. With both saved, we could review the results together.

**中文**

马的文件，就是前面从兵的位置解码得到的那一份。它声明有一百七十七层，实际却只有七十八个编号层段，而且最高运动 Z 也没达到头部声明值。另外，虽然有结束注释，却没有关闭加热器的指令。不过，文件里还留了一条恢复提示，链接指向原始模型。顺着它，我们成功打开了一个包含六十一个实体实例的 STEP 装配，所以把它和不完整的原 G-code 一起保留了下来。有了这些文件，最后就可以把所有结果放在一起核对了。

承接逻辑（不朗读）：承接第 10 页的文件检查方法，回到第 6 页已下载的 Knight 文件。检查发现不完整，文件内恢复提示提供下一步，成功恢复 CAD 后进入总结。

指图提示（不朗读）：先提醒是第 6 页取得的文件，再指检查结果、恢复提示和 STEP。只恢复了模型，没有重新切片或实体打印。

### 第 12 页：Recovered information and verification

6:35-7:00，约 25 秒。

**English**

So those clues gave us the material, target heights, Pawn assembly, and King and Knight files. The decodes, ZIP checks, CAD imports, and hashes supported those results, while physical printing and fit remain untested. Thank you, and we're happy to take questions.

**中文**

顺着这些线索，我们最后找回了材料说明、目标高度、兵的装配资料，以及王和马的文件。解码结果、ZIP 校验、CAD 导入和文件哈希也都支持这些结果，不过实体打印和配合还没有测试。谢谢各位，接下来欢迎提问。

承接逻辑（不朗读）：从各分支的恢复过程回到整体任务，说明已经恢复什么、如何核对，以及实物测试的边界。

指图提示（不朗读）：停留在汇总页，7:00 结束正式演讲，进入三分钟提问。

