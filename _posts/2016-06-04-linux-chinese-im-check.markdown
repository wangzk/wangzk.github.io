---
layout: post
title:  "Linux下中文输入法出现问题的排查步骤"
date:   2016-06-04 18:55:29 +0800
categories: linux
---
使用中文Linux时，一个比较头疼的问题就是中文输入法的安装与配置。目前开发Linux发行版的大多是老外，他们不懂中文，很多人也不太清楚中文输入的问题。在中文化方面，中文的Linux发行版处理的都很好（比如Ubuntu Kylin和Deepin Linux）。但有时难免会用国外的发行版，这篇文章主要会介绍一下配置中文输入法时常见的问题和一些心得。

## 选对输入法框架
在Linux桌面下，输入法软件分为输入法框架和输入法引擎两部分。**输入法框架**是负责和操作系统以及应用程序打交道的。我们常见的fcitx和ibus都是输入法框架。而**输入法引擎**则负责把用户输入的英文字符（比如“woaikaiyuanzhongguo”）转变为中文字符（比如“我爱开源中国”）。Linux下比较著名的输入法引擎有libpinyin,rime,sougou等。常见的输入法软件包名字fcitx-libpinyin,fcitx-rime,ibus-rime等一般都是以"输入法框架-输入法引擎"来命名的。 

很多不能正确输入的问题，都与输入法框架配置不正确有关系。因此选对一个输入法框架很重要！

在这里推荐使用fcitx输入法框架。原因有如下几点：

* fcitx目前的主力开发者csslayer是中国人，对于中文输入需求更了解。
* fcitx强大的插件框架，使拼音输入法支持云拼音输入，大大提高了整句输入的正确率和效果。ibus因为架构受限，至今没有云拼音的成熟实现。
* fcitx框架支持搜狗。
* fcitx框架具有更加良好的配置诊断工具fcitx-diagnose，大大减轻排查困难度。

## 排查问题

下面假设你使用的是fcitx输入法框架，而且按照相关指示进行了配置（主要是配置环境变量）。如果不知道怎么配置中文输入法，可以参考[Ubuntu的Wiki](http://wiki.ubuntu.org.cn/Fcitx)，[Arch的Wiki](https://wiki.archlinux.org/index.php/Fcitx_%28%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%29)教程。Ubuntu和Debian系会在系统设置中提供有关设置，一般在哪里设置好即可，如果还不行，可以安装im-switch程序进行设置。

安装、配置好后，启动输入法。

如果出现了问题，无法输出，那么怎么办呢？在运行fcitx后（您可以开启一个终端，然后再里面运行命令“fcitx”，这样可以看到fcitx的输出信息），请按如下步骤操作。

1.　打开终端（这个应该懂的什么意思），在终端中执行命令“fcitx-diagnose”。下面的说明检查都是针对fcitx-diagnose程序的输出。

２. 检查locale配置部分，至少保证有zh_CN的locale可用，下面是我的输出：
    
    全部可用 locale:
            C
            en_US
            en_US.iso88591
            en_US.utf8
            POSIX
            zh_CN
            zh_CN.gb18030
            zh_CN.gb2312
            zh_CN.gbk
            zh_CN.utf8
            zh_HK
            zh_HK.big5hkscs
            zh_HK.utf8
            zh_TW
            zh_TW.big5
            zh_TW.utf8
            
3.检查**前端设置**，这一部分非常重要，需要仔细看里面的提示信息。一般出问题都在这里。本步骤检查主要是确保几个环境变量${GTK_IM_MODULE}、${QT_IM_MODULE}正确配置，以及Qt输入法模块文件、Gtk输入法模块文件均存在。如果有什么问题，工具会提示进行改进。


    # 前端设置:
    ## Xim:
    1.  `${XMODIFIERS}`:

        环境变量 XMODIFIERS 已经正确地设为了 "@im=fcitx".
        从环境变量中获取的 Xim 服务名称为 fcitx.

    2.  根窗口上的 XIM_SERVERS:

        Xim 服务的名称与环境变量中设置的相同.

    ## Qt:
    1.  `${QT_IM_MODULE}`:

        环境变量 QT_IM_MODULE 已经正确地设为了 "fcitx".

    2.  Qt 输入法模块文件:
        找到了 Qt4 的输入法模块: `/usr/lib/qt4/plugins/inputmethods/qtim-fcitx.so`.
        找到了 Qt5 的输入法模块: `/usr/lib/qt/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so`.
        找到了 fcitx 的 qt 模块: `/usr/lib/fcitx/qt/libfcitx-quickphrase-editor.so`.
        找到了 fcitx 的 qt 模块: `/usr/lib/fcitx/qt/libfcitx-libpinyin-dictmanager.so`.

    ## Gtk:
    1.  `${GTK_IM_MODULE}`:

        环境变量 GTK_IM_MODULE 已经正确地设为了 "fcitx".

    2.  `gtk-query-immodules`:

        1.  gtk 2:

            在 `/usr/bin/gtk-query-immodules-2.0` 找到了 gtk `2.24.24` 的 `gtk-query-immodules`.
            版本行:

                # Created by /usr/bin/gtk-query-immodules-2.0 from gtk+-2.24.24

            已找到 gtk `2.24.24` 的 fcitx 输入法模块.

                "/usr/lib/gtk-2.0/2.10.0/immodules/im-fcitx.so" 
                "fcitx" "Fcitx (Flexible Input Method Framework)" "fcitx" "/usr/share/locale" "ja:ko:zh:*" 

            在 `/usr/bin/gtk-query-immodules-2.0-32` 找到了 gtk `2.24.24` 的 `gtk-query-immodules`.
            版本行:

                # Created by /usr/bin/gtk-query-immodules-2.0-32 from gtk+-2.24.24

            **无法在 `/usr/bin/gtk-query-immodules-2.0-32` 的输出重找到 fcitx.**

        2.  gtk 3:

            在 `/usr/bin/gtk-query-immodules-3.0` 找到了 gtk `3.12.2` 的 `gtk-query-immodules`.
            版本行:

                # Created by /usr/bin/gtk-query-immodules-3.0 from gtk+-3.12.2

            已找到 gtk `3.12.2` 的 fcitx 输入法模块.

                "/usr/lib/gtk-3.0/3.0.0/immodules/im-fcitx.so" 
                "fcitx" "Fcitx (Flexible Input Method Framework)" "fcitx" "/usr/share/locale" "ja:ko:zh:*" 

    3.  Gtk 输入法模块缓存:

        1.  gtk 2:

            在 `/usr/lib/gtk-2.0/2.10.0/immodules.cache` 找到了 gtk `2.24.24` 的输入法模块缓存.
            版本行:

                # Created by gtk-query-immodules-2.0 from gtk+-2.24.24

            已找到 gtk `2.24.24` 的 fcitx 输入法模块.

                "/usr/lib/gtk-2.0/2.10.0/immodules/im-fcitx.so" 
                "fcitx" "Fcitx (Flexible Input Method Framework)" "fcitx" "/usr/share/locale" "ja:ko:zh:*" 

            在 `/usr/lib32/gtk-2.0/2.10.0/immodules.cache` 找到了 gtk `2.24.24` 的输入法模块缓存.
            版本行:

                # Created by usr/bin/gtk-query-immodules-2.0-32 from gtk+-2.24.24

            **无法输入法模块缓存 `/usr/lib32/gtk-2.0/2.10.0/immodules.cache` 中找到 fcitx**

        2.  gtk 3:

            在 `/usr/lib/gtk-3.0/3.0.0/immodules.cache` 找到了 gtk `3.12.2` 的输入法模块缓存.
            版本行:

                # Created by gtk-query-immodules-3.0 from gtk+-3.12.2

            已找到 gtk `3.12.2` 的 fcitx 输入法模块.

                "/usr/lib/gtk-3.0/3.0.0/immodules/im-fcitx.so" 
                "fcitx" "Fcitx (Flexible Input Method Framework)" "fcitx" "/usr/share/locale" "ja:ko:zh:*" 

    4.  Gtk 输入法模块文件:

        1.  gtk 2:

            找到的全部 Gtk 2 输入法模块文件均存在.

        2.  gtk 3:

            找到的全部 Gtk 3 输入法模块文件均存在.

一般经过如上几个步骤后，就能发现问题，根据提示进行修改就可以了。

