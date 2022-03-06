---
title: Away3D 热扰动特效（HeatHaze）
layout: post
tags: [Away3D, HeatHazeEffect]
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

热扰动其实就是折射。就像看夏天烈日下的柏油马路时，路面好像扭曲了一样。折射的产生是因为不同的介质对光线有不同的折射率。折射的模拟大概有两种方法：1.事前将环境中的折射渲染至一张用来扰动的图片，然后在游戏运行时加载图片后对场景进行扰动。2.将扰动体RTT，然后动态分配一个扰动参数来实时模拟。下面的实现是第二种方案。

效果图：（点击Demo,在Demo中按A键切换效果）

![image](../../images/wp-content/uploads/2014/05/heatDemo.jpg)

[Demo][1]

1.大多数情况下，都是在播放特效的时候需要这种扭曲效果（如上图）。所以要将正常的渲染对象和扰动体做一个区分。要在Entity.as中添加如下代码:

<pre class="brush:as3">/**
* 粒子层 
*/      
public static const PARTICLE_LAYER:uint = 2;

/**
* 热干扰类型
* 0不是热干扰体，1是热干扰体并渲染干扰体本身，2是热干扰体但不渲染干扰体本身 
*/      
public var heatHazeType:uint = 0;</pre>

2.在收集器里，也要讲Particle单独收集至RenderableListItem。在EntityCollector.as中添加对应代码:

<pre class="brush:as3">protected var _particleRenderableHead:RenderableListItem;//Particle Renderable
//在applyRenderable方法中修改收集判断
if(renderable.sourceEntity.renderLayer == Entity.AVATAR_LAYER)//Avatar层
{
    item.next = _avatarRenderableHead;
    _avatarRenderableHead = item;
}else if(renderable.sourceEntity.renderLayer == Entity.PARTICLE_LAYER)//Particle层
{
    item.next = _particleRenderableHead;
    _particleRenderableHead = item;
}else if(material.requiresBlending)
{
    item.next = _blendedRenderableHead;
    _blendedRenderableHead = item;
} else
{
    item.next = _opaqueRenderableHead;
    _opaqueRenderableHead = item;
}
//要在clear方法中清楚收集
_particleRenderableHead = null;</pre>

3.根据heatHazeType来确定渲染方式，修改DefaultRenderer.as的drawRenderables方法，还要修改draw方法来正常渲染粒子层

<pre class="brush:as3">//修改drawRenderables方法
var numPasses:uint;
var j:uint;
var camera:Camera3D = entityCollector.camera;
var item2:RenderableListItem;
var singlePassMat:SinglePassMaterialBase;

while (item) 
{
    if(item.renderable.sourceEntity.heatHazeType == 2)
    {
        item = item.next;
        continue;
    }
}
//修改draw方法，添加粒子的渲染
drawRenderables(entityCollector.opaqueRenderableHead, entityCollector, which);
drawRenderables(entityCollector.blendedRenderableHead, entityCollector, which);
drawRenderables(entityCollector.particleRenderableHead, entityCollector, which);
//还要将扰动体RTT，所以要在executeRender方法中添加对应代码
if(_view3D && _view3D.filters3d)
{
    for each(var filter:Filter3DBase in _view3D.filters3d)
    {
        if(filter is HeatHazeFilter3D)
        {
            filter.helpRender(stage3DProxy, entityCollector, _textureRatioX, _textureRatioY);
            break;
        }
    }
}</pre>

4.最后是Filter：Filter3DHeatHazeTask.as,HeatHazeFilter3D.as,HeatHazeRenderer.as其中Filter3DheatHazeTask中的shader可参考[GUP精粹2的第19章][2]

Filter3DHeatHazeTask.as

<pre class="brush:as3">package copper3d.filters.tasks
{
    import flash.display3D.Context3DBlendFactor;
    import flash.display3D.Context3DProgramType;
    import flash.display3D.textures.Texture;

    import away3d.cameras.Camera3D;
    import away3d.core.managers.Stage3DProxy;
    import away3d.filters.tasks.Filter3DTaskBase;
    import away3d.textures.RenderTexture;

    /**
     * 热扰动 
     * @author vancopper
     * 
     */ 
    public class Filter3DHeatHazeTask extends Filter3DTaskBase
    {
        private var _data:Vector.;
        public var heatMap:RenderTexture;

        public function Filter3DHeatHazeTask()
        {
            _data = Vector.([1, 1, 0.0015, 1, 2, 2, 0, 0]);
        }

        override protected function getFragmentCode():String
        {
            var code:String = "";

            code += "tex ft1, v0, fs1 &lt;2d, nearest&gt;\n"
                + "mul ft0,ft1,fc1\n"
                + "sub ft0,ft0,fc0\n"
                + "mul ft0,ft0,fc0.z\n"
                + "add ft0,v0,ft0\n"
                + "tex oc, ft0, fs0 &lt;2d, nearest&gt;\n";
            return code;
        }

        override public function activate(stage3DProxy:Stage3DProxy, camera:Camera3D, depthTexture:Texture):void
        {
            stage3DProxy.context3D.setBlendFactors(Context3DBlendFactor.ONE, Context3DBlendFactor.ZERO);
            stage3DProxy.context3D.setProgramConstantsFromVector(Context3DProgramType.FRAGMENT, 0, _data, 2);
            stage3DProxy.context3D.setTextureAt(1, heatMap.getTextureForStage3D(stage3DProxy));
        }

        override public function deactivate(stage3DProxy:Stage3DProxy):void
        {
            stage3DProxy.context3D.setTextureAt(1, null);
        }

        /**
         * 扰动强度 
         */
        public function get disturb():Number
        {
            return _data[2];
        }

        /**
         * @private
         */
        public function set disturb(value:Number):void
        {
            _data[2] = value;
        }

    }
}</pre>

HeatHazeFilter3D.as

<pre class="brush:as3">package copper3d.filters
{
    import away3d.arcane;
    import away3d.core.managers.Stage3DProxy;
    import away3d.core.traverse.EntityCollector;
    import away3d.filters.Filter3DBase;
    import away3d.textures.RenderTexture;

    import copper3d.core.render.HeatHazeRenderer;
    import copper3d.filters.tasks.Filter3DHeatHazeTask;

    use namespace arcane;

    /**
     * 热扰动 
     * @author vancopper
     * 
     */ 
    public class HeatHazeFilter3D extends Filter3DBase
    {
        private var _heatFilterTask:Filter3DHeatHazeTask;
        private var _renderTexture:RenderTexture;
        private var _render:HeatHazeRenderer;

        public function HeatHazeFilter3D()
        {
            _renderTexture = new RenderTexture(2,2);
            _heatFilterTask = new Filter3DHeatHazeTask();
            _render = new HeatHazeRenderer();
            addTask(_heatFilterTask);
        }

        override public function helpRender(stage3DProxy : Stage3DProxy, collector:EntityCollector, textureRatioX:Number, textureRatioY:Number):void
        {
            var stage3DIndex:int = stage3DProxy.stage3DIndex;
            _render.stage3DProxy = stage3DProxy;
            _render.textureRatioX = textureRatioX;
            _render.textureRatioY = textureRatioY;
            _heatFilterTask.heatMap = _renderTexture;
            _render.render(collector, _renderTexture.getTextureForStage3D(stage3DProxy));
        }

        override public function dispose():void
        {
            super.dispose();
            _renderTexture.dispose();
        }

        override public function set textureWidth(value : int):void
        {
            super.textureWidth = value;
            _renderTexture.width = value;
        }

        override public function set textureHeight(value:int):void
        {
            super.textureHeight = value;
            _renderTexture.height = value;
        }

        /**
         * 热扰动强度 
         */
        public function get disturb():Number
        {
            return _heatFilterTask.disturb;
        }

        /**
         * @private
         */
        public function set disturb(value:Number):void
        {
            _heatFilterTask.disturb = value;
        }

    }
}</pre>


`HeatHazeRenderer.as`

<pre class="brush:as3">package copper3d.core.render
{
    import flash.display3D.textures.TextureBase;

    import away3d.arcane;
    import away3d.cameras.Camera3D;
    import away3d.core.data.RenderableListItem;
    import away3d.core.render.RendererBase;
    import away3d.core.traverse.EntityCollector;
    import away3d.materials.MaterialBase;

    use namespace arcane;

    public class HeatHazeRenderer extends RendererBase
    {

        private var _activeMaterial:MaterialBase;

        public function HeatHazeRenderer()
        {
        }

        override protected function draw(entityCollector:EntityCollector, target:TextureBase):void
        {
            drawRenderables(entityCollector.particleRenderableHead, entityCollector, true);
            if (_activeMaterial)
            {
                _activeMaterial.deactivate(_stage3DProxy);
            }
            _activeMaterial = null;
        }

        private function drawRenderables(renderableListItem:RenderableListItem, entityCollector:EntityCollector, flag:Boolean):void
        {
            var numPasses:uint;
            var i:uint;
            var renderableListItem1:RenderableListItem;
            var heatHazeType:int;
            var camera:Camera3D = entityCollector.camera;
            while (renderableListItem) {
                _activeMaterial = renderableListItem.renderable.material;
                _activeMaterial.updateMaterial(_stage3DProxy.context3D);
                numPasses = _activeMaterial.numPasses;
                i = 0;
                do  
                {
                    renderableListItem1 = renderableListItem;
                    _activeMaterial.activatePass(i, _stage3DProxy, camera);
                    do  
                    {
                        heatHazeType = renderableListItem1.renderable.sourceEntity.heatHazeType;
                        if (heatHazeType != 0)
                        {
                            _activeMaterial.renderPass(i, renderableListItem1.renderable, _stage3DProxy, entityCollector, _rttViewProjectionMatrix);
                        } 
                        renderableListItem1 = renderableListItem1.next;
                    } while (renderableListItem1 && renderableListItem1.renderable.material == _activeMaterial);

                    _activeMaterial.deactivatePass(i, _stage3DProxy);
                } while (++i &lt; numPasses)
                renderableListItem = renderableListItem1;
            }
        }
    }
}
</pre>

 [1]: http://blog.as3er.com/demo/HeatHaze.html
 [2]: http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter19.html