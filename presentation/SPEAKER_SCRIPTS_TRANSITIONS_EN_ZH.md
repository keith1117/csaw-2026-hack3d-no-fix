# No Fix 演讲稿：页间衔接版

共 12 页。正式演讲 7 分钟，之后 3 分钟提问。A、B、C、D 各 105 秒。中英文是同一讲稿的两种语言版本，现场选择一种。下方“承接逻辑”和“指图提示”用于排练，不计入朗读稿。

原版 `notes.json` 和 `SPEAKER_SCRIPTS_EN_ZH.md` 保留。此版对应 `output/No_Fix_7_Minute_Transitions.pptx` 的 speaker notes。

## 成员 A：第 1-3 页，共 105 秒

### 第 1 页：A simple game of Chess

0:00-0:15，约 15 秒。

**English**

Hi everyone, we're No Fix. We explored a chess assembly to recover hidden manufacturing information. We'll show how the clues connected to the files and specifications we recovered.

**中文**

大家好，我们是 No Fix。这个挑战需要我们从一份国际象棋装配模型里，找回隐藏的制造信息。我们会从拿到的文件讲起，说明每条线索怎样带我们找到最后的结果。

承接逻辑（不朗读）：从任务进入起点：要说明怎么恢复信息，先交代手里有什么文件。

指图提示（不朗读）：开场后直接翻到文件和线索图，让观众先知道任务是什么。

### 第 2 页：The clue paths

0:15-0:50，约 35 秒。

**English**

We started with three files: the STEP assembly, the problem statement, and a locked Pawn ZIP. This map shows separate clue paths. The board covered material, heights, and the Knight link. The rook unlocked the Pawn files, while the king had its own link. To follow these paths, we first had to inspect the hidden geometry.

**中文**

我们一开始拿到三个文件：STEP 装配模型、题目说明，还有一个加密的兵零件压缩包。图里是几条独立的线索：棋盘提供材料、尺寸和马的文件链接，车提供压缩包密码，王内部还有自己的链接。要跟进这些线索，我们首先得看清模型里面藏了什么。

承接逻辑（不朗读）：这张图是线索关系图。几条分支各有来源，共同的第一步是检查 STEP 内部。

指图提示（不朗读）：沿图说明几条路线各自解决什么问题。最后一句引向下一页的内部几何检查。

### 第 3 页：Inspecting the hidden geometry

0:50-1:45，约 55 秒。

**English**

A text search only found part names, so we opened the assembly. We counted 129 solid instances, including 37 pawns. We separated bodies and exported internal faces, like these king cutaways. We read small inscriptions by eye and used scripts for sampling and decoding. Inside the board, we found both a QR pattern and written directions, including 'Every square has a value.' We'll start with the QR.

**中文**

我们先搜索 STEP 文本，但只找到了零件名，于是转去检查几何模型。整个装配有 129 个实体实例，其中包括 37 个兵。我们分离遮挡的实体、导出内部平面，左边就是王的剖视图。细小刻字由我们放大后人工读取，脚本负责采样和解码。棋盘内部既有二维码，也有文字提示，其中一句是‘每个格子都有数值’。下面先看二维码这条线索。

承接逻辑（不朗读）：文本搜索不足，所以检查内部几何。这里先介绍发现的两条棋盘线索，为第 4 页的 QR 和第 5 页的文字提示同时铺垫。

指图提示（不朗读）：指剖视图解释为什么外观检查不够。提到二维码和文字两种发现，随后交给 B 讲二维码。

## 成员 B：第 4-6 页，共 105 秒

### 第 4 页：The QR pattern identifies AlF357

1:45-2:20，约 35 秒。

**English**

That QR wouldn't scan because the physical squares had gaps. We sampled the centers of the 25-by-25 grid, filled the modules, and added a white border. The restored code linked to the official AlF357 material sheet and its process settings. With the material identified, we returned to the board's written directions.

**中文**

刚才提到的二维码，一开始扫不出来，因为模型的小方块之间有间隙。我们按二十五乘二十五的网格读取每个模块的中心，填满对应方格，再补上白色边框。恢复后的二维码指向官方 AlF357 材料说明书，里面也有制造参数。材料这条线索解决后，我们回到棋盘上的文字提示。

承接逻辑（不朗读）：第 3 页发现 QR，第 4 页解决其扫描问题并取得材料。材料文件与兵位解码属于不同分支，第 5 页回到棋盘原有文字提示。

指图提示（不朗读）：指原始图案的间隙、恢复后的 QR，再指材料信息。最后一句明确返回另一条棋盘线索。

### 第 5 页：The rank labels fix the reading order

2:20-2:50，约 30 秒。

**English**

Following the board instructions, we read occupied squares as one and empty squares as zero. The engraved rank labels corrected our first row order. We read rank eight first, then A to H across each row, producing 64 bits. We still needed a way to turn those bits into characters.

**中文**

按照棋盘上的文字提示，我们把有兵的格子记为一，空格记为零。第一次的行顺序读反了，所以我们核对了刻在边缘的行号，确认从第八横排开始，每一行从 A 读到 H。这样得到六十四位数据。接下来还需要知道，怎么把这些位数变成文字。

承接逻辑（不朗读）：从文字提示得到二进制规则，再用刻字行号纠正方向。现在只有 64 位数据，还缺少位数到字符的转换规则。

指图提示（不朗读）：首句承接棋盘文字。指第八横排，示范 A 到 H 的方向，末句引出下一页的六位查表。

### 第 6 页：Six-bit groups reveal the Knight link

2:50-3:30，约 40 秒。

**English**

The instructions also said 'six at a time.' We used the board's 64-character alphabet to map each six-bit value to a character, counting from zero. Seven selects H. Ten groups gave this suffix. We recorded the four leftover zeros. The link opened the Knight G-code. We saved it for checking and returned to the board's height diagram.

**中文**

同一段文字还说，每六位一组。棋盘上另有一个六十四字符的字母表，我们把每组六位转成数值，再从零开始查表。例如七对应 H。十组数据就得到屏幕上的链接后缀，剩下的四个零则单独记录。打开链接后，我们拿到了马的 G-code，先保存下来等待检查，再继续看棋盘上的高度图。

承接逻辑（不朗读）：第 5 页得到位串，第 6 页用同一文字提示的六位规则和独立刻字字母表完成解码。随后转向棋盘的另一条高度线索。

指图提示（不朗读）：用第一组示范查表，不逐字拼读后缀。说清马的文件已经下载，文件检查留到第 11 页；随后交给 C。

## 成员 C：第 7-9 页，共 105 秒

### 第 7 页：The bottom grid gives the target heights

3:30-4:00，约 30 秒。

**English**

On the board's underside, six labeled binary rows gave the target heights. We read shallow squares as one and deep squares as zero. The ruler gave centimeters: nine for the King meant 90 millimeters. A nearby note says the prototype sizes may differ. But the Pawn ZIP was still locked.

**中文**

棋盘底部有六行带棋子标签的二进制方格，对应六种棋子的目标高度。我们把浅格记为一、深格记为零，旁边尺子的单位是厘米。例如王这一行得到九，也就是九厘米，换算成九十毫米。附近还提醒，原型尺寸可能与最终尺寸不同。到这里，我们有了高度，但兵的压缩包仍然没有打开。

承接逻辑（不朗读）：接续第 6 页预告的高度图，使用底部独立的二进制行和 cm 尺子。高度结果没有直接解锁 ZIP，因此引向密码问题。

指图提示（不朗读）：只示范 King 的 8+1=9 和单位转换。结尾把观众带回尚未解决的 ZIP 密码。

### 第 8 页：The rook inscription unlocks the Pawn ZIP

4:00-4:40，约 40 秒。

**English**

We tried the height values and earlier link strings as passwords, but none worked. The rook inscription gave us a better lead. Shifting its letters back three places revealed a Pawn-promotion question. We tried Queen with a capital Q. Both files extracted and passed CRC checks, so we could now inspect their contents.

**中文**

我们试过把高度数字和前面得到的链接文字当作密码，但都失败了。车内部的刻字给了我们新的方向。把每个字母向前移三位后，密文变成了一道关于兵升变的问题。我们尝试首字母大写的 Queen，两个文件都成功解出，并通过了 CRC 校验。这样，我们就能进一步检查压缩包里的内容。

承接逻辑（不朗读）：第 7 页留下 ZIP 未解锁的问题。本页先说明已有结果作密码为何失败，再用车内独立线索提出候选，以实际解压验证。

指图提示（不朗读）：用 Zkdw 变成 What 示范移位。Queen 的 Q 大写；解压和 CRC 通过之后才确认密码。

### 第 9 页：The recovered files describe a mechanism

4:40-5:15，约 35 秒。

**English**

Opening the ZIP gave us a STEP model and this Queen-Pawn drawing. We counted 31 solid instances. The drawing's 21 labels include repeats, which also total 31 body pieces. It specifies the magnets, springs, and pins. We recovered the assembly information, while fit and motion remain untested. Next, we'll follow the King's separate file link.

**中文**

打开压缩包后，我们拿到一个 STEP 模型，还有这张 Queen-Pawn 爆炸装配图。模型里有三十一个实体实例。图纸虽然只有二十一个标签，但把重复数量算进去，也正好是三十一个主体零件。图纸还给出了磁铁、弹簧和销钉的信息。我们因此恢复了装配资料，实际配合和运动还没有测试。接下来由第四位成员跟进王内部的另一条文件链接。

承接逻辑（不朗读）：ZIP 解锁后，才有条件检查内部 CAD 和图纸。完成 Pawn 分支后，转到独立的 King 分支，避免把 King 文件说成来自这个压缩包。

指图提示（不朗读）：对照 21 个标签与 31 个主体件，硬件另算。交给 D 时明确 King 链接来自王本身。

## 成员 D：第 10-12 页，共 105 秒

### 第 10 页：The King file contains filament commands

5:15-5:50，约 35 秒。

**English**

The King's own inscription led to this G-code. We enlarged the lettering to correct the file ID. Its maximum Z matched the header, and it had heater-off commands. But we counted 336 sections against 337 declared. The inscription said metal, while the file used filament commands. We then checked the other G-code the same way.

**中文**

王自己的内部刻字指向了这份 G-code。我们放大文字，修正了最初读错的文件 ID。文件的最高运动 Z 与头部一致，也有关闭加热器的指令。不过，头部声明三百三十七层，我们实际只找到三百三十六个编号层段。另外，刻字提到金属，文件用的却是耗材挤出指令。这些差异我们都保留了。随后，我们用同样的检查方法查看另一份 G-code。

承接逻辑（不朗读）：明确 King 文件来自王的刻字。下一页通过相同的层数、Z 和结束指令检查衔接，同时需要重申 Knight 来自第 6 页的兵位链接。

指图提示（不朗读）：顺着表格比较头部与实际指令。最后一句引向共同的检查方法；下一页首句补明 Knight 文件的来源。

### 第 11 页：The Knight file leads to the original model

5:50-6:35，约 45 秒。

**English**

That Knight G-code came from the Pawn-position link. It declared 177 layers, but contained only 78 and stopped below its stated maximum Z. It also lacked heater-off commands, despite its end comment. The file's recovery note pointed to the original model. Following it gave us 61 solid instances. We kept the partial G-code and recovered STEP together. With that model recovered, we could review all the results together.

**中文**

另一份就是前面通过兵的位置解码得到的马的 G-code。它声明一百七十七层，实际只有七十八个编号层段，最高运动 Z 也低于头部声明值。它虽然有结束注释，却没有关闭加热器的指令。文件里还有一条恢复提示，指向原始模型。我们跟进链接，打开了包含六十一个实体实例的 STEP 装配，并把它与不完整的原 G-code 一起保留。恢复模型后，我们就可以把各条线索的结果放在一起核对了。

承接逻辑（不朗读）：承接第 10 页的文件检查方法，回到第 6 页已下载的 Knight 文件。检查发现不完整，文件内恢复提示提供下一步，成功恢复 CAD 后进入总结。

指图提示（不朗读）：先提醒是第 6 页取得的文件，再指检查结果、恢复提示和 STEP。只恢复了模型，没有重新切片或实体打印。

### 第 12 页：Recovered information and verification

6:35-7:00，约 25 秒。

**English**

We recovered the material, target heights, Pawn assembly, and the King and Knight files. We checked the decodes, ZIP contents, CAD imports, and hashes. Physical printing and fit remain untested. Thank you. We're happy to take questions.

**中文**

最后，我们找回了材料说明、目标高度、兵的装配资料，以及王和马的文件。我们用解码结果、ZIP 校验、CAD 导入和文件哈希核对这些成果，文件中的矛盾也都如实记录。实体打印和配合还没有测试。谢谢各位，欢迎提问。

承接逻辑（不朗读）：从各分支的恢复过程回到整体任务，说明已经恢复什么、如何核对，以及实物测试的边界。

指图提示（不朗读）：停留在汇总页，7:00 结束正式演讲，进入三分钟提问。

