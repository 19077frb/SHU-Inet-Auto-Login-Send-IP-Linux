## 功能
本脚本用于自动化登录SHU校园网并获取当前的内网IP地址，通过电子邮件发送给指定的收件人。

## 目的
- 自动化登录校园网，减少手动操作。
- 获取校园网内网IP地址，应对IP地址变化。
- 通过电子邮件通知用户当前的内网IP地址，以便远程连接。

## 环境要求
- Python环境（建议使用Python 3.x版本）。
- Selenium库，用于自动化Web浏览器操作。
- Chrome浏览器及其对应的WebDriver。
- SMTP支持的电子邮件服务。

## 需要修改的代码内容
1. 用户名
```
username_input.send_keys('xxxxxxxx')  # 替换为实际用户名
```
2. 密码
```
password_input.send_keys('xxxxxxxx')  # 替换为实际密码
```
3. 发件邮箱
```
from_email = 'xxxxxxxx@xxxx.com'  # 替换为你的发件邮箱
```
4. 邮箱授权码
```
from_password = 'xxxxxxxx'  # 替换为你的邮箱授权码
```
   - 不是邮箱登录密码，而是当你启用了SMTP服务之后邮箱生成的授权码，用来代替普通密码进行邮箱的第三方应用登录。
   - 对于QQ邮箱，可以按照以下步骤获取授权码：
     - 登录 [QQ邮箱](https://mail.qq.com/)
     - 进入 **设置** → **账户** → 启用 **SMTP服务**
     - 完成手机验证后，系统会生成一个授权码，**复制并粘贴到该字段**。

5. 邮箱SMTP
```
server = smtplib.SMTP_SSL('smtp.xxxxx', xxxx)  # 使用 SSL 连接 邮箱 SMTP
```
   - 需要替换为你的邮箱的**SMTP服务器地址**和**端口号**。  
   - 如果你使用QQ邮箱：
     - SMTP服务器地址是：`smtp.qq.com`
     - 端口号是：`465`（使用SSL连接）
     对于其他邮箱服务提供商，SMTP服务器和端口号可以参考邮箱服务的帮助文档。例如：
  - **Gmail**: `smtp.gmail.com`, 端口：`465`
  - **Outlook**: `smtp.office365.com`, 端口：`587`
6. 收件人邮箱
```
send_email(subject, body, 'xxxxxxxx@xxxx.com')  # 替换为实际的收件人邮箱
```
## 使用方法
### 1. 普通运行
1. 编辑脚本中的用户名、密码以及邮箱信息，确保信息正确无误。
2. 在终端或命令提示符中运行脚本：
   ```
   python main.py
   ```
### 2. 设置脚本开机自启动（Windows任务计划程序）
1. 打开 **Windows 任务计划程序**。
2. 点击 **“创建基本任务”**，按照向导填写名称和描述。
3. 在 **触发器** 选项中，选择 **“开机时”** 或自定义定时运行。
4. 在 **操作** 选项中，选择 **“启动程序”**，并选择你的Python解释器和脚本路径。例如：
   - 程序/脚本：`C:\path\to\python.exe`
   - 添加参数：`C:\path\to\main.py`
5. 点击 **“完成”** 保存任务。
