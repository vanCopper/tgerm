---
layout: post
comments: 
excerpt:  写App的乐趣就在于，我一个人搞定了所有。不需要扯皮，不需要妥协。
tag: []
title: 微信小程序-蹭饭早知道
---

![](/Users/vancopper/Documents/tgerm/images/wx_02.jpeg)

![](/Users/vancopper/Documents/tgerm/images/wx_01.jpeg)

![](/Users/vancopper/Documents/tgerm/images/wx_03.jpg)

#### 最初的构思

起初这个App的设计要比现在这个复杂一些，但由于微信小程序的限制就阉割成现在的版本。

1. 微信钱包里有一个群收款功能，本以为小程序是有权限发起群收款的，毕竟这个不涉及第三方支付，只是微信钱包内的转账。结果翻遍API，都没有。
2. 想做一个通知功能，但小程序的通知是需要获取一个fromid的，而且是有效期7天，一个fromid对应一个用户的通知，这样如果要做通知就会比较困难。除非我在小程序里收集到足够的fromid，发回服务器储存起来。等到需要通知的时候再找出有效期内的fromid，再进行推送。太麻烦，再说我15块每个月的服务器，别给整奔溃了。

