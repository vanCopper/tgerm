---
title: AS3 Graphics 多次绘制
layout: post
tags: [AS3]
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

AS3中 Sprite和Shape类都持有一个Graphics对象，利用Graphics对象可以方便的利用内置的绘图方法绘制一些简单的图形。

之前在游戏中做新手引导的时候利用显示对象的BlendMode可以实现一个镂空的光圈引导，后来看到有人用Graphics连续画两个形状就实现了。

![image](../../images/wp-content/uploads/2012/08/截屏13-5-1_下午3_26-5-300x241.png)

<pre class="brush:as3">package
{
    import flash.display.Sprite;

    /**
     * 
     * @author vanCopper
     */
    public class Ts extends Sprite
    {
        public function Ts()
        {
            var sw:int = this.stage.stageWidth;
            var sh:int = this.stage.stageHeight;
            var hollowMask:Sprite = new Sprite;

            hollowMask.graphics.beginFill(0x333333,.8);
            hollowMask.graphics.drawRect(sw/4,sh/4,sw/2,sh/2);
            //hollowMask.graphics.beginFill(0xFF9aff);
            hollowMask.graphics.drawCircle(200,150,30);
            hollowMask.graphics.endFill();
            addChild(hollowMask);
        }
    }
}</pre>

&nbsp;

 [1]: http://blog.as3er.com/wp-content/uploads/2012/08/截屏13-5-1_下午3_26-5.png