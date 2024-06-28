# Mac-app
This project shows how to use pyqt5 to develop an application that can run on an M-csilicon.\
本项目展示了如何利用pyqt5开发一款可以在M硅片上运行的应用。

The **onnx** file can be found in this link: https://pan.baidu.com/s/1mUOyc26TpwR5BHwhF4jq7Q, and the password: 1111.
**onnx**可以通过以下链接获取https://pan.baidu.com/s/1mUOyc26TpwR5BHwhF4jq7Q, 密码: 1111.

## Environment Configurations 环境配置
```bash
pip install PyQt5
pip install pyinstaller
pip install ultralytics
```
PyQT5 is mainly used to generate GUI interface.\
PyQT5主要用于生成GUI界面。

pyinstaller is mainly used to package into MacOS can be used Application file.\
pyinstaller主要用于封装成MacOS可以用的Application文件。

ultralytics was applied mainly because our project is a YOLO v8 based detection program. The trained weights (.pt files) need to be converted to (.onnx files).\
ultralytics被应用主要是因为我们的项目是一个基于YOLO v8的检测项目。训练好的权重（.pt文件）需要被转换为（.onnx文件）

## Application Icons 应用图标
Mac中的图标格式为.icns，因此我们需要首先制作一个文件。

1、First select a 1024*1024 resolution image (to be used as an icon) and name it **icon.png**.\
首先选定一个1024*1024分辨率的图像（用作图标），命名为**icon.png**；

2、Create a folder **icons.iconset** and place **icon.png** in the same directory as that folder.\
创建一个**icons.iconset**的文件夹，将**icon.png**与该文件夹放置在同一目录下；\
![image](https://github.com/yingchaoAo/Mac-app/assets/145567458/df280304-1ba7-444c-85c4-9f99451ea205)

3、Open this directory in a Mac terminal and run the following command.\
在Mac终端中打开这个目录,并运行以下命令;
```bash
sips -z 16 16     pic.png --out tmp.iconset/icon_16x16.png
sips -z 32 32     pic.png --out tmp.iconset/icon_16x16@2x.png
sips -z 32 32     pic.png --out tmp.iconset/icon_32x32.png
sips -z 64 64     pic.png --out tmp.iconset/icon_32x32@2x.png
sips -z 128 128   pic.png --out tmp.iconset/icon_128x128.png
sips -z 256 256   pic.png --out tmp.iconset/icon_128x128@2x.png
sips -z 256 256   pic.png --out tmp.iconset/icon_256x256.png
sips -z 512 512   pic.png --out tmp.iconset/icon_256x256@2x.png
sips -z 512 512   pic.png --out tmp.iconset/icon_512x512.png
sips -z 1024 1024   pic.png --out tmp.iconset/icon_512x512@2x.png
```
4、It can be noticed that 10 images are generated in **icons.iconset**; \
可以发现在**icons.iconset**中会生成10张图像;

5、Run the following command to get the **.icns** file in the same directory;\
运行以下命令，就可以同目录中得到.icns文件;
```bash
 iconutil -c icns icons.iconset -o icon.icns
```

## Packaging as an app file  包装为app文件
```bash
pyinstaller --windowed --onefile --add-data "/Volumes/2T/Code/QT/best.onnx:." --hidden-import PyQt5.sip --icon=icon.icns --target-architecture arm64 --collect-all ultralytics demo.py
```

This command creates a macOS application for the ARM64 architecture, including all necessary dependencies and data files, and packages it into a single executable.\
这条命令将创建一个针对 ARM64 架构的 macOS 应用程序,包含所有必要的依赖项和数据文件,并将其打包成一个单独的可执行文件。

--windowed\
&emsp;&emsp; Creates a GUI application without a console window.\
&emsp;&emsp; 创建一个没有控制台窗口的图形界面应用程序。

--onefile\
&emsp;&emsp; Packages everything into a single executable file.\
&emsp;&emsp; 将所有内容打包into一个单独的可执行文件。

--add-data "/Volumes/2T/Code/QT/best.onnx:."\
&emsp;&emsp; Adds external files or folders to the bundle. Here, it's adding the "best.onnx" file to the root of the bundle.\
&emsp;&emsp; 将外部文件或文件夹添加到打包中。这里是将"best.onnx"文件添加到打包的根目录。

--hidden-import PyQt5.sip\
&emsp;&emsp; Includes a module that PyInstaller might not detect automatically.\
&emsp;&emsp; 包含一个 PyInstaller 可能无法自动检测到的模块。

--icon=icon.icns\
&emsp;&emsp; Specifies the icon file for the application (macOS format).\
&emsp;&emsp; 指定应用程序的图标文件（macOS 格式）。

--target-architecture arm64\
&emsp;&emsp; Specifies the target architecture for the build, here it's for Apple Silicon Macs.\
&emsp;&emsp; 指定构建的目标架构,这里是针对 Apple Silicon Mac。

-collect-all ultralytics\
&emsp;&emsp; Collects all packages, submodules, and data files from the ultralytics library.\
&emsp;&emsp; 收集 ultralytics 库的所有包、子模块和数据文件。

demo.py\
&emsp;&emsp; he main Python script of your application.\
&emsp;&emsp; 你的应用程序的主 Python 脚本。

## Usage 使用
In the **dist** folder, you can find the generated "**.app**" file, double-click to open and use!\
在**dist**文件夹下，可以找到生成的"**.app**"文件，双击即可打开使用!


