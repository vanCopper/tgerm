---
title: Node.js 接入微信公众号平台
tag: [Node.js, 服务器]
layout: post
---
<span style="color: #ff6600;"><strong>原创博文，转载请声明</strong></span>

先看最终演示的结果：

![image](../../images/wp-content/uploads/2014/03/screenshot.jpg)

实现了简单的文本回复。lipi觉得这篇Blog会是篇水文，所以。。。（请参考截图）

1.公众号的申请不复杂，而且很快就能通过审核。通过审核后到后台开启开发者模式，在服务器配置上填上你的接口地址和Token.

2.配置好以后微信平台需要验证你的接口是否可用，按照消息规则返回消息就可以验证通过了

3.接下来就可以进行消息（文本消息，图片消息，位置消息）的处理了。这里只处理了文本消息，接收并自动回复。

<pre class="brush:js">/**
 * Created by vancopper on 14-2-18.
 */
var http = require('http');
var url = require('url');
var sha1 = require('sha1');
var xml2js = require('xml2js');
var token = '你的token';


http.createServer(onCreateServer).listen(端口, 'ip');


function onCreateServer(req, res)
{
    if(checkSignature(req))
    {
//        console.log('Signature OK')
        if(req.method == 'POST')
        {
            parsePostData(req, res);
        }
//        res.end('onCreateServer');
    }else
    {
        console.log('Signature FAILURE');
        res.end('error')
    }

}

function checkSignature(req)
{
    var gURL = url.parse(req.url, true);
    // 获取校验参数
    var signature = gURL.query.signature;
    var timestamp = gURL.query.timestamp;
    var nonce = gURL.query.nonce;
    var echostr = gURL.query.echostr;

    // 按照字典排序
    var array = [token, timestamp, nonce];
    array.sort();


    var str = sha1(array.join(""));

    // 对比签名
    if(str == signature)
    {
        return true;
    } else {
        return false;
    }
}

function parsePostData(req, res)
{
    req.setEncoding("utf8");
    var postStr = '';
    req.addListener('data', function(postDataChunk)
    {
        postStr += postDataChunk;
    })

    req.addListener('end', function()
    {
        xml2js.parseString(postStr, function(error, json)
        {
            if(error)
            {
                //TODO;
            }else
            {
               // console.log(json.xml.MsgType[0], json.xml.Content[0]);
               this.parseData = json.xml;
               parse(res);
            }
        })
    })
}

function parse(res)
{
    var msgType = this.parseData.MsgType[0] ? this.parseData.MsgType[0] : 'text';
    switch(msgType)
    {
        case 'text':
            switch (this.parseData.Content[0])
            {
                case 'lipi':
                    sendTextMsg('二货',res)
                    break;
                default :
                    sendTextMsg('不懂~', res);
                    break;
            }
        break;
    }
}

function sendTextMsg(str, res)
{
    var time = Math.round(new Date().getTime() / 1000);

    var output = "" +
        "&lt;xml&gt;" +
        "&lt;ToUserName&gt;&lt;![CDATA[" + this.parseData.FromUserName[0] + "]]&gt;&lt;/ToUserName&gt;" +
        "&lt;FromUserName&gt;&lt;![CDATA[" + this.parseData.ToUserName[0] + "]]&gt;&lt;/FromUserName&gt;" +
        "&lt;CreateTime&gt;" + time + "&lt;/CreateTime&gt;" +
        "&lt;MsgType&gt;&lt;![CDATA[" + this.parseData.MsgType[0] + "]]&gt;&lt;/MsgType&gt;" +
        "&lt;Content&gt;&lt;![CDATA[" + str + "]]&gt;&lt;/Content&gt;&lt;/xml&gt;";

//    console.log(output);
    res.type = 'xml';
    res.method = 'GET';
    res.end(output);
}</pre>
