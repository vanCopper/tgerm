---
layout: page
title: TriggerX Notes
tag: 
 - UnrealEngine
---

#  移除StarterContent

把项目里的StarterContent删除后，每次开项目StarterContent资源又会被重新导入。发现在DefaultGame.ini中配置了InsertPack，把相关配置移除即可：

```ini
;[StartupActions]
;bAddPacks=True
;InsertPack=(PackSource="StarterContent.upack,PackName="StarterContent")
```

