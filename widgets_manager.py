# widgets_manager.py
from PyQt6.QtCore import Qt
from loguru import logger
import conf

class WidgetsManager:
    def __init__(self):
        self.widgets = []
        self.state = 1
        self.window_penetration = conf.read_conf('Advanced', 'window_penetration') == '1'
        self.apply_window_penetration()

    def apply_window_penetration(self):
        for widget in self.widgets:
            if self.window_penetration:
                widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
                logger.info(f'启用指针穿透: {widget.windowTitle()}')
            else:
                widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
                logger.info(f'禁用指针穿透: {widget.windowTitle()}')
            widget.show()

    def add_widget(self, widget):
        self.widgets.append(widget)
        self.apply_window_penetration()

    def hide_widgets(self):
        if self.window_penetration:
            # 窗口穿透开启时，不执行隐藏操作
            return
        for widget in self.widgets:
            widget.hide()

    def show_widgets(self):
        if self.window_penetration:
            # 窗口穿透开启时，不执行显示操作
            return
        for widget in self.widgets:
            widget.show()

    def show_windows(self):
        for widget in self.widgets:
            widget.animate_show()
        self.state = 1

    def clear_widgets(self):
        for widget in self.widgets:
            widget.animate_hide_opacity()
        self.widgets.clear()

    def update_widgets(self):
        for widget in self.widgets:
            path = getattr(widget, 'path', None)
            if path:
                widget.update_data(path=path)
            else:
                widget.update_data()

    def decide_to_hide(self):
        hide_method = conf.read_conf('General', 'hide_method')
        if hide_method == '0':  # 正常
            self.hide_windows()
        elif hide_method == '1':  # 单击即完全隐藏
            self.full_hide_windows()
        elif hide_method == '2':  # 最小化为浮窗
            if not getattr(fw, 'animating', False):
                self.full_hide_windows()
                fw.show()
        else:
            self.hide_windows()

    def full_hide_windows(self):
        for widget in self.widgets:
            widget.animate_hide(full=True)
        self.state = 0

    def hide_windows(self):
        for widget in self.widgets:
            widget.animate_hide()
        self.state = 0

# 创建单例实例
mgr = WidgetsManager()