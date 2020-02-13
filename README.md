# BusinessCardRing
Hello, everyone!

I am Tenghui Zhang, this is my product of a business card exchange system. The purpose of this project is that people can exchange their name card by shaking their hands and the Arduino will collect the signal and upload the business card information to the cloud by Python.

If you want to see how the product works, please go to the https://youtu.be/F6YNxm4p_R4 or visit my personal website: tenghuizhang.com

以下是Python 文件一些操作的注意事项：
首先，我们需要知道本地服务器的IP：1.Arduino控制端需要根据IP、无线网来初始化；2.APP需要IP来初始化。

接下来，Arduino部分：
首先，初始化，有wifi模块的初始化（波特率为115200），蓝牙模块不需要初始化（每次使用的时候将波特率设定为9600就OK了）。LED的初始化，戒指上按键的初始化，蓝牙模块和WiFi模块的选择端口初始化（CD4052的A口连接到Arduino的输出IO口，B口接到GND），RTC的初始化（不用管）。

当RTC时间出错后，用另一个程序来设定时间：
将时间改成当前时间的下两分钟，分别上传到两块带有RTC模块的ARDUINO板，等上传完成后，等待至当前时间与设定时间一致，同时复位两个ARDUINO板，完成RTC的配置。然后需要将之前的戒指的程序重新上传至ARDUINO板。

APP：
首先确定好配对的ARDUINO模块。打开之后，先设定自己的信息，然后点击更新（需要选取配对的蓝牙），（如果收到字符‘A’，说明更新成功）。等待新的名片进入。

服务器：
监听与ARDUINO连接的端口、接受数据、对比判断（是否更新数据库）
监听与APP连接的端口、接受请求，若有数据，则发送
