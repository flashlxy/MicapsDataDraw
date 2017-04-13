

    利用配置文件config.xml定制参数，结合micaps具体数据，
    
    可实现一种或多种类型（in the future）的micaps数据的叠加绘制

    并自动输出相应图像到指定文件。
    
###### Author：Xianyao Liu | Version：2.0.20170411 | E-mail：flashlxy@qq.com | Language：Python2.7
###### 
****

### 主要功能

#### 1、支持Micaps第3、4、11类数据的绘制

    目前实现了某类数据的单独绘制，多类数据叠加在不久的将来实现。

#### 2、支持多种投影

    sall：无投影，lcc:兰波托投影，mill，ortho，stere：极射赤面投影，

    npstere：北半球极射赤面投影, 
    
    hammer，kav7，merc：麦卡托投影，gnom, cyl：等经纬度投影。

#### 3、支持底图叠加

    用一个或多个shp格式或者定制的txt文件叠加到底图。
    
#### 4、支持任意区域完美白化

    用shp或者定制的txt文件所形成的单个或多个闭合区域切图，也就是所谓的白化。
    
#### 5、支持灵活配置色标

    可以自己定义色标，同时支持
[NCL色标](http://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml)

#### 6、高度可定制化

    包括但不限于标题内容、样式、位置；色标选择、位置、放置方式；

    色版图、等值线、标注、格点着色的显隐等都实现了高度自定义。

### 程序运行

    python main.py config.xml

### 项目参考的代码及的用到的一些库

#### 代码[完美白化](http://bbs.06climate.com/forum.php?mod=viewthread&tid=42437)

    气象家园帖子作者的片段代码
   
#### 第三方库[nclcmaps](http://bbs.06climate.com/forum.php?mod=viewthread&tid=43521)

    作者的一个支持NCL colorbar的python库。
    
    matplotlib，basemap，numpy，scipy，shapefile，nclcmaps
    
    欢迎大家star和fork，一并感谢2位作者！


    Micaps第四类数据ortho投影：
    
![](https://github.com/flashlxy/MicapsDataDraw/raw/master/images/3.png)

    Micaps第四类 数据无投影：

![](https://github.com/flashlxy/MicapsDataDraw/raw/master/images/2.png)

    Micaps第四类 数据Lambert投影：

![](https://github.com/flashlxy/MicapsDataDraw/raw/master/images/1.png)

    Micaps第三类数据-等经纬度投影：

![](https://github.com/flashlxy/MicapsDataDraw/raw/master/images/4.png)

##### ![](https://github.com/flashlxy/MicapsDataDraw/raw/master/jxlogo.png) 
   
   
   
