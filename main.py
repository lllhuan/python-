import pygame
import pymysql
import sys
import time
import logging
import os
from datetime import datetime

# 配置日志系统
def setup_logger():
    # 创建logs目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 生成日志文件名，包含日期
    log_filename = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# 初始化日志记录器
logger = setup_logger()

# 初始化pygame
pygame.init()

# 颜色定义
BACKGROUND = (230, 240, 255)
INPUT_BG = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
TEXT_COLOR = (25, 25, 112)
ERROR_COLOR = (220, 20, 60)
SUCCESS_COLOR = (50, 205, 50)

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("用户登录注册系统")

# 字体
font = pygame.font.SysFont("simhei", 32)
small_font = pygame.font.SysFont("simhei", 24)

class InputBox:
    def __init__(self, x, y, width, height, placeholder='', is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.text = ''
        self.placeholder = placeholder
        self.txt_surface = font.render(placeholder, True, (150, 150, 150))
        self.active = False
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = (70, 130, 180) if self.active else (200, 200, 200)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                if self.is_password:
                    display_text = '*' * len(self.text)
                else:
                    display_text = self.text

                self.txt_surface = font.render(display_text, True, TEXT_COLOR)
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, INPUT_BG, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)

        if self.text or self.active:
            screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        else:
            placeholder_surface = font.render(self.placeholder, True, (150, 150, 150))
            screen.blit(placeholder_surface, (self.rect.x + 10, self.rect.y + 10))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.text = text
        self.txt_surface = font.render(text, True, (255, 255, 255))
        self.is_hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

def register_user(username, password):
    """注册新用户"""
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='aicarnumber',
            charset='utf8mb4'
        )
        logger.info(f"数据库连接成功 - 用户注册尝试: {username}")

        cursor = connection.cursor()

        # 检查用户名是否已存在
        cursor.execute("SELECT * FROM user WHERE user = %s", (username,))
        if cursor.fetchone():
            logger.warning(f"注册失败 - 用户名已存在: {username}")
            return False, "用户名已存在"

        # 插入新用户
        cursor.execute(
            "INSERT INTO user (user, password) VALUES (%s, %s)",
            (username, password)
        )

        connection.commit()
        logger.info(f"注册成功 - 新用户: {username}")
        return True, "注册成功!"
    except pymysql.Error as e:
        error_msg = f"数据库错误: {e}"
        logger.error(f"注册失败 - {error_msg}")
        return False, error_msg
    finally:
        if connection:
            connection.close()
            logger.debug("数据库连接已关闭")

def login_user(username, password):
    """用户登录"""
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='aicarnumber',
            charset='utf8mb4'
        )
        logger.info(f"数据库连接成功 - 用户登录尝试: {username}")

        cursor = connection.cursor()

        # 验证用户名和密码
        cursor.execute("SELECT * FROM user WHERE user = %s AND password = %s", (username, password))
        if cursor.fetchone():
            logger.info(f"登录成功 - 用户: {username}")
            return True, "登录成功!"
        else:
            logger.warning(f"登录失败 - 用户名或密码错误: {username}")
            return False, "用户名或密码错误"
    except pymysql.Error as e:
        error_msg = f"数据库错误: {e}"
        logger.error(f"登录失败 - {error_msg}")
        return False, error_msg
    finally:
        if connection:
            connection.close()
            logger.debug("数据库连接已关闭")

def main():
    logger.info("应用程序启动")
    
    # 创建UI元素
    username_box = InputBox(SCREEN_WIDTH // 2 - 150, 200, 300, 50, '用户名')
    password_box = InputBox(SCREEN_WIDTH // 2 - 150, 280, 300, 50, '密码', is_password=True)

    login_button = Button(SCREEN_WIDTH // 2 - 160, 380, 150, 50, "登录")
    register_button = Button(SCREEN_WIDTH // 2 + 10, 380, 150, 50, "注册")

    # 状态变量
    message = ""
    message_color = TEXT_COLOR
    close_time = None

    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # 检查是否需要关闭窗口
        if close_time and time.time() >= close_time:
            logger.info("应用程序正常关闭")
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("用户关闭窗口")
                running = False

            # 输入框事件
            username_box.handle_event(event)
            if password_box.handle_event(event):
                logger.info(f"用户尝试登录 - 用户名: {username_box.text}")
                success, msg = login_user(username_box.text, password_box.text)
                message = msg
                message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    close_time = time.time() + 10

            # 按钮事件
            if login_button.handle_event(event):
                logger.info(f"用户点击登录按钮 - 用户名: {username_box.text}")
                success, msg = login_user(username_box.text, password_box.text)
                message = msg
                message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    close_time = time.time() + 10

            if register_button.handle_event(event):
                logger.info(f"用户点击注册按钮 - 用户名: {username_box.text}")
                success, msg = register_user(username_box.text, password_box.text)
                message = msg
                message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    close_time = time.time() + 10

        # 按钮悬停效果
        login_button.check_hover(mouse_pos)
        register_button.check_hover(mouse_pos)

        # 绘制界面
        screen.fill(BACKGROUND)

        # 绘制标题
        title = font.render("用户登录注册系统", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # 绘制输入框
        username_box.draw(screen)
        password_box.draw(screen)

        # 绘制按钮
        login_button.draw(screen)
        register_button.draw(screen)

        # 绘制消息
        if message:
            msg_surface = small_font.render(message, True, message_color)
            screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 340))
            
            # 如果设置了关闭时间，显示倒计时
            if close_time:
                remaining_time = int(close_time - time.time())
                if remaining_time > 0:
                    countdown = small_font.render(f"窗口将在 {remaining_time} 秒后关闭", True, TEXT_COLOR)
                    screen.blit(countdown, (SCREEN_WIDTH // 2 - countdown.get_width() // 2, 450))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    logger.info("应用程序已退出")
    sys.exit()

if __name__ == "__main__":
    main()