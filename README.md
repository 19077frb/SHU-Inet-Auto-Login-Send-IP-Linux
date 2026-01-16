## 功能

本脚本用于自动化登录SHU校园网并获取当前的内网IP地址，通过电子邮件发送给指定的收件人。

## 目的

- 自动化登录校园网，减少手动操作。
- 获取校园网内网IP地址，应对IP地址变化。
- 通过电子邮件通知用户当前的内网IP地址，以便远程连接。

## 环境要求

- Python环境（建议使用Python 3.x版本）。
- ```
  pip install selenium wakeonlan
  ```
- Chrome浏览器及其对应的WebDriver。
- SMTP支持的电子邮件服务。

## 配置说明

1. 复制 `config.example.py` 文件并重命名为 `config.py`
2. 在 `config.py` 中修改以下配置项：

### 校园网登录配置

```python
CAMPUS_USERNAME = 'your_username'  # 替换为实际用户名
CAMPUS_PASSWORD = 'your_password'  # 替换为实际密码
```

### 邮件配置

```python
EMAIL_SENDER = 'your_email@qq.com'      # 替换为你的发件邮箱
EMAIL_PASSWORD = 'your_email_auth_code'  # 替换为你的邮箱授权码
EMAIL_RECEIVER = 'receiver@example.com'  # 替换为实际的收件人邮箱
EMAIL_SMTP_SERVER = 'smtp.qq.com'       # SMTP服务器地址
EMAIL_SMTP_PORT = 465                    # SMTP端口
```

注意：

- 邮箱授权码不是邮箱登录密码，而是当你启用了SMTP服务之后邮箱生成的授权码，用来代替普通密码进行邮箱的第三方应用登录。
- 对于QQ邮箱，可以按照以下步骤获取授权码：
  - 登录 [QQ邮箱](https://mail.qq.com/)
  - 进入 **设置** → **账户** → 启用 **SMTP服务**
  - 完成手机验证后，系统会生成一个授权码，**复制并粘贴到该字段**。

对于其他邮箱服务提供商，SMTP服务器和端口号可以参考邮箱服务的帮助文档。例如：

- **Gmail**: `smtp.gmail.com`, 端口：`465`
- **Outlook**: `smtp.office365.com`, 端口：`587`

## 使用方法

### 1. 普通运行

1. 按照上述说明配置 `config.py` 文件，确保信息正确无误。
2. 在终端或命令提示符中运行脚本：
   ```
   python main.py
   ```

### 2. 设置脚本开机自启动（Windows任务计划程序）

1. 打开 **Windows 任务计划程序**。
2. 点击 **"创建基本任务"**，按照向导填写名称和描述。
3. 在 **触发器** 选项中，选择 **"开机时"** 或自定义定时运行。
4. 在 **操作** 选项中，选择 **"启动程序"**，并选择你的Python解释器和脚本路径。例如：
   - 程序/脚本：`C:\path\to\python.exe`
   - 添加参数：`C:\path\to\main.py`
5. 点击 **"完成"** 保存任务。

### 3. 设置脚本开机自启动（Linux Crontab）

1. 确保脚本具有执行权限：

   ```bash
   chmod +x /path/to/main.py
   ```
2. 打开 crontab 编辑器：

   ```bash
   crontab -e
   ```
3. 添加以下内容：

   ```bash
   @reboot sleep 60 && cd /path/to/script/directory && /usr/bin/python3 main.py
   ```

   说明：

   - `@reboot`: 表示在系统启动时执行
   - `sleep 60`: 延迟60秒执行，确保网络服务已经启动
   - `cd /path/to/script/directory`: 切换到脚本所在目录
   - `/usr/bin/python3`: 使用完整的 Python 路径（可以通过 `which python3` 命令查看）
4. 保存并退出编辑器：

   - 如果使用 nano 编辑器：按 `Ctrl + X`，然后按 `Y` 确认保存，最后按 `Enter`
   - 如果使用 vim 编辑器：按 `Esc`，输入 `:wq`，然后按 `Enter`
5. 验证 crontab 是否设置成功：

   ```bash
   crontab -l
   ```

注意事项：

- 请将路径替换为你实际的脚本路径
- 确保 Python 和所需库在系统级别已安装
- 如果遇到权限问题，可能需要使用 `sudo` 运行命令
- 建议在 crontab 中使用绝对路径
- 可以通过查看系统日志来排查问题：
  ```bash
  tail -f /var/log/syslog    # Ubuntu/Debian
  tail -f /var/log/messages  # CentOS/RHEL
  ```
