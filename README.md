# Suicide-Squad
Let's make the history together.

## Strategies
### 1. Let Drone flying by programming control
* UP slowly
* Stay at a certain altitude stably, say 100cm
* Down slowly

### 2. Try to use OpenMV to find black_lines
* Let drone stay at 100cm, then take pictures.
* Move camera up to 125cm. Then drone goes straight until he meets a vertical black line at the center of the camera. 
* Camera rotates with a fixed degree from 0 to x. During this, the camera needs to know when a vertical black line disappears and a new black line appears. Save that x degree, then let drone rotates by x degree. Reset the camera to 0 degrees. Then let the drone go straight until he meets another vertical black line.
* Let the drone Go back with the old path (You have to record data, then reverse your data for doing this).
* Down slowly until the drone reaches the ground.

### 3. Try to recognize color_blobs
* During the flying between black_LineA and black_LineB, if camera finds any color blob, stay at there for 3 seconds.
* During the flying between black_LineA and black_LineB, if camera finds any color blob, light up the LED with related color.
* Try to calculate the distance between black_LineA and color_blob.

### 4. Wireless communication
* Use `TTL(tx, rx)` technology to send distance infomation to Showing_Device. I'll use `Pyborad + OpenSmart LCD(UART version)`.

### 5. Test
* Do whatever you can to make it stable.

## Time Table
### Task1: 前期准备，分配任务，准备场地

9月29日: 
* yingshaoxo: 完成 time table.
* 孙雅斌: 购买比赛用品，飞机、TTL收发USB等
* 刘露: 学习如何使用 github，方便后期更新此表.

9月30日: 
* yingshaoxo: 用 Pyboard(OpenMV) 控制 LCD，利于调试，实现按比赛要求`显示对应信息到显示屏`
* 孙雅斌: 购买搭场地所需物品。(两根黑杆，中间一条黑线，线上一个有颜色的物体)
* 刘露: 熟悉 OpenMV (Pyboard) | 未完成

10月1日: 
* yingshaoxo: 用 Pyboard(OpenMV) 写出一套可靠的 UART 数据传输协议，用来传输`故障点距离`到`笔记本电脑`，笔记本电脑再显示对应信息 | 完成了一半
* 孙雅斌: 购买搭场地所需物品。(两根黑杆，中间一条黑线，线上一个有颜色的物体)
* 刘露: 熟悉 OpenMV (Pyboard) | 未完成

___

### Task2: 摄像头寻黑线，找到垂直、水平的两根线; 另一个人用程序测算`从起点 到 色块 之间的距离`（假设速度恒定）

10月2日: 
* yingshaoxo: 写出了一套稳定的 UART 传输协议(支持大文件，支持json) ; 
* 孙雅斌: 无
* 刘露: 学习`霍夫变换`，尤其是`利用 最小二乘法 和 霍夫变换 拟合、寻找直线`的方法。要求能够用通俗易懂的语言将其解释清楚。

10月3日: 
* yingshaoxo: 写出了寻找 vertical and horizontal black line 的 function
* 孙雅斌: 把 OpenMV3 退了货， 因为我们需要 OpenMV4
* 刘露: 把店家给的所有飞行器资源下载到本地，方便学习

10月4日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task3: 利用OpenMV测算`第2根杆 与 第3根杆 的夹角度数`

10月5日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月6日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月7日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task4: 让无人机飞起来，先手动遥控，后编程控制。要求能不使用GPS，用超声波`定高旋停`。最后还得让无人机缓慢地降落

10月8日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月9日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月10日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task5: 通过`AirSim模拟器`学习如何让无人机在原地旋转指定的度数。

10月11日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月12日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月13日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task6: 通过`AirSim模拟器`学习如何让无人机向各个方向`飞行指定的距离`。

10月14日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月15日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月16日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task7: 让`实体无人机`在现实中向指定角度飞行指定的距离

10月17日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月18日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月19日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task8: 整合代码，按照 Strategies 写流程

10月20日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月21日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月22日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

___

### Task9: 稳定性测试

10月23日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月24日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

10月25日: 
* yingshaoxo: 
* 孙雅斌: 
* 刘露: 

## About 
author: 
* yingshaoxo(胡英杰) | 铁道通信1702

school: 南京铁道职业技术学院

> 参加本次比赛没有酬劳，和学校也没有雇佣劳动关系。同时，所有的代码，都是基于开源社区的工作成果，我所作的不过是把它们聚合起来。所以我认为代码可以在`比赛结束后`开源。
