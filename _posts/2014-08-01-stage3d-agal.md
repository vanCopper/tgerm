---
layout: post
tag: [Stage3D]
title: Stage3D-AGAL
---
前两篇涉及到AGAL的地方，都直接略过了。这里详细理解一下。

**AGAL(Adobe Graphics Assembly Language)**Adobe 图形汇编语言

AGAL是用来编写着色器的，着色器是和显卡交互的程序。所以就可以理解为如果想让显卡对顶点和像素进行操作就要通过编写对应的AGAL代码来实现。

理解AGAL主要是以下几点：

1. 语法
2. 寄存器
3. 寄存器分类和操作

####1.语法

`<opcode> <destination> <source 1> <source 2>`

`opcode`是指要执行的指令，如：`add`,`div`,`mov...`。`destination`保存指令执行的结果。`source 1`,`source 2`是要参与运算的源数据。例如：

`mov v0, va1`：表示将`va1`的值复制到`v0`中。

`mul ft0,ft1,fc1`：表示将`ft1`与`fc1`相乘的结果存放在`ft0`中。

`opcode`大约有30个，具体可以参考这里[opcode1](http://www.adobe.com/cn/devnet/flashplayer/articles/what-is-agal/_jcr_content/articlecontentAdobe/viewlarger.content.html),[opcode2](http://www.adobe.com/cn/devnet/flashplayer/articles/what-is-agal/_jcr_content/articlecontentAdobe/viewlarger_0.content.html)。

####2.寄存器

`<opcode> <destination> <source 1> <source 2>`中的`destination`和`source`称作**寄存器**。可以将**寄存器**理解为变量，它是GPU中的小型内存区域，AGAL程序（着色器）可在执行期间使用它们。每个寄存器占128位，即可存放4个浮点数。4个浮点数称作寄存器的分量，通过`xyzw`或`rgba`进行存取操作。例如访问寄存器`v0`的第一个分量：
<pre> v0.x 或者 v0.r</pre>
我们一般在顶点着色器中访问分量使用`xyzw`，在片段着色器中使用`rgba`。

####3.寄存器分类和操作
寄存器分为三类：顶点着色器使用的寄存器，片段着色器使用的寄存器，两者为交换数据共用的寄存器。参考下表：

| 顶点着色器使用的寄存器 | 共用的寄存器 | 片段着色器使用的寄存器 |
| ---------------------- | ------------ | ---------------------- |
| va:顶点属性寄存器 | v:变量寄存器 | fc:常量寄存器 |
| vc:常量寄存器 |  | ft:临时寄存器 |
| vt:临时寄存器 |  | fs:纹理采样寄存器 |
| op:输出寄存器 |  | oc:输出寄存器|

#####顶点属性寄存器：va0-va7

`0-7`表示索引，共8个可用。也就是说每个顶点均有8个可用的寄存器，那么也就意味着每个顶点有32个数字可以用来存储数据。比如：x,y,z位置数据，UV数据，法线数据等。回想Texture的例子：

{% highlight as3 %}
var vertexData:Vector.<Number> = Vector.<Number>(
[
    // x, y, z, u, v
    -0.5, 0.5, 0, 0, 0,
    0.5, 0.5, 0, 1, 0,
    0.5, -0.5, 0, 1, 1,
    -0.5, -0.5, 0, 0, 1
]);

_context3d.setVertexBufferAt(0, _vertexBuffer, 0,
    Context3DVertexBufferFormat.FLOAT_3);
_context3d.setVertexBufferAt(1, _vertexBuffer, 3,
    Context3DVertexBufferFormat.FLOAT_2);
{% endhighlight %}

从代码里可以知道，每个顶点包含 x, y, z, u, v六个数据。因为每个顶点属性寄存器只能保存4个数字，所以我们需要把数据分别保存在两个不同的属性寄存器中。`_context3d.setVertexBufferAt(0, _vertexBuffer, 0,Context3DVertexBufferFormat.FLOAT_3);`就表示将x, y, z坐标信息保存在`va0`中。`_context3d.setVertexBufferAt(1, _vertexBuffer, 3,Context3DVertexBufferFormat.FLOAT_2);`就表示将u,v保存在`va1`中。

#####常量寄存器：vc0-vc249 & fc0-fc63

AGAL1的版本里vc是128个，fc是28个，AGAL2的版本里vc和fc就分别增加到250个和64个。通过`_context3d.setProgramConstantsFromVector`方法将需要的数据上传至`vc`或`fc`。

#####临时寄存器：vt0-vt25 & ft0-ft15

AGAL1的版本里vt和ft均为8个，AGAL2的版本里vt有26个，ft有16个。可以将临时寄存器理解为局部变量，用来临时存储计算结果等数据的。

#####变量寄存器：v0-v9

AGAL1的版本里v有8个，AGAL2版本里v增加至10个。这些寄存器用于将数据从顶点着色器传递到像素着色器。传递的数据由GPU恰当地插入，使像素着色器能够收到被处理的像素的正确值。比如Texture例子中将UV信息传入`v0`,随后被片段着色器使用：
`mov v0, va1`。

#####纹理采样寄存器：fs0-fs7

纹理采样器寄存器用于基于`UV`坐标，从纹理挑选颜色值。
要使用的纹理通过调用 `Context3D::setTextureAt()` 来指定。
使用纹理采样器的语法为：`fs<n> <flags>` ，其中 `<n>` 是采样器索引，`<flags>` 是一个或多个指定应该如何采样的标志。
`<flags>` 是一个逗号分隔的字符串集，定义：  
纹理维度。选项：2d、cube  
mip 映射。选项：nomip （或 mipnone，它们是相同的）、mipnearest、miplinear  
纹理过滤。选项：nearest、linear  
纹理重复。选项：repeat、wrap、clamp  

例如Texture的例子里:  
<pre>tex ft0, v0, fs0 <2d, repeat, linear, nomip></pre>
***
>原创博文，转载请注明  
>作者：vanCopper  
>Blog: http://blog.as3er.com http://blog.copper3d.org
