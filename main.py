import pygame
import sys
from LoginRegister import LoginWindow
from logger import logger
from btn import PlateRecognitionSystem
import time
import subprocess
import os

def safe_pygame_quit():
    """安全地退出pygame"""
    try:
        pygame.quit()
    except Exception as e:
        logger.error(f"退出pygame时出错: {e}")
    finally:
        # 确保所有pygame模块都被清理
        for module in [pygame.display, pygame.font, pygame.event]:
            try:
                module.quit()
            except:
                pass

def run_plate_system():
    """在单独的进程中运行停车场系统"""
    try:
        # 获取当前脚本的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建btn.py的完整路径
        btn_path = os.path.join(current_dir, 'btn.py')

        # 使用Python解释器运行btn.py
        subprocess.run([sys.executable, btn_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"停车场系统运行失败: {e}")
        return False
    except Exception as e:
        logger.error(f"启动停车场系统时出错: {e}")
        return False

def main():
    logger.info("应用程序启动")
    print("程序启动中...")

    try:
        # 初始化pygame
        pygame.init()
        pygame.font.init()
        logger.info("初始化Pygame for LoginWindow")
        print("启动登录窗口...")

        # 创建并运行登录窗口
        window = LoginWindow()
        clock = pygame.time.Clock()

        logger.info("GUI窗口正在运行: 登录")
        print("登录窗口已启动，请在弹出的窗口中操作...")

        # 运行登录窗口循环
        while window.is_running():
            window.handle_events()
            window.draw()
            clock.tick(30)

        # 退出pygame
        pygame.quit()
        logger.info("GUI窗口已关闭: 登录")
        print("登录窗口已关闭。")

        # 检查登录状态
        if window.logged_in:
            print("登录成功，正在启动停车场管理系统...")
            logger.info("登录成功，启动停车场管理系统")

            # 在单独的进程中运行停车场系统
            if run_plate_system():
                print("停车场管理系统已关闭。")
                logger.info("停车场管理系统已关闭。")
            else:
                print("停车场管理系统运行失败。")
                logger.error("停车场管理系统运行失败。")
        else:
            print("未登录或登录失败，程序退出。")
            logger.info("未登录或登录失败，程序退出。")

    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        print(f"程序运行出错: {e}")
        if pygame.get_init():
            pygame.quit()
        time.sleep(2)
        print("程序将在短时间后尝试重新启动（回到登录界面）。")

if __name__ == "__main__":
    main()
