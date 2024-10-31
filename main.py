from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import re

# 登录校园网
def login_campus_network():
    driver = None
    max_attempts = 5  # 最大尝试次数
    attempts = 0

    while attempts < max_attempts:
        try:
            driver = webdriver.Chrome()
            driver.get('http://10.10.9.9/')

            # 检查是否已经登录
            try:
                already_logged_in = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'toLogOut'))
                )
                print("已经登录校园网，跳过登录步骤。")
                return
            except Exception:
                print("未检测到登录状态，继续执行登录。")

            # 登录流程
            try:
                username_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'username'))
                )
                username_input.send_keys('xxxxxxxx')

                pwd_tip = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'pwd_tip'))
                )
                pwd_tip.click()

                password_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'pwd'))
                )
                password_input.send_keys('xxxxxxxx')

                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'loginLink_div'))
                )
                login_button.click()

                # 确保页面登录完成
                time.sleep(5)
                print("校园网登录成功")
                return
            except Exception as e:
                print(f"登录过程中发生错误: {e}")
                attempts += 1
                print(f"尝试次数: {attempts}/{max_attempts}")

        except Exception as e:
            print(f"校园网连接或其他错误: {e}")
            attempts += 1
            print(f"尝试次数: {attempts}/{max_attempts}")

        finally:
            if driver:
                driver.quit()

        time.sleep(5)  # 等待一段时间后再尝试

    print("达到最大尝试次数，登录失败。")

# 获取本地网络接口的IP地址
def get_internal_ip():
    try:
        result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE)
        output = result.stdout.decode('gbk')
        ip_match = re.findall(r'IPv4 地址[^\d]*(\d+\.\d+\.\d+\.\d+)', output)
        internal_ips = [ip for ip in ip_match if not ip.startswith('127.')]
        return internal_ips[0] if internal_ips else "未找到有效的内网IP"
    except Exception as e:
        return f"获取内网IP时出错: {e}"

# 发送邮件的设置
def send_email(subject, body, to_email):
    from_email = 'xxxxxxxx@xxxxxxxx.com'
    from_password = 'xxxxxxxx'
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('xxxxxxxx', xxxxxxxx)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print("邮件发送成功")
        server.quit()
    except smtplib.SMTPException as e:
        print(f"邮件发送失败 (SMTP 错误): {e}")
    except Exception as e:
        print(f"邮件发送失败 (其他错误): {e}")

# 执行校园网登录
print("尝试登录校园网...")
login_campus_network()

# 获取内网IP地址
internal_ip = get_internal_ip()
print(f"内网IP: {internal_ip}")

# 准备邮件内容
subject = "当前校园网 IP 地址"
body = f"当前的内网 IP 地址是: {internal_ip}"

# 发送邮件
send_email(subject, body, 'xxxxxxxx@xxxxxxxx')
