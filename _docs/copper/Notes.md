---
title: Notes
tag: 
 - CopperEngine
---

> CopperEngine 开发日志。记录一些零碎的知识点以及遇到的问题。

# Static library vs. Dynamic library

![image-20220504172817314](../../assets/img/StaticLibrary_vs._DynamicLibray_Compiler.png)

* Static library 静态库在编译阶段会被直接编译至目标Executable文件，也就是每个Executable文件都包含了完整的静态库代码拷贝。
* Dynamic library 动态库在编译阶段生成Symbol Table至目标Executable文件，在Executable文件运行时，在已经加载的库文件中通过Symbol Table来查找函数并执行。

![image-20220504171941850](../../assets/img/StaticLibrary_vs._DynamicLibray_Runtime.png)

使用Static Library有两个明显的缺点：

1. 应用程序的包体会变大，如果你的应用中又包含多个可执行程序，最坏的情况是同一个库在不同的可执行程序中被包含了多次。
2. 修改或升级库需要重新构建应用程序，这会增加编译以及部署成本。

# __declspec(dllexport & dllimport)

* __declspec: MS VC++中用于指定类信息的扩展属性语法: [declspec doc](https://docs.microsoft.com/en-us/cpp/cpp/declspec?view=msvc-170)

* __declspec(dllexport) 从动态库（dll）中导出函数或类。

* __declspec(dllimport) 从动态库（dll）中导入函数或类。

相对应的不同编译平台下，函数或类的导出与导入会有不同的语法，例如在Unreal Engine中对于Mac平台（GCC）中导入导出的宏就被定义为：

```c++
// DLL export and import definitions
#define DLLEXPORT			__attribute__((visibility("default")))
#define DLLIMPORT			__attribute__((visibility("default")))
```

用法：

库中声明函数：

```c
/* math_util.c */
int __declspec(dllexport) add(int a, int b)
{
    return (a + b);
}
```

使用库：

```c
int __declspec(dllimport) add(int a, int b)
```

