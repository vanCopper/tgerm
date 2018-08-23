---
layout: post
comments: true
excerpt:  使用Vertex Shader实现简单变形
tag: [Stage3D]
title: Stage3D-Vertex Shader Morphing
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

关于游戏我一直是国产黑，之所以坚持做这行，多是出于对技术的喜欢。目前的确还没有除写代码之外特别想做的事情（当老板，赚大钱，走向人生巅峰除外）。所以还是继续来折腾代码吧。

先来看Demo:

<div id="flashcontent"></div>
<script type="text/javascript">
var flashvars = {};
var params = {wmode:'direct'};
var attributes = {};
swfobject.embedSWF(
'../swf/Stage3DGuide.swf',
'flashcontent',
'800',
'600',
'14.0',
null,
flashvars,
params,
attributes,
null
);
</script>

其实是把球体进行了Wave扰动。对顶点进行扰动即可。  
**MorphingShader.as**
{% highlight as3 %}
package com.core.shaders
{
	/**
	 * 
	 * @author vancopper
	 * 
	 */	
	public class MorphingShader extends ShaderBase
	{
		public function MorphingShader()
		{
			super();
		}
		override public function get vertexSrc():String
		{
			var str:String =
				"mov vt0, va0	\n" +
				//wave
				"dp4 vt2, vt0, vc4	\n" +
				"cos vt3, vt2	\n" +
				"sin vt3, vt3   \n" +
				"add vt1, vt0, vt3	\n" +
				//lerp
				"sub vt0, vt1, va0  \n" +
				"mul vt0, vt0, vc5	\n" +
				"add vt0, vt0, va0	\n" +
				
				// project 
				"m44 op, vt0, vc0	\n" +
				//UV
				"mov v0, va1	\n" +
				//Normal
				"mov v1, va2	\n";
			
			return str; 
		}
		
		override public function get fragmentSrc():String
		{
			return  "tex ft0, v0, fs0 <2d, repeat, linear, nomip>\n" +
				"mov oc ft0\n";
		}
	}
}
{% endhighlight %}

完整的代码访问gitHub即可：

> GitHub:[https://github.com/vanCopper/Stage3DGuide]( https://github.com/vanCopper/Stage3DGuide)