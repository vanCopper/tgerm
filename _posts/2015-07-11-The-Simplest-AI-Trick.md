---
layout: post
comments: true
excerpt:  The Simplest AI Trick
tag: [Stage3D]
title: The Simplest AI Trick
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

> 参考资料：[GDC Vault - The Simplest AI Trick in the Book](http://www.gdcvault.com/play/1020104/The-Simplest-AI-Trick-in)

好久没有更新博客了，好像没有什么动力写文了。项目中的怪的AI是完全放在服务端的，经常看到怪会叠在一起，就想看看有没有什么既简单又不重叠的做法。本不是该我操心的事，我就是爱管闲事啊。噼里啪啦写了个简单Demo。

####1）预先生成怪物的目标点并进行排序

![image](../../images/simpleAI_01.png)

**图一**

怪（红色圈点，即所有需要移动后才能攻击的怪）随机分布在玩家（绿色方块）四周。那么怪把人围起来的第一步自然是生成怪的目标点（这里假设就是圆形）。

可以根据怪的数量在距玩家一定距离的地方生成圆形包围圈，然后对目标点按照从上往下，或者从左往右进行排序。排序后目标点列表即是有序列表，那么用同样的办法对怪进行排序。最终每个怪都有了自己的目标点。

![image](../../images/simpleAI_02.png)

**图二**

####2）移动至目标点

![image](../../images/simpleAI_03.gif)

**图三**

####3）不同攻击距离的怪
如果怪的攻击范围并不是一致的，上面的做法就无法满足需求了。解决办法就只要将怪物攻击距离带入生成目标点的计算即可。

![image](../../images/simpleAI_04.gif)

**图四**
