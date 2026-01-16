import platform
import re
import smtplib
import subprocess
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 导入配置
from config import *

# 登录校园网
def login_campus_network():
    driver = None
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(LOGIN_URL)

            # 检查是否已经登录
            try:
                already_logged_in = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'toLogOut'))
                )
                print("已经登录校园网，跳过登录步骤。")
                return 2
            except Exception:
                print("未检测到登录状态，继续执行登录。")

            # 登录流程
            try:
                username_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'username'))
                )
                username_input.send_keys(CAMPUS_USERNAME)
                pwd_tip = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'pwd_tip'))
                )
                pwd_tip.click()
                password_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'pwd'))
                )
                password_input.send_keys(CAMPUS_PASSWORD)
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'loginLink_div'))
                )
                login_button.click()
                time.sleep(5)
                print("校园网登录成功")
                return 1
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

        time.sleep(5)

    print("达到最大尝试次数，登录失败。")

# 获取本地网络接口的IP地址
def get_internal_ip():
    try:
        system = platform.system().lower()
        if system == 'windows':
            result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, text=True, encoding='gbk')
            output = result.stdout
            # 在Windows下查找IPv4地址
            ip_matches = re.findall(r'IPv4.*?(\d+\.\d+\.\d+\.\d+)', output)
            internal_ips = [ip for ip in ip_matches if not ip.startswith('127.')]
        else:  # Linux系统
            result = subprocess.run(['ip', 'addr', 'show'], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            # 在Linux下查找IPv4地址
            ip_matches = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)/', output)
            internal_ips = [ip for ip in ip_matches if not ip.startswith('127.')]

        return internal_ips[0] if internal_ips else "未找到有效的内网IP"
    except Exception as e:
        return f"获取内网IP时出错: {e}"

# 发送邮件的设置
def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print("邮件发送成功")
        server.quit()
    except smtplib.SMTPException as e:
        print(f"邮件发送失败 (SMTP 错误): {e}")
    except Exception as e:
        print(f"邮件发送失败 (其他错误): {e}")

# 执行校园网登录
print("尝试登录校园网...")
status = login_campus_network()
if status == 1 or (status == 2 and random.randint(1, 10) <= 2):

    # 获取内网IP地址
    internal_ip = get_internal_ip()
    print(f"内网IP: {internal_ip}")

    # 准备邮件内容
    subject = "当前校园网 IP 地址"
    body = f"当前的内网 IP 地址是: {internal_ip}"

    # 发送邮件
    send_email(subject, body, EMAIL_RECEIVER)