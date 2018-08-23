---
layout: post
comments: true
excerpt:  关于Flash Worker安全沙箱错误问题
tag: [Stage3D]
title: Flash Worker Sandbox
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

上个项目利用Flash Worker做了文件解析，很大程度上解决了第一次进场景帧频较低的问题。前几天朋友遇到了利用Worker加载文件出现安全沙箱的问题。我自己写例子测试了一下，问题的确存在。而且尝试了各种方法后依然未能解决。这可能是FlashPlayer本身的机制所导致的问题。

#### 问题
利用worker加载并解析文件，在FlashBuilder的调试环境下，加载本地文件会出现安全沙箱错误，提示远程SWF无法加载本地文件。但放到网络环境下就不会出现这个问题。

*workerTest.as*

{% highlight as3 %}
package
{
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.system.LoaderContext;
	import flash.system.MessageChannel;
	import flash.system.Security;
	import flash.system.Worker;
	import flash.system.WorkerDomain;
	import flash.utils.ByteArray;
	
	public class workerTest extends Sprite
	{
		private var _loadWorker:Worker;
		private var _mainToWorker:MessageChannel;
		private var _workerToMain:MessageChannel;
		
		public function workerTest()
		{
			trace("workerTest::::", Security.sandboxType);
			initWorker();
		}
		
		private function initWorker():void
		{
			var workBytes:ByteArray = Workers.LoadWorker;
//			_loadWorker = WorkerDomain.current.createWorker(workBytes);
//			_mainToWorker = Worker.current.createMessageChannel(_loadWorker);
//			_workerToMain = _loadWorker.createMessageChannel(Worker.current);
//			
//			_loadWorker.setSharedProperty("mainToWorker", _mainToWorker);
//			_loadWorker.setSharedProperty("workerToMain", _workerToMain);
//			
//			_workerToMain.addEventListener(Event.CHANNEL_MESSAGE, onWorkerToMain);
//			_loadWorker.start();
//			_mainToWorker.send("../assets/bkg.jpg");
			
			var loader:Loader = new Loader();
			var context:LoaderContext = new LoaderContext();
			context.allowCodeImport = true;
			loader.loadBytes(workBytes, context);
			loader.contentLoaderInfo.addEventListener(Event.COMPLETE, onLoaderComplete);
		}
		
		protected function onLoaderComplete(event:Event):void
		{
			var loaderInfo:LoaderInfo = event.target as LoaderInfo;
			trace("onLoaderComplete");
			_loadWorker = WorkerDomain.current.createWorker(loaderInfo.bytes);
			_mainToWorker = Worker.current.createMessageChannel(_loadWorker);
			_workerToMain = _loadWorker.createMessageChannel(Worker.current);
			
			_loadWorker.setSharedProperty("mainToWorker", _mainToWorker);
			_loadWorker.setSharedProperty("workerToMain", _workerToMain);
			
			_workerToMain.addEventListener(Event.CHANNEL_MESSAGE, onWorkerToMain);
			_loadWorker.start();
//			_mainToWorker.send("../assets/bkg.jpg");
		}
		
		private function onWorkerToMain(e:Event):void
		{
			trace("workerTest.onWorkerToMain(e)");
		}
	}
}
{% endhighlight %}

*LoadWorker.as*

{% highlight as3 %}
package
{
	import flash.display.Loader;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.net.URLRequest;
	import flash.system.MessageChannel;
	import flash.system.Security;
	import flash.system.SecurityDomain;
	import flash.system.Worker;
	
	public class LoadWorker extends Sprite
	{
		private var _mainToWorker:MessageChannel;
		private var _workerToMain:MessageChannel;
		
		public function LoadWorker()
		{
			super();
			trace("LoadWorker:::", Security.sandboxType);
			if(!Worker.current.isPrimordial)
			{
				_mainToWorker = Worker.current.getSharedProperty("mainToWorker");
				_workerToMain = Worker.current.getSharedProperty("workerToMain");
				_mainToWorker.addEventListener(Event.CHANNEL_MESSAGE, onMainToWorker);
			}
		}
		
		private function onMainToWorker(event:Event):void
		{
			var url:String = _mainToWorker.receive()
			var urlReq:URLRequest = new URLRequest(url);
			var loader:Loader = new Loader();
			loader.contentLoaderInfo.addEventListener(Event.COMPLETE, onComplete);
			loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, onIOError);
			loader.load(urlReq);
		}
		
		private function onIOError(e:IOErrorEvent):void
		{
			trace(e);
		}
		
		private function onComplete(e:Event):void
		{
			trace("LoadWorker.onComplete(e)");
		}
	}
}

{% endhighlight %}

按照上面的代码执行后可以得到：

{% highlight as3 %}
workerTest:::: localTrusted
LoadWorker::: localTrusted
onLoaderComplete
LoadWorker::: remote
{% endhighlight %}

可以看到就算用loader把worker再加载一遍，当创建Worker的时候，Worker对应的swf安全沙箱依然为*remote*

#### 解决
如果哪位网友知道如何解决这个问题，希望能留言告诉我。

参考：

> [安全沙箱](http://help.adobe.com/zh_CN/as3/dev/WS5b3ccc516d4fbf351e63e3d118a9b90204-7e3f.html)

> [FLEX Workers unable to load local files](https://forums.adobe.com/message/5127263#5127263)
