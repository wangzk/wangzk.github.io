---
title:  "在Linux中使用JACK提升音质：快速教程"
date:   2018-05-27 09:21:00 +0800
categories: linux 
---

## 为什么使用 JACK 而不是默认的音频驱动 ALSA？

根据Deepin论坛[《简单提升linux音效，实测有效》](https://bbs.deepin.org/forum.php?mod=viewthread&tid=137002)的帖子的说法，Deepin Linux使用的PulseAudio/ALSA声卡驱动效果并不好，只是能听个响，多环绕声等高级功能无法利用起来，导致收听效果没法和Win10/Mac比。而装上JACK之后，就能充分发挥声卡硬件本身的特性，提供高质量的音质。据发帖人说，音质有了质的飞跃。

之前帖子中对如何安装JACK描述的不详细，难以正确安装。而JACK相关资料又多是英文的，很繁琐，难以快速上手。

面对当前中文相关教程缺乏的现状，本博文提供了一个快速、简易的JACK安装教程，尤其是面向Deepin系统环境，希望能帮助更多的人更容易的享受到JACK[^1] 驱动的效果。

[^1]: 本教程安装的是目前比较成熟的Jack1版本的驱动。

## 安装 JACK

主要是需要安装两个和JACK相关的软件包：
1. qjackctl: JACK驱动的一个图形化配置程序。安装该软件包会自动安装JACK相关的驱动程序。
2. pulseaudio-module-jack：使JACK可以和Deepin采用的默认音频栈Pulseaudio联合工作的模块。该模块使Deepin无缝切换到JACK。

使用如下命令在**终端**中安装软件包（安装过程中需要进行命令行交互配置）：

```bash
sudo apt install qjackctl pulseaudio-module-jack
```

在安装的过程中遇到各种提示时都选择“Y”或”是“。

## 配置 JACK

### 配置用户组

需要将你的用户名添加到audio用户组。在终端中执行如下命令：

```bash
sudo usermod -a -G audio <你的用户名>
```

执行完后，需要注销当前桌面会话或重启系统（建议重启）以生效。

### 配置 QJackctl

配置完用户组之后，就可以启动JACK图形化配置程序qjackctl进行配置了（图标是一个插头）。

启动Qjackctl后可以见到如下的图形界面，我们需要点击其中的“Setup”按钮进行进一步配置。

![Qjackctl界面](/img/deepin-jack-install/qjackctl-ui.png)

在Setup界面，选择Options选项卡：

![Options选项卡](/img/deepin-jack-install/options.png)

在Scripting选项组下面勾选"Execute script after Startup"一项，并在后面的文本框中填入：

`pactl load-module module-jack-sink channels=2; pactl load-module module-jack- source channels=2;pacmd set -default-sink jack_out`

点击“OK”保存并关闭配置对话框。

## 启动 JACK

在QJackctl的主界面点击"Start"按钮，启动JACK音频模块。建议启动过程中播放音乐以便测试。

![Qjackctl界面](/img/deepin-jack-install/qjackctl-ui.png)

启动后会出现短暂的声音暂停（<5s)，然后就会切换到JACK工作模式:

![JACK工作状态](/img/deepin-jack-install/jack-working.png)

点击“Stop”就会暂停使用JACK驱动并切换回之前的ALSA工作模式。点击“Quit”可以彻底停止JACK驱动模块。

### 调节系统音量上限

第一次使用JACK时，可能会出现音量很小的情况。这时需要使用alsamixer程序调节系统的**最大音量**。

首先安装alsamixer程序：

```bash
sudo apt install alsa-utils
```

然后在终端中运行`alsamixer`命令。

在alsamixer程序的界面，首先按F6键选择声卡，选择除Default之外的那块实际物理声卡：

![alsamixer选择声卡界面](/img/deepin-jack-install/alsamixer-select-sound-card.png)

然后在新的界面中使用左右方向键移动到Master选项上，利用上下方向键调节Master的音量，该音量值设置的是系统**最大音量**（注意不要太大，否则容易爆音）：

![alsamixer调节最大音量](/img/deepin-jack-install/alsamixer-change-master-volumn.png)

配置好后，按Esc退出设置。


### 配置 JACK 开机自动启动

如果对JACK的音质感到满意，可以按如下步骤将JACK配置为开机自动启动。

1. 首先在QJackctl的主界面点击“Setup”打开配置界面；
2. 打开“Misc”选项卡，将图中画圈的选项都勾选，该选项保证启动QJackctl后会自动开启JACK驱动：
    ![JACK开机自动启动配置](/img/deepin-jack-install/configure-jack-autostart.png)
3. 点击“OK”保存配置并关闭。
4. 配置QJackctl程序为开机自动启动程序（在Deepin的启动器界面操作）：
    ![QJackctl开机自动启动](/img/deepin-jack-install/autostart-qjackctl.png)

每次开机后，QJackctl就会自动启动并缩小在托盘中运行，并且自动将音频驱动切换到JACK：

![QJackctl托盘](/img/deepin-jack-install/tray-icon.png)

完成配置之后，就可以关闭QJackctl的界面，使它在系统托盘中继续运行：

1. 关闭QJackctl窗口（不是Quit按钮），软件会提示JACK会在后台继续运行，此时点击“OK”：
    ![QJackctl退出提示](/img/deepin-jack-install/close-qjackctl.png)
2. QJackctl会被缩小到托盘在后台继续运行：
    ![QJackctl托盘](/img/deepin-jack-install/tray-icon.png)
3. 想彻底退出QJackctl，需要在QJackctl的主界面里点击Quit。

---

注：







