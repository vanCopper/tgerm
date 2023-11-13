---
layout: page
title: Integrating RenderDoc for CopperEngine
tag: 
 - CopperEngine
---

# RenderDoc In-application API

最近修改EveryRay RenderingEngine中阴影相关的实现，需要频繁使用RenderDoc来抓帧，总要先build后再用RenderDoc进行Launch后再抓帧，非常的不方便。在Unreal Engine中RenderDoc是以插件的形式集成，翻看了相关实现细节，发现原来并不复杂。RenderDoc 提供了**In-application API**，可以非常方便的集成：

> In-application API: https://renderdoc.org/docs/in_application_api.html

## Step 1:

加载**renderdoc.dll**并获取API指针，API的版本可根据你本机版本来设置：

```c++
RENDERDOC_API_1_0_0* GetRenderDocApi() 
{ 
    RENDERDOC_API_1_0_0* rdoc = nullptr; 
    HMODULE module = GetModuleHandleA("renderdoc.dll"); 

    if (module == NULL) 
    { 
        // 这里我把dll放在项目文件夹了，如果没有在当前进程中找到RenderDoc就直接加载。
        std::string renderdocPath = GetFilePath("external\\Renderdoc\\lib\\renderdoc.dll");
        mRenderDocDLL = LoadLibraryA(renderdocPath.c_str());
        return nullptr; 
    } 

    pRENDERDOC_GetAPI getApi = nullptr;
    getApi = (pRENDERDOC_GetAPI)GetProcAddress(module, "RENDERDOC_GetAPI"); 

    if (getApi == nullptr) 
    {
        return nullptr;
    }
    
    if (getApi(eRENDERDOC_API_Version_1_0_0, (void**)&rdoc) != 1) 
    {
        return nullptr;
    } 
    return rdoc; 
}
```

## Step 2:

在渲染开始时调用捕获，渲染结束时调用结束捕获并加载RenderDoc UI即可：

```C++
// Start a frame capture
GetRenderDocAPI()->StartFrameCapture(nullptr, nullptr);
// Your rendering should happen here

// stop the capture
if(GetRenderDocAPI()->IsFrameCapturing())
{
    auto result = GetRenderDocAPI()->EndFrameCapture(nullptr, nullptr);
    GetRenderDocAPI()->LaunchReplayUI(1, nullptr);
}
```

# Tips:

* 必须在任何图形API调用之前加载**renderdoc.dll**，最好是在**main**函数的第一行。我就踩了这个坑，一开始我把dll的加载放在了rhi相关初始化完成以后的位置，结果一直提示：Couldn't find matching frame capturer for device ....
* 还有更多用法，如果有需要可以参考In-application API或阅读下Unreal Engine的实现。
