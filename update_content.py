import argparse
import tempfile
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NoteMsUploader:
    def __init__(self):
        self.driver = None
        self.args = self.parse_arguments()
    
    def parse_arguments(self):
        """解析命令行参数"""
        parser = argparse.ArgumentParser(description='跨浏览器note.ms文件上传工具')
        
        parser.add_argument(
            '--browser', 
            type=str, 
            default='chrome',
            choices=['chrome', 'edge'],
            help='选择浏览器类型: chrome 或 edge (默认: chrome)'
        )
        
        parser.add_argument(
            '--driver-path', 
            type=str, 
            help='指定浏览器驱动路径 (可选)'
        )
        
        parser.add_argument(
            '--headless', 
            action='store_true',
            help='启用无头模式 (无界面)'
        )
        
        parser.add_argument(
            '--page-name', 
            type=str, 
            default='python_auto_note',
            help='note.ms页面名称 (默认: python_auto_note)'
        )
        
        parser.add_argument(
            '--file-path', 
            type=str, 
            required=True,
            help='要上传的文本文件路径'
        )
        
        parser.add_argument(
            '--window-size', 
            type=str, 
            default='1920,1080',
            help='设置浏览器窗口大小，格式: 宽,高 (默认: 1920,1080)'
        )
        
        parser.add_argument(
            '--disable-automation', 
            action='store_true',
            default=True,
            help='禁用自动化控制提示，避免被网站检测 (默认启用)'
        )
        
        parser.add_argument(
            '--timeout', 
            type=int, 
            default=30,
            help='页面加载超时时间(秒) (默认: 30)'
        )
        
        return parser.parse_args()
    
    def setup_chrome_driver(self):
        """配置Chrome浏览器驱动"""
        chrome_options = ChromeOptions()
        
        # 基础配置
        if self.args.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        
        if self.args.window_size:
            chrome_options.add_argument(f'--window-size={self.args.window_size}')
        
        # 反自动化检测配置
        if self.args.disable_automation:
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 其他常用优化参数
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        
        # 创建驱动实例
        if self.args.driver_path:
            service = ChromeService(executable_path=self.args.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        
        # 执行隐藏webdriver属性的脚本
        if self.args.disable_automation:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def setup_edge_driver(self):
        """配置Edge浏览器驱动"""
        edge_options = EdgeOptions()
        
        # 基础配置
        if self.args.headless:
            edge_options.add_argument('--headless')
            edge_options.add_argument('--disable-gpu')
        
        if self.args.window_size:
            edge_options.add_argument(f'--window-size={self.args.window_size}')
        
        # 反自动化检测配置
        if self.args.disable_automation:
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
        
        # 其他常用优化参数
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')
        edge_options.add_argument('--disable-infobars')
        edge_options.add_argument('--disable-notifications')
        edge_options.add_argument('--ignore-certificate-errors')
        edge_options.add_argument('--ignore-ssl-errors')
        
        # 创建驱动实例
        if self.args.driver_path:
            service = EdgeService(executable_path=self.args.driver_path)
            self.driver = webdriver.Edge(service=service, options=edge_options)
        else:
            self.driver = webdriver.Edge(options=edge_options)
        
        # 执行隐藏webdriver属性的脚本
        if self.args.disable_automation:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def initialize_driver(self):
        """初始化浏览器驱动"""
        try:
            if self.args.browser.lower() == 'chrome':
                print("正在初始化 Chrome 浏览器...")
                self.setup_chrome_driver()
            elif self.args.browser.lower() == 'edge':
                print("正在初始化 Edge 浏览器...")
                self.setup_edge_driver()
            else:
                raise ValueError(f"不支持的浏览器类型: {self.args.browser}")
            
            print(f"{self.args.browser} 浏览器初始化成功!")
            # 设置页面加载超时
            self.driver.set_page_load_timeout(self.args.timeout)
            return self.driver
            
        except Exception as e:
            print(f"浏览器初始化失败: {e}")
            return None
    
    def read_file_content(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"成功读取文件，内容长度: {len(content)} 字符")
            return content
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
    
    def upload_to_note_ms(self, content, page_name):
        """上传内容到note.ms"""
        target_url = f"https://note.ms/{page_name}"
        print(f"正在打开: {target_url}")
        

        # 打开目标页面
        self.driver.get(target_url)
        
        # 等待页面加载并找到文本输入区域
        wait = WebDriverWait(self.driver, self.args.timeout)
        print("正在寻找文本输入区域...")
        
        # 根据源码，textarea的class为"content"
        textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.content")))
        
        # 先点击文本区域确保获得焦点
        textarea.click()
        time.sleep(1)
        
        # 清空现有内容
        textarea.clear()
        time.sleep(1)
        
        print("正在上传内容...")
        
        # 对于大文件，使用JavaScript直接设置值更可靠
        self.driver.execute_script("arguments[0].value = arguments[1];", textarea, content)
        
        # 触发输入事件以确保内容被保存
        self.driver.execute_script("""
            var event = new Event('input', { bubbles: true });
            arguments[0].dispatchEvent(event);
        """, textarea)
        
        # 等待内容保存
        time.sleep(3)
        
        # 验证内容是否已上传
        current_content = textarea.get_attribute('value')
        if len(current_content) == len(content):
            print("✅ 内容上传成功！")
            return target_url
        else:
            print(f"⚠️ 内容可能未完全上传，期望长度: {len(content)}，实际长度: {len(current_content)}")
            return target_url
    
    def run(self):
        """运行上传流程"""
        # 检查文件是否存在
        if not os.path.exists(self.args.file_path):
            print(f"❌ 文件不存在: {self.args.file_path}")
            return False
        
        # 读取文件内容
        content = self.read_file_content(self.args.file_path)
        if not content:
            return False
        
        # 初始化浏览器驱动
        driver = self.initialize_driver()
        if not driver:
            return False
        
        try:
            # 上传内容到note.ms
            result_url = self.upload_to_note_ms(content, self.args.page_name)
            
            if result_url:
                print(f"📝 内容已上传，访问地址: {result_url}")
                print("接收端可以通过访问此URL获取内容")
                return True
            else:
                print("上传失败，请检查网络连接或稍后重试")
                return False
                
        except Exception as e:
            print(f"❌ 运行过程中出现错误: {e}")
            return False
        finally:
            # 退出浏览器
            if self.driver:
                self.driver.quit()
                print("浏览器已关闭")


def main():
    """主函数"""
    uploader = NoteMsUploader()
    success = uploader.run()
    
    if success:
        print("✅ 文件上传任务完成!")
        exit(0)
    else:
        print("❌ 文件上传任务失败!")
        exit(1)


if __name__ == "__main__":
    main()