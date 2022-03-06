---
layout: post
tag: [Stage3D]
title: Stage3D-3D世界
---

<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

先来理解一个重要的概念**矩阵**。
ActionScript3中提供了**矩阵**的类：[Matrix3D](http://help.adobe.com/zh_CN/FlashPlatform/reference/actionscript/3/flash/geom/Matrix3D.html)

>Matrix3D 类表示一个转换矩阵，该矩阵确定三维 (3D) 显示对象的位置和方向。该矩阵可以执行转换功能，包括平移（沿 x、y 和 z 轴重新定位）、旋转和缩放（调整大小）。Matrix3D 类还可以执行透视投影，这会将 3D 坐标空间中的点映射到二维 (2D) 视图。

![](../../images/Matrix3Delements.jpg)

既然**矩阵**可以用来控制3D显示对象的位置等，我们就把**Texture**的例子修改一下。用**矩阵**来让显示对象动起来。


需要修改部分代码来实现上面的效果：

* 首先我们要有一个`矩阵`来对应3D的显示对象。
<pre>
private var _modelMatrix:Matrix3D = new Matrix3D();
//在render方法中 将矩阵上传至 vc0
if(_t > .5) _speed = -.02;
if(_t < -.5) _speed = .02;
_t += _speed;
_modelMatrix.identity();
_modelMatrix.appendTranslation(_t, 0, 0);
_context3d.setProgramConstantsFromMatrix(Context3DProgramType.VERTEX, 0, _modelMatrix, true);
</pre>

* 其次对AGAL代码进行对应的修改。
<pre>
var vertexSrc:String = "m44 op, va0, vc0\n" +
	"mov v0, va1\n";
</pre>
`m44 op, va0, vc0`这句代码就是将顶点矩阵与变换矩阵进行乘法操作。这样一来显示对象就会叠加上变换矩阵，进行了平移，旋转，缩放操作。

进入正题，构建一个3D场景我们需要利用矩阵进行一些几何变换。这些几何变换按照执行顺序依次是：

1. 视图变换
2. 模型变换
3. 投影变换
4. 视口变换

##### 1.视图变换

**视图变换**是我们应用的第一个变换，它主要是用来确定观察点位置，也可以理解为摄像机位置。需要注意的是，在进行其他任何变换之前必须先指定视图变换。

##### 2.模型变换

**模型变换**主要是对3D对象本身进行的移动，旋转，缩放操作。

##### 3.投影变换

**投影变换**建立了一个裁剪平面，用于确定哪些3D显示对象可以被看到。投影又分为：**正投影（平行投影）**和**透视投影**。

######正投影：几何图形会以指定的大小直接被映射到2D屏幕上，也就是没有近大远小的效果。  

######透视投影：通过透视投影，场景会显示的更接近现实情况。即有近大远小的效果。

我们这里只讨论**透视投影**。使用**平截头体**来定义**透视投影**。**平截头体**最终会转化为**投影矩阵**,具体推导算法我们不在这里讨论。我们大概理解一下**平截头体**是什么样子，如何定义它。

**平截头体**示意图：  
![](../../images/perspective.gif)

`fovy:` 定义了 camera 在 y 方向上的视线角度（介于 0 ~ 180 之间）

`aspect:` 定义了近裁剪面的宽高比 aspect = w/h

`zNear, zFar:` 定义了从 Camera/Viewer 到远近两个裁剪面的距离(正值)。
在Adobe官方提供的工具类中，可通过`PerspectiveMatrix3D.perspectiveFieldOfViewRH()`来创建平截头体。
<pre>
_projectionmatrix = new PerspectiveMatrix3D();
// 45 degrees FOV, 700/500 aspect ratio, 0.1=near, 100=far
_projectionmatrix.perspectiveFieldOfViewRH(45.0, 700 / 500, 0.01, 100.0);
</pre>
##### 4.视口变换

**视口变换**就是将最终变换后的结果映射到窗口上。这步操作，不需要我们去关注细节。

所以我们为了显示3D场景，最终需要做的事情就是执行下面的这个几何变换：

**投影矩阵 × 视图矩阵 × 模型矩阵（左乘矩阵，变换效果是按从右向左）**
反应在代码里就是：
<pre>
_viewMatrix.identity();
_viewMatrix.append(_modelMatrix);
_viewMatrix.append(_cameraMatrix);
_viewMatrix.append(_projectionmatrix);
</pre>

我们继续修改**Texture**的例子，让矩形自身绕Y轴旋转，让镜头绕Z轴旋转。
执行完整代码即可观察到效果：
{% highlight as3 %}
package
{
import com.adobe.utils.PerspectiveMatrix3D;
import com.adobe.utils.extended.AGALMiniAssembler;

import flash.display.Bitmap;
import flash.display.Sprite;
import flash.display.Stage3D;
import flash.display3D.Context3D;
import flash.display3D.Context3DProfile;
import flash.display3D.Context3DProgramType;
import flash.display3D.Context3DRenderMode;
import flash.display3D.Context3DTextureFormat;
import flash.display3D.Context3DVertexBufferFormat;
import flash.display3D.IndexBuffer3D;
import flash.display3D.Program3D;
import flash.display3D.VertexBuffer3D;
import flash.display3D.textures.Texture;
import flash.events.ErrorEvent;
import flash.events.Event;
import flash.geom.Matrix3D;
import flash.geom.Vector3D;

[SWF(backgroundColor="#333333", frameRate="60", width="800", height="600")]
public class TextureTest extends Sprite
{
private var _context3d:Context3D;
private var _stage3d:Stage3D;
private var _modelMatrix:Matrix3D = new Matrix3D();
private var _projectionmatrix:PerspectiveMatrix3D;
private var _cameraMatrix:Matrix3D;
private var _viewMatrix:Matrix3D;

private var _vertexBuffer:VertexBuffer3D;
private var _indexBuffer:IndexBuffer3D;

private var _program3d:Program3D;

private var _texture:Texture;

[Embed(source="./assets/floor_diffuse.jpg")]
private static var TextureClass:Class;

public function TextureTest()
{
​    super();
​    addEventListener(Event.ADDED_TO_STAGE, onAddToStage);
}

private function onAddToStage(e:Event):void
{
​    removeEventListener(Event.ADDED_TO_STAGE, onAddToStage);
​    if(this.stage.stage3Ds.length > 0)
​    {
​        _stage3d = this.stage.stage3Ds[0];
​        _stage3d.addEventListener(ErrorEvent.ERROR, onCreateContext3DError);
​        _stage3d.addEventListener(Event.CONTEXT3D_CREATE, onContext3DCreated);
​        _stage3d.requestContext3D(Context3DRenderMode.AUTO, Context3DProfile.STANDARD);
​    }
}

private function onContext3DCreated(event:Event):void
{
​    initContext3D();
​    initBuffer();
​    initTexture();
​    initProgram();

    addEventListener(Event.ENTER_FRAME, render);
}

private var _t:Number = 0;
private var _speed:Number = .02;
private var _degrees:Number = 0;
private function render(event:Event):void
{
​    if(_t > .5) _speed = -.02;
​    if(_t < -.5) _speed = .02;

    _t += _speed;
    _degrees += 2.0;
    _modelMatrix.identity();
//          _modelMatrix.appendTranslation(_t, 0, 1);
​    _modelMatrix.appendRotation(_degrees*1.0, Vector3D.Y_AXIS);

    _cameraMatrix.identity();
    _cameraMatrix.appendTranslation(0, 0, -5);
    _cameraMatrix.appendRotation(_degrees, Vector3D.Z_AXIS);
    
    _viewMatrix.identity();
    _viewMatrix.append(_modelMatrix);
    _viewMatrix.append(_cameraMatrix);
    _viewMatrix.append(_projectionmatrix);
    
    _context3d.setProgramConstantsFromMatrix(Context3DProgramType.VERTEX, 0, _viewMatrix, true);
    
    _context3d.clear(0, 0, 0);
    _context3d.drawTriangles(_indexBuffer);
    _context3d.present();
}

private function onCreateContext3DError(event:ErrorEvent):void
{
​    trace(event.text);
}

private function initContext3D():void
{
​    _context3d = _stage3d.context3D;
​    _stage3d.x = 50;
​    _stage3d.y = 50;
​    _context3d.configureBackBuffer(700, 500, 2);

    _projectionmatrix = new PerspectiveMatrix3D();
    // 45 degrees FOV, 700/500 aspect ratio, 0.1=near, 100=far
    _projectionmatrix.perspectiveFieldOfViewRH(45.0, 700 / 500, 0.01, 100.0);
    
    _cameraMatrix = new Matrix3D();
    _cameraMatrix.appendTranslation(0, 0, -5);
    
    _viewMatrix = new Matrix3D();
}

private function initBuffer():void
{
​    var vertexData:Vector.<Number> = Vector.<Number>(
​        [
​            // x, y, z, u, v
​            -0.5, 0.5, 0, 0, 0,
​            0.5, 0.5, 0, 1, 0,
​            0.5, -0.5, 0, 1, 1,
​            -0.5, -0.5, 0, 0, 1
​        ]);

    var indexData:Vector.<uint> = Vector.<uint>(
        [0, 1, 2, 2, 3, 0]);
    
    _vertexBuffer = _context3d.createVertexBuffer(vertexData.length/5, 5);
    _vertexBuffer.uploadFromVector(vertexData, 0, vertexData.length/5);
    
    _indexBuffer = _context3d.createIndexBuffer(indexData.length);
    _indexBuffer.uploadFromVector(indexData, 0, indexData.length);
}

private function initTexture():void
{
​    _texture = _context3d.createTexture(512, 512, Context3DTextureFormat.BGRA, true);
​    _texture.uploadFromBitmapData((new TextureClass() as Bitmap).bitmapData);
}

private function initProgram():void
{
​    var vertexSrc:String = "m44 op, va0, vc0\n" +
​        "mov v0, va1\n";
​    var fragmentsrc:String = "tex ft0, v0, fs0 <2d, repeat, linear, nomip>\n" +
​        "mov oc ft0\n";
​    var shaderAssembler:AGALMiniAssembler = new AGALMiniAssembler();
​    _program3d = shaderAssembler.assemble2(_context3d, 2, vertexSrc, fragmentsrc);

    _context3d.setVertexBufferAt(0, _vertexBuffer, 0,
        Context3DVertexBufferFormat.FLOAT_3);
    _context3d.setVertexBufferAt(1, _vertexBuffer, 3,
        Context3DVertexBufferFormat.FLOAT_2);
    _context3d.setTextureAt(0, _texture);
    _context3d.setProgram(_program3d);

}

}
}
{% endhighlight %}
***
>原创博文，转载请注明   
>作者：vanCopper  
>Blog: http://blog.as3er.com http://blog.copper3d.org
