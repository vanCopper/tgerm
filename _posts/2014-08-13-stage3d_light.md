---
layout: post
tag: [Stage3D]
title: Stage3D-光照
---
###光特性
参考OpenGL的光照模型，把光分成4种独立的成分：

1. 环境光
2. 散射光
3. 镜面光
4. 发散光

#####1.环境光：ambient light
环境光是那些在环境中进行了充分的散射，无法分辨其方向的光。它会均匀的照亮物体。

#####2.漫反射光：diffuse light
漫反射光来自某个方向，但在物体表面上向各个方向上反射，无论在何处观察，散射光看上去亮度都相同。我们之所以能看到物体，就是因为物体将入射的光向各个方向反射（所以称之为漫反射）

#####3.镜面光：specular light
镜面光来自一个特定的方向，并在物体表面以特定的方向反射出去。所以镜面光会让物体看起来有光泽，如金属表面的光泽。

#####4.发射光：emission light
发射光是由物体本身发射的光。

###材质属性
光分成了4种成分，那么对应的材质也有对着4种光成分的反射率。物体最终呈现的颜色就是物体表面（材质）对不同光成分反射后所得到的颜色。

1.  环境光材质
2.  漫反射光材质
3.  镜面光材质
4.  发射光材质

#####1.环境光材质
环境光材质的反射率影响物体的整体颜色，并且反射率不受观察点影响。

#####2.漫反射光材质
漫反射光材质的反射率同样影响物体颜色。对颜色的影响取决于漫反射光的颜色以及与法线的夹角的影响，而不受观察点位置的影响。

#####3.镜面光材质
物体对光的镜面反射材质属性决定了光泽的颜色、大小和亮度。镜面反射光的强度还取决于观察点的位置，当观察点正好处于入射光的反射光线上，亮斑的亮度到达最大值。


#####4.发射光材质
前面提到的三种材质都是被动地反射来自外界的光线，而有些物体本身可以发射光。

###光照计算
光照效果是由发射光，环境光，漫反射光以及镜面高光四部分组成，这四部分各自独立计算，然后再累加起来得到最终的光照效果。
对于光照着色有**高洛德着色（Gouraud Shading）**与**冯氏着色（Phong Shading）**。

* 高洛德着色：也被称为Per-Vertex着色，它是在顶点着色阶段对顶点进行颜色计算，然后在光栅化阶段对这些顶点颜色进行线性插值形成片段的颜色。
* 冯氏着色：也被称为Per-Pixel像素着色，它是在片段着色阶段对每一个片段（像素）进行颜色计算。

**冯氏着色**得到效果更好。

<pre>
光照最终颜色 = 发射颜色 + 环境颜色 + 漫反射颜色 + 镜面反射颜色
</pre>

我只实现了**环境颜色**和**漫反射颜色**，其他同理。

#####漫反射颜色
<pre>
diffuseColor = MaterialDiffuseColor * LightColor * cos(Θ)
</pre>

**MaterialDiffuseColor:** 我们直接取材质颜色。

**cos(Θ):** 是表面法向与灯光方向的夹角。
公式在AGAL中即：
<pre>
//纹理采样
"tex ft0, v1, fs0<2d, linear, repeat>\n" +
//法线纹理
"tex ft1, v1, fs1<2d, linear, repeat>\n" +
//法线转换到世界空间
"m44 ft2 ft1 fc0\n"+
"nrm ft2.xyz ft2.xyz\n"+
//求法线和灯光的角度
"dp3 ft2.w ft2.xyz fc3.xyz\n"+
//取出大于0的部分
"max ft2.w ft2.w fc4.w\n"+
//diffuseColor = ft2.w * lightDiffuseColor;
"mul ft3.xyzw ft2.wwwww fc1.xyzw\n"+
//混合漫反射光
"mul ft3 ft0 ft3\n"
</pre>

#####环境颜色
<pre>
ambientColor = ambientLightColor * ambientMaterialColor
</pre>

**ambientMaterialColor:**直接使用贴图颜色

<pre>
//混合环境光 ft0:贴图 fc2:环境光颜色
"mul ft4 ft0 fc2\n"
</pre>

最后将颜色叠加：

<pre>
"add oc ft3 ft4\n"
</pre>

直接运行[Demo](../images/LightTest.swf),源码在下面的Github链接中。

*** 

> 原创博文，转载请注明  
> 作者：vanCopper  
> Blog: http://blog.as3er.com http://blog.copper3d.org  
> GitHub:https://github.com/vanCopper/Stage3DGuide
