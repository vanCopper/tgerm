---
layout: page
title: Component Visualizers
tag: 
 - UnrealEngine
---

# Component Visualizers

起因是想在BlueprintEditor下对某个组件的一个Vector属性进行可视化并且支持编辑。引擎在UPROPERTY的meta中提供了MakeEditWidget的功能。如果将一个属性（支持Vector、Transform类型）设置为MakeEditWidget=true，那么引擎会自动给这个属性生成一个编辑用的小组件：

```c++
UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (MakeEditWidget = true))
FTransform RespawnLocation;
```

![image-20230312145726522](Images/ComponentVisualizers/image-20230312145726522.png)

但通过MakeEditWidge生成的编辑组件只在LevelEditor下有效，在Blueprint Edtior下无法使用。流程上我们不可能先把BP拖放到LevelEditor然后可视化到编辑Vector，然后再把数值复制粘贴到蓝图。

**Component Visualizers**是一个将数据在Blueprint Editor下可视化的很好方式，并且支持鼠标响应，右键菜单绑定等操作。

## Setting Up

**Component Visualizers**的使用需要在Editor Module环境下，所以首先需要在项目能新建一个Editor模块。关于模块的创建以及配置可以参考官方Wiki：[Creating an Editor Module](https://unrealcommunity.wiki/creating-an-editor-module-x64nt5g3)

## Aiming Point

假设我们有一个巨型怪，怪可以被玩家使用枪械瞄准射击，并且有多个部位可瞄准（瞄准时需要有自动吸附）。也就是怪身体上存在多个可用于瞄准且吸附的Point，我们暂且定义为**Aiming Point** 。一般情况下我们可能会使用指定的骨骼来作为Aiming Point，但使用骨骼可能会导致瞄准时由于骨骼本身的运动导致吸附枪线抖动。所以我们选择在DamageComponent（ActorComponent）上配置多个Vector作为Aiming Point。

**DamageComponent**

```c++
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class UDamageComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UDamageComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FVector> AimingPoints;

protected:
	virtual void BeginPlay() override;

public:
	virtual void TickComponent(float DeltaTime, ELevelTick TickType,
	                           FActorComponentTickFunction* ThisTickFunction) override;
};
```

## Creating DamageComponent Visualization Class

接下来在EditorModule中创建DamageComponentVisualizer:

```c++
#pragma once

#include "CoreMinimal.h"
#include "ComponentVisualizer.h"

class DamageComponentVisualizer : public FComponentVisualizer
{
public:
	DamageComponentVisualizer();
	virtual ~DamageComponentVisualizer();

	virtual void OnRegister() override;
	virtual void DrawVisualization(const UActorComponent* Component, const FSceneView* View, FPrimitiveDrawInterface* PDI) override;
	virtual bool GetWidgetLocation(const FEditorViewportClient* ViewportClient, FVector& OutLocation) const override;
	virtual bool VisProxyHandleClick(FEditorViewportClient* InViewportClient, HComponentVisProxy* VisProxy, const FViewportClick& Click) override;
	virtual bool IsVisualizingArchetype() const override;
	virtual bool HandleInputDelta(FEditorViewportClient* ViewportClient, FViewport* Viewport, FVector& DeltaTranslate, FRotator& DeltalRotate, FVector& DeltaScale) override;
};
```

可以在子类中Override我们需要的可视化行为，如组件的绘制，组件的Input行为等。要使用ComponentVisualizer，首先需要将自定义的Visualizer在编辑模块启动时注册到引擎中：

```C++
void FMasteryEditorModule::StartupModule()
{
	if(GUnrealEd)
	{
		TSharedPtr<FDamageComponentVisualizer> Visualizer = MakeShareable(new FDamageComponentVisualizer);
		GUnrealEd->RegisterComponentVisualizer(UDamageComponent::StaticClass()->GetFName(),
			Visualizer);

		if(Visualizer.IsValid())
		{
			Visualizer->OnRegister();
		}
	}
}
```

完成这一步后，当我们在BlueprintEditor下选中**DamageComponent**时，引擎会使用我们注册的**FComponentVisualizer**。

由于我们需要编辑多个**FVector**类型的AimingPoint，所以我们需要在**DamgeComponentVisualizer**中分别定义要可视化的属性和当前正在编辑的AimingPoint:

```C++
private:
	FProperty* AimingPointProperty;
	int32 SelectedPointIndex;
```

初始化：

```C++
FDamageComponentVisualizer::FDamageComponentVisualizer():AimingPointProperty(nullptr),
															SelectedPointIndex(0)
{
	AimingPointProperty = FindFProperty<FProperty>(UDamageComponent::StaticClass(),
	                                               "AimingPoints");
}
```

## Hit Proxies

由于我们需要在蓝图编辑器下的View中编辑AimingPoint，所以我们需要实现自己的Hit Proxies以便能够自定AimingPoint的显示以及操作数据的修改等。

在**DamageComponentVisualizer.h**中声明：

```c++
struct HDamageComponentVisProxy : public HComponentVisProxy
{
	DECLARE_HIT_PROXY();
	HDamageComponentVisProxy(const UActorComponent* InComponent, EHitProxyPriority InPriority = HPP_Wireframe)
		: HComponentVisProxy(InComponent, InPriority)
	{}

	virtual EMouseCursor::Type GetMouseCursor() override
	{
		return EMouseCursor::Crosshairs;
	}
};

struct HInteractiveSocketProxy: public HDamageComponentVisProxy
{
	DECLARE_HIT_PROXY();

	HInteractiveSocketProxy(const UActorComponent* InComponent, int32 InKeyIndex)
		: HDamageComponentVisProxy(InComponent)
		, SocketIndex(InKeyIndex)
	{}

	int32 SocketIndex;

	virtual EMouseCursor::Type GetMouseCursor() override
	{
		return EMouseCursor::Crosshairs;
	}
};
```

在**DamageComponentVisualizer.cpp**中使用引擎内置的宏实现：

```c++
IMPLEMENT_HIT_PROXY(HDamageComponentVisProxy, HComponentVisProxy);
IMPLEMENT_HIT_PROXY(HInteractiveSocketProxy, HDamageComponentVisProxy);
```

## Drawing

在DrawVisualization函数中使用DrawWireSphere绘制出AimingPoint:

```c++
void FDamageComponentVisualizer::DrawVisualization(const UActorComponent* Component, const FSceneView* View,
	FPrimitiveDrawInterface* PDI)
{
	if(const UDamageComponent* DamageComponent = Cast<UDamageComponent>(Component))
	{
		for(int i = 0; i < DamageComponent->AimingPoints.Num(); ++i)
		{
			const FVector DamageComponentLocation = FVector::ZeroVector;
			const float DamageSphereRadius = 5.0f;
			const FColor DamageSphereColor = FColor::Red;

			PDI->SetHitProxy(new HInteractiveSocketProxy(Component, i));
			DrawWireSphere(PDI, DamageComponent->AimingPoints[i], DamageSphereColor, DamageSphereRadius, 16, SDPG_Foreground);
			PDI->SetHitProxy(nullptr);
		}
	}
}
```

![image-20230404210732507](Images/ComponentVisualizers/image-20230404210732507.png)

但这里只是绘制出了AimingPoint所在的位置，如果现在想改变AimingPoint的位置，那么只能通过Detail面板上直接修改其XYZ的值来实现。我们希望能更便捷的修改AimingPoint的位置，这就是为什么前面我们新增了HitProxies相关实现。

## Receiving Clicks

在VisProxyHandleClick函数中处理当前被选中的AimingPoint，以便在后续的编辑中提供数据：

```c++
bool FDamageComponentVisualizer::VisProxyHandleClick(FEditorViewportClient* InViewportClient,
	HComponentVisProxy* VisProxy, const FViewportClick& Click)
{
	bool bEditing = false;
	const UDamageComponent* DamageComponent = CastChecked<const UDamageComponent>(VisProxy->Component.Get());
	DamageComponentPropertyPath = FComponentPropertyPath(DamageComponent);
	
	if(VisProxy && VisProxy->Component.IsValid())
	{
		if(HInteractiveSocketProxy* SocketProxy = (HInteractiveSocketProxy*)(VisProxy))
		{
			SelectedPointIndex = SocketProxy->SocketIndex;
			bEditing = true;
		}
	}
	else
	{
		SelectedPointIndex = INDEX_NONE;
	}

	return bEditing;
}
```

1. 使用PropertyPath记录当前编辑的是哪一个DamageComponent。
2. 使用SelectedPointIndex记录当前编辑的是哪一个AimingPoint。

## Set Widget Location

当我们确定了要编辑的AimingPoint就需要在其所在位置给一编辑用的Widget并显示在其对应位置上，这时我们只需要实现GetWidgetLocation函数即可：

```c++
bool FDamageComponentVisualizer::GetWidgetLocation(const FEditorViewportClient* ViewportClient,
	FVector& OutLocation) const
{
	UDamageComponent* EditedDamageComponent = Cast<UDamageComponent>(DamageComponentPropertyPath.GetComponent());
	if(IsValid(EditedDamageComponent) && SelectedPointIndex != INDEX_NONE)
	{
			OutLocation = EditedDamageComponent->AimingPoints[SelectedPointIndex];
			return true;
	}
	return false;
}
```

另外为了能够在BlueprintEditor中编辑AimingPoint我们还需要实现IsVisualizingArchetype函数，使其使用Owner的Archetype:

```c++
bool FDamageComponentVisualizer::IsVisualizingArchetype() const
{
	UActorComponent* Component = DamageComponentPropertyPath.GetComponent();
	return (Component && Component->GetOwner() && FActorEditorUtils::IsAPreviewOrInactiveActor(Component->GetOwner()));
}
```

![image-20230404213157444](Images/ComponentVisualizers/image-20230404213157444.png)

到目前为止，当我们选中某个需要编辑的AimingPoint时，会显示Crosshair以便我们对其位置进行编辑。

## Handle Input Delta

我们还剩最后一步：只需要响应Crosshair的操作并将数据保存即可。

实现HandleInputDelta:

```c++
bool FDamageComponentVisualizer::HandleInputDelta(FEditorViewportClient* ViewportClient, FViewport* Viewport,
	FVector& DeltaTranslate, FRotator& DeltalRotate, FVector& DeltaScale)
{
	if(!DeltaTranslate.IsZero())
	{
		UDamageComponent* EditedDamageComponent = Cast<UDamageComponent>(DamageComponentPropertyPath.GetComponent());
		if(IsValid(EditedDamageComponent) && SelectedPointIndex != INDEX_NONE && SelectedPointIndex < EditedDamageComponent->AimingPoints.Num())
		{
			EditedDamageComponent->AimingPoints[SelectedPointIndex] += DeltaTranslate;
			NotifyComponentModified();
			return true;
		}
	}
	
	return false;
}
```

修改后需要通知组件：

```c++
void FDamageComponentVisualizer::NotifyComponentModified()
{
	if(DamageComponentPropertyPath.IsValid())
	{
		NotifyPropertyModified(DamageComponentPropertyPath.GetComponent(), AimingPointProperty);
	}
	
	GEditor->RedrawLevelEditingViewports(true);
}
```

