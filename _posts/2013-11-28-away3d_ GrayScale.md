---
title: Away3D 灰度图全屏滤镜（GrayScale）
layout: post
tage: [Stage3D, Away3D, AS3]
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

away3d里面提供几种全屏特效：BloomFilter3D，BlurFilter3D，DepthOfFieldFilter3D，HBlurFilter3D， HDepthOfFieldFilter3D，HueSaturationFilter3D，MotionBlurFilter3D，RadialBlurFilter3D， VBlurFilter3D，VDepthOfFieldFilter3D

今天lipi提到了灰度图效果，花时间弄了一个。先看下最终效果：

![image](../../images/wp-content/uploads/2013/11/灰度图-300x224.jpg)

<a title="GrayScaleDemo" href="http://blog.as3er.com/demo/GrayScale.html" target="_blank">Demo链接</a>

1.添加滤镜Task：Filter3DGrayScaleTask.as 用了两种实现方法，第一种灰度效果会偏暗，第二种效果稍微好些，并且几个参数都是可调的。公式来自Google，所以里面的0.3，0.59，0.11是公式推导出来的，有兴趣的可以去Google下。

<pre class="brush:as3">package away3d.filters.tasks
{
    import flash.display3D.Context3DProgramType;
    import flash.display3D.textures.Texture;

    import away3d.cameras.Camera3D;
    import away3d.core.managers.Stage3DProxy;

    /**
     *  
     * @author vancopper
     * 
     */ 
    public class Filter3DGrayScaleTask extends Filter3DTaskBase
    {
        private var _rfactor:Number = 0.3;
        private var _gfactor:Number = 0.59;
        private var _bfactor:Number = 0.11;
        public function Filter3DGrayScaleTask(requireDepthRender:Boolean=false)
        {
            super(requireDepthRender);
        }

        public function get bfactor():Number
        {
            return _bfactor;
        }

        public function set bfactor(value:Number):void
        {
            _bfactor = value;
        }

        public function get gfactor():Number
        {
            return _gfactor;
        }

        public function set gfactor(value:Number):void
        {
            _gfactor = value;
        }

        public function get rfactor():Number
        {
            return _rfactor;
        }

        public function set rfactor(value:Number):void
        {
            _rfactor = value;
        }

        override protected function getFragmentCode():String
        {
//-------------公式一 偏暗 ----------------//
//          var code:String = "tex ft0, v0, fs0 &lt;2d,clamp,linear&gt;\n" +
//
//              "dp3 ft0.x, ft0, fc0\n" +
//              
//              "mov ft0.y, ft0.x\n" +
//              
//              "mov ft0.z, ft0.x\n" +
//              
//              "mov oc, ft0\n";
//          
//-------------公式二-------------------//         
//          val = 0.3*R + 0.59*G + 0.11*B;
//          R = val;
//          G = val;
//          B = val;
            var code:String = 
                "tex ft0, v0, fs0 &lt;2d,linear,nomip&gt;\n" +
                "mul ft1.x, ft0.x, fc1.x\n" +
                "mul ft1.y, ft0.y, fc1.y\n" +
                "mul ft1.z, ft0.z, fc1.z\n" +
                "add ft1.w, ft1.x, ft1.y\n" +
                "add ft1.w, ft1.w, ft1.z\n" +
                "mov ft0.x, ft1.w\n" +
                "mov ft0.y, ft1.w\n" +
                "mov ft0.z, ft1.w\n" +
                "mov oc,ft0";

            return code;
        }

        override public function activate(stage3DProxy:Stage3DProxy, camera:Camera3D, depthTexture:Texture):void
        {
            stage3DProxy.context3D.setProgramConstantsFromVector(Context3DProgramType.FRAGMENT, 1, Vector.&lt;Number&gt;([_rfactor, _gfactor, _bfactor,0]) );
        }
    }
}</pre>

2.GrayScaleFilter3D.as 公开Task的几个可调的参数。

<pre class="brush:as3">package away3d.filters
{
    import away3d.filters.tasks.Filter3DGrayScaleTask;

    /**
     * 灰度滤镜 
     * @author vancopper
     * 
     */ 
    public class GrayScaleFilter3D extends Filter3DBase
    {
        private var _grayScaleTask:Filter3DGrayScaleTask;
        public function GrayScaleFilter3D()
        {
            super();
            _grayScaleTask = new Filter3DGrayScaleTask();
            addTask(_grayScaleTask);
        }

        public function get bfactor():Number
        {
            return _grayScaleTask.bfactor;
        }

        public function set bfactor(value:Number):void
        {
            _grayScaleTask.bfactor = value;
        }

        public function get gfactor():Number
        {
            return _grayScaleTask.gfactor;
        }

        public function set gfactor(value:Number):void
        {
            _grayScaleTask.gfactor = value;
        }

        public function get rfactor():Number
        {
            return _grayScaleTask.rfactor;
        }

        public function set rfactor(value:Number):void
        {
            _grayScaleTask.rfactor = value;
        }

    }
}</pre>

3.用法就更简单了添加Filter到View3D就可以了

<pre class="brush:as3">var grayScaleFilter:GrayScaleFilter3D = new GrayScaleFilter3D();
view.filters3d = [grayScaleFilter];</pre>

 [1]: http://blog.as3er.com/wp-content/uploads/2013/11/灰度图.jpg