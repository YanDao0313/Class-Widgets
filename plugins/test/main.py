'''
    这是一个示例插件
'''
from PyQt6.QtCore import Qt
from loguru import logger
from datetime import datetime

from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from qfluentwidgets import ImageLabel

# 自定义小组件
WIDGET_CODE = 'widget_test.ui'
WIDGET_NAME = '测试组件'
WIDGET_WIDTH = 245


class Plugin:
    def __init__(self, cw_contexts, method):
        # 先保存上下文和方法，因为load_ui需要用到PATH
        self.cw_contexts = cw_contexts
        self.method = method
        self.PATH = cw_contexts['PLUGIN_PATH']
        self.CONFIG_PATH = f'{self.PATH}/config.json'
        
        self.test_widget = None
        self.load_ui()  # 加载UI放在最后
        
        # 注册小组件
        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)

    def load_ui(self):
        try:
            # 使用正确的UI文件路径
            ui_path = f'{self.PATH}/{WIDGET_CODE}'
            self.test_widget = self.method.get_widget(WIDGET_CODE)
            
            if self.test_widget is None:
                raise Exception(f"无法加载UI文件: {ui_path}")
                
        except Exception as e:
            logger.error(f"加载UI失败: {e}")
            return False
        return True

    def execute(self):
        # 不需要重新获取widget，直接使用self.test_widget
        if self.test_widget is None:
            logger.error("小组件未正确初始化")
            return

        try:
            contentLayout = self.test_widget.findChild(QHBoxLayout, 'contentLayout')
            if contentLayout is None:
                raise Exception("未找到contentLayout")
                
            contentLayout.setSpacing(1)

        if self.test_widget:  # 判断小组件是否存在
            contentLayout = self.test_widget.findChild(QHBoxLayout, 'contentLayout')  # 标题布局
            contentLayout.setSpacing(1)  # 设置间距

            self.testimg = ImageLabel(f'{self.PATH}/img/favicon.png')  # 自定义图片
            self.testimg.setFixedSize(36, 30)
            contentLayout.addWidget(self.testimg)

            # 更新内容
            if self.cw_contexts['State']:
                self.method.change_widget_content(WIDGET_CODE, '测试', '上课状态')
            else:
                self.method.change_widget_content(WIDGET_CODE, '测试', '课间状态')

            logger.success('Plugin1 executed!')
            logger.info(f'Config path: {self.CONFIG_PATH}')
            
        except Exception as e:
            logger.error(f"execute执行失败: {e}")
