---
layout: page
title: Component Visualizers
tag: 
 - UnrealEngine
---

# Component Visualizers

起因是想在BlueprintEditor下对某个组件的一个Vector属性进行可视化并且支持编辑。引擎在UPROPERTY的meta中提供了MakeEditWidget的功能。如果将一个属性（支持Vector、Transform类型）设置为MakeEditWidget=true，那么引擎会自动给这个属性生成一个编辑用的小组件：

```c++
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Respawn", meta = (MakeEditWidget = true))
FTransform RespawnLocation;
```



