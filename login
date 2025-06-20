import pygame
import pymysql
import os
import time
from logger import logger

# 颜色定义 - 新的配色方案
BACKGROUND = (240, 248, 255)  # 淡蓝色背景RGB RED GREEN BULE
INPUT_BG = (255, 255, 255)    # 白色输入框
BUTTON_COLOR = (65, 105, 225)  # 皇家蓝
BUTTON_HOVER = (30, 144, 255)  # 道奇蓝
TEXT_COLOR = (47, 79, 79)     # 深青灰色
ERROR_COLOR = (220, 20, 60)   # 猩红色
SUCCESS_COLOR = (60, 179, 113) # 海洋绿
INPUT_BORDER = (176, 196, 222) # 淡钢蓝
PLACEHOLDER_COLOR = (169, 169, 169) # 暗灰色

# 初始化pygame字体
pygame.font.init()

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 字体文件路径
font_path = os.path.join(current_dir, "fonts", "simhei.ttf")

# 如果字体文件不存在，创建fonts目录并下载字体
if not os.path.exists(font_path):
    try:
        os.makedirs(os.path.dirname(font_path), exist_ok=True)
        logger.info("正在创建fonts目录")
    except Exception as e:
        logger.error(f"创建fonts目录失败: {e}")

# 创建字体对象
try:
    # 尝试加载系统字体
    title_font = pygame.font.SysFont("simhei", 48, bold=True)
    font = pygame.font.SysFont("simhei", 32)
    small_font = pygame.font.SysFont("simhei", 24)
    
    # 测试字体
    test_text = "测试"
    title_font.render(test_text, True, (0, 0, 0))
    logger.info("使用系统字体成功")
except Exception as e:
    logger.error(f"加载系统字体失败: {e}")
    # 如果系统字体加载失败，使用默认字体
    title_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
    logger.info("使用默认字体")

# 测试字体是否可用
def test_font():
    try:
        test_text = "测试"
        title_font.render(test_text, True, (0, 0, 0))
        font.render(test_text, True, (0, 0, 0))
        small_font.render(test_text, True, (0, 0, 0))
        logger.info(f"字体初始化成功，使用字体: {font_path}")
    except Exception as e:
        logger.error(f"字体渲染测试失败: {e}")

# 运行字体测试
test_font()

class InputBox:
    def __init__(self, x, y, width, height, placeholder='', is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.placeholder = placeholder
        self.is_password = is_password
        self.txt_surface = font.render(placeholder, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render('*' * len(self.text) if self.is_password else self.text, True, self.color)
        return False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = pygame.Color('lightskyblue3')
        self.hover_color = pygame.Color('dodgerblue2')
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class LoginWindow:
    def __init__(self):
        # 屏幕尺寸
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("用户登录注册系统")

        # 创建UI元素
        self.username_box = InputBox(self.SCREEN_WIDTH // 2 - 150, 220, 300, 50, '用户名')
        self.password_box = InputBox(self.SCREEN_WIDTH // 2 - 150, 300, 300, 50, '密码', is_password=True)
        self.login_button = Button(self.SCREEN_WIDTH // 2 - 160, 400, 150, 50, "登录")
        self.register_button = Button(self.SCREEN_WIDTH // 2 + 10, 400, 150, 50, "注册")

        # 状态变量
        self.message = ""
        self.message_color = TEXT_COLOR
        self.close_time = None
        self.running = True
        self.logged_in = False  # 添加登录状态标志

    def render_text(self, text, font_obj, color):
        """渲染文本并返回surface和rect"""
        try:
            surface = font_obj.render(text, True, color)
            rect = surface.get_rect()
            return surface, rect
        except Exception as e:
            logger.error(f"文本渲染失败: {e}")
            return pygame.Surface((0, 0)), pygame.Rect(0, 0, 0, 0)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        # 检查是否需要关闭窗口
        if self.close_time and time.time() >= self.close_time:
            logger.info("应用程序正常关闭")
            self.running = False
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("用户关闭窗口")
                self.running = False
                return

            # 输入框事件
            self.username_box.handle_event(event)
            if self.password_box.handle_event(event):
                logger.info(f"用户尝试登录 - 用户名: {self.username_box.text}")
                success, msg = login_user(self.username_box.text, self.password_box.text)
                self.message = msg
                self.message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    self.logged_in = True  # 设置登录成功标志
                    self.close_time = time.time() + 5

            # 按钮事件
            if self.login_button.handle_event(event):
                logger.info(f"用户点击登录按钮 - 用户名: {self.username_box.text}")
                success, msg = login_user(self.username_box.text, self.password_box.text)
                self.message = msg
                self.message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    self.logged_in = True  # 设置登录成功标志
                    self.close_time = time.time() + 5

            if self.register_button.handle_event(event):
                logger.info(f"用户点击注册按钮 - 用户名: {self.username_box.text}")
                success, msg = register_user(self.username_box.text, self.password_box.text)
                self.message = msg
                self.message_color = SUCCESS_COLOR if success else ERROR_COLOR
                if success:
                    self.close_time = time.time() + 10

        # 按钮悬停效果
        self.login_button.check_hover(mouse_pos)
        self.register_button.check_hover(mouse_pos)

    def draw(self):
        # 绘制界面
        self.screen.fill(BACKGROUND)

        # 绘制标题
        title_surface, title_rect = self.render_text("用户登录注册系统", title_font, TEXT_COLOR)
        title_rect.center = (self.SCREEN_WIDTH // 2, 120)
        self.screen.blit(title_surface, title_rect)

        # 绘制输入框
        self.username_box.draw(self.screen)
        self.password_box.draw(self.screen)

        # 绘制按钮
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # 绘制消息
        if self.message:
            msg_surface, msg_rect = self.render_text(self.message, small_font, self.message_color)
            msg_rect.center = (self.SCREEN_WIDTH // 2, 480)
            self.screen.blit(msg_surface, msg_rect)
            
            # 如果设置了关闭时间，显示倒计时
            if self.close_time:
                remaining_time = int(self.close_time - time.time())
                if remaining_time > 0:
                    countdown_text = f"窗口将在 {remaining_time} 秒后关闭"
                    countdown_surface, countdown_rect = self.render_text(countdown_text, small_font, TEXT_COLOR)
                    countdown_rect.center = (self.SCREEN_WIDTH // 2, 520)
                    self.screen.blit(countdown_surface, countdown_rect)

        pygame.display.flip()

    def is_running(self):
        return self.running

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
