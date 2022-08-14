<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">
<h1 align="center">🔥 nonebot_plugin_bfinfo</h1>


✨ 战地1、5战绩查询 ✨

</div>

<p align="center">
  <a href="https://github.com/GC-ZF/nonebot_plugin_bfinfo/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/GC-ZF/nonebot_plugin_bfinfo" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_bfinfo">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_bfinfo" alt="pypi">
  </a>
  <img  src="https://visitor-badge.glitch.me/badge?page_id=nonebot_plugin_bfinfo" />
  <img src="https://img.shields.io/badge/python-3.7.3+-blue" alt="python"><br />
</p></br>

## 插件描述

一款基于[Nonebot2](https://github.com/nonebot/nonebot2)的插件

调用[Stats API for the Battlefield series](https://api.gametools.network/docs)，用于QQ私聊或群聊发送战地游戏ID，返回基础信息以及最佳兵种、最佳枪械、最佳载具、最佳模式信息

由于API返回信息不全，获取的json存在一些问题，无法获取正确信息

* 战地一
  * 等级(`rank`)字段为0
  * 总治疗量(`heals`)字段为None
* 战地五
  * 总治疗量(`heals`)字段为None
  * 最佳兵种(`classes`)字段中所有数据为0
  * 最佳游戏模式(`gamemodes`)字段不存在

因为期末考试，中间隔了好久才完成，文件夹**本地测试源码**中存放了未加入nonebot框架以前的源码，可以在编译器中直接调试

* BF1_record：初步完成基本功能，输入游戏ID，绘制基础信息
* Battlefield_Test：`03数据分析.py`中实现输入游戏ID，绘制基础信息以及最佳兵种、最佳枪械、最佳载具、最佳模式信息

提供以上源码是为了方便测试，如果你有更好的解决办法，欢迎留言

API如下，将`{player_name}`替换为游戏ID即可在浏览器中查看信息

```python
https://api.gametools.network/bf1/all/?name={player_name}&lang=en-us
https://api.gametools.network/bfv/all/?name={player_name}&lang=en-us    
```

本人未系统学习过py,靠仅有的cpp和py的一点点理解制作的,如果有任何问题、建议,欢迎[issues](https://github.com/GC-ZF/nonebot_plugin_bfinfo/issues)

## 安装
```python
pip install nonebot_plugin_bfinfo
```
## 配置项
在`bot.py`中添加
```python
nonebot.load_plugin("nonebot_plugin_bfinfo")
```
## 命令

在群聊或私聊中发送`BFI+ID`，`BFV+ID`

## 示例

<div align="center">
  <img height="300px" src="https://test1.jsdelivr.net/gh/GC-ZF/nonebot_plugin_bfinfo/BFI示例图片.png">
</div>

<div align="center">
  <img height="300px" src="https://test1.jsdelivr.net/gh/GC-ZF/nonebot_plugin_bfinfo/BFV示例图片.png">
</div>

## 历史

2022.07.05 成功提交给nonebot2，第一次贡献代码，激动！

2022.07.08 修复win环境下，字体缺失，主要原因是配置了Linux的绝对路径，获取文字材质。改为直接在插件中存放**华文行楷.TTF**



欢迎小🍟入群927254485

