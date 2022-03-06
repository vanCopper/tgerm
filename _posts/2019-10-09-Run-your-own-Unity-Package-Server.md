---
layout: post
comments: true
excerpt:
tag: [U3D]
title: Run your own Unity Package Server
---



# Run your own Unity Package Server

最近项目迁移到了Git，并且把项目分成了美术和程序两个独立的仓库。两个仓库存在共用代码问题，比如项目自定义的管线，工具等。所以一开始直接在Package Manager里指定git repository的URL来实现代码共用，但版本更新不方便，每次都需要把repository打release包，然后再修改manifest.json来更新。当有多个共用repository，更新就变的异常麻烦，并且版本回退也很不方便。

Unity Package Manager是支持npm的，通过在manifest.json中使用scopedRegistries来配置Package Server和包信息，就可以通过npm来分发包了。

![](Untitled-e3687d2d-6cdc-4f07-8337-bfbe22eb9f3a.png)

# Step 1:安装配置Verdaccio （MacOS）

当然也可以不使用Verdaccio, cnpmjs也是可以的。首先要确保安装了NodeJS和npm，使用 $ nodejs -v 和 $npm -v 确认是否已经安装。

安装 verdaccio:

    $ npm install --global verdaccio

修改配置：

    $ cd verdaccio
    $ vim config.yaml

> listen:
>
>   - 0.0.0.0:4873

启动服务：

    $ verdaccio

![](../../images/Untitled-0462fea6-cdcf-4aff-908f-b46486b6b2a4.png)

访问本机IP既可通过web端查看Package信息：

![](../../images/Untitled-9c3cb276-41b7-4e76-bfe4-31c68a324b45.png)

# Step 2: 添加用户

    $ npm adduser --registry http://192.168.6.53:4837

根据提示输入用户名，密码即可。设置完成后，可以通过以下命令来登陆：

    $ npm login --registry http://192.168.6.53:4837

# Step 3: 创建并上传Pacakges

1. 创建package.json,设置包的一些信息。这里需要注意的是 name 字段后面是需要跟scopedRegistries里的scopes做匹配的。

    ```json
    {
      "name": "com.tgerm.srp",
      "displayName": "Your Package's Name",
      "version": "1.0.1",
      "unity": "2019.1.4f",
      "description": "The description of your package",
      "keywords": [ "package", "unity", "yeah" ],
      "dependencies": {}
    }
    ```

2. 创建 assembly definition files 

   参考：[Assembly Definitions in Unity](https://medium.com/@markushofer/assembly-definitions-in-unity-cec6a6aa98af)

3. Publish  

    ```bash
    $ npm publish --registry http://192.168.6.53:4837
    ```

![](../../images/Untitled-29342631-949b-4c12-925d-91da5146ba2b.png)

现在包已经被成功推送到本地服务器了。

![](../../images/Untitled-b273bf76-ff86-4b60-9ca9-d384721498d0.png)

更新包只需在package.json中修改version并重新publish即可：

```json
{
  "name": "com.tgerm.srp",
  "displayName": "Your Package's Name",
  "version": "1.0.2",
  "unity": "2019.1.4f",
  "description": "The description of your package",
  "keywords": [ "package", "unity", "yeah" ],
  "dependencies": {}
}
```

publish完成后，就可以在Unity Package Manager中看到新版本了：

![](../../images/Untitled-fd055843-b159-4e84-bc3f-e5b55c83c36d.png)

# Step 4: 配置 Package/mainfest.json

```json
"scopedRegistries": [
    {
      "name": "srp",
      "url": "http://192.168.6.53:4873/",
      "scopes": [
        "com.tgerm"
      ]
    }
  ]
```

关于scopedRegistries的配置可参考Unity官方文档 [Scoped package registries](https://docs.unity3d.com/Manual/upm-scoped.html)

# Tips:

1. 移除包

    ```bash
    $ npm unpublish --force com.tgerm.srp --registry http://192.168.6.53:4873
    ```

2. 移除 Uplinks

    uplinks是当前服务器没有搜索到对应的包就会去uplinks指定的服务器去下载包，但因为我们都是私有的仓库，所以就没必要用这个东西，去掉就好了。

![](../../images/Untitled-254751bd-6e87-4fc0-b504-77a898ba1989.png)

