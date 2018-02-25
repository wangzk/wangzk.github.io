---
title:  "Set HighDPI environment for Eclipse"
date:   2018-02-25 08:32:00 +0800
categories: java 
---

To make Eclipse work well in the HighDPI environment in Linux, it needs to do the following configuration:

1. Make the font look bigger ([reference page](https://www.eclipse.org/eclipse/news/4.6/platform.php)): run eclipse with the environment variable `GDK_DPI_SCALE`.

> On GTK, the standard way to configure scaling for a single application is to set the GDK_DPI_SCALE environment variable before launching an application. E.g. to set the scale factor to 150% on the command line when launching Eclipse:

``` shell
$ GDK_DPI_SCALE=1.5 ./eclipse
```

2. Make icons look bigger ([reference page](https://www.eclipse.org/forums/index.php?t=msg&th=1088764&goto=1777163&#msg_1777163)): edit `$ECLIPSE_HOME/eclipse.ini` and add the following lines to the file:
```
-Dswt.enable.autoScale=true
-Dswt.autoScale=200
-Dswt.autoScale.method=nearest
```

Restart the eclipse and it works!

Tested on Eclipse 4.7.2.