---
title: Mac OS搭建 openGL开发环境
layout: post
tag: [OpenGL]
---
**<span style="color: #ff6600;">原创博文，转载请声明</span>**

参考自<openGL超级宝典>

1.从<a href="https://code.google.com/p/oglsuperbible5/source/checkout" target="_blank">https://code.google.com/p/oglsuperbible5/source/checkout</a>下载源码

2.在xCode中创建Cocoa application

![image](../../images/wp-content/uploads/2013/12/01-300x206.png)

3.删除项目中的AppDelegate.h,AppDelegate.m,MainMenu.xib,main.m

![image](../../images/wp-content/uploads/2013/12/02-300x167.png)

4.添加GLTools搜索路径，GLTools在第一步下载的src文件夹中

![image](../../images/wp-content/uploads/2013/12/03-300x71.png)

![image](../../images/wp-content/uploads/2013/12/04-300x184.png)

5.右键单击&#8221;Frameworks&#8221;文件夹，添加&#8221;OpenGL.framework&#8221;和&#8221;GLUT.framework&#8221;(System/Library/Frameworks/GLUT.framework&OpenGL.framework)

6.在Supporting Files中新建C++ Files 编写对应代码，编译运行 

![image](../../images//wp-content/uploads/2013/12/05-300x190.png)


