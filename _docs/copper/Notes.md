---
title: Notes
tag: CopperEngine
---

> CopperEngine 开发日志。记录一些零碎的知识点以及遇到的问题。

### Static library vs. Dynamic library

![image-20220504172817314](../../assets/img/StaticLibrary_vs._DynamicLibray_Compiler.png)

* Static library 静态库在编译阶段会被直接编译至目标Executable文件，也就是每个Executable文件都包含了完整的静态库代码拷贝。
* Dynamic library 动态库在编译阶段生成Symbol Table至目标Executable文件，在Executable文件运行时，在已经加载的库文件中通过Symbol Table来查找函数并执行。

![image-20220504171941850](../../assets/img/StaticLibrary_vs._DynamicLibray_Runtime.png)

使用Static Library有两个明显的缺点：

1. 应用程序的包体会变大，如果你的应用中又包含多个可执行程序，最坏的情况是同一个库在不同的可执行程序中被包含了多次。
2. 修改或升级库需要重新构建应用程序，这会增加编译以及部署成本。

