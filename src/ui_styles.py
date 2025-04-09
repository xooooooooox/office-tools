"""
UI样式定义模块
包含应用程序的颜色、字体和其他样式常量
"""

# 颜色定义 - 更柔和的配色方案
COLORS = {
    "primary": "#3498db",  # 主色调 - 柔和的蓝色
    "primary_dark": "#2980b9",  # 深主色调
    "primary_light": "#e8f4fc",  # 浅主色调
    "secondary": "#7f8c8d",  # 次要色调 - 柔和的灰色
    "success": "#2ecc71",  # 成功色调 - 柔和的绿色
    "danger": "#e74c3c",  # 危险色调 - 柔和的红色
    "warning": "#f39c12",  # 警告色调 - 柔和的黄色
    "info": "#3498db",  # 信息色调 - 柔和的青色
    "light": "#ecf0f1",  # 浅色
    "dark": "#34495e",  # 深色
    "white": "#ffffff",  # 白色
    "bg_light": "#f5f7fa",  # 背景浅色
    "border": "#bdc3c7"  # 边框颜色
}

# 字体定义
FONTS = {
    "title": ("Helvetica", 14, "bold"),
    "subtitle": ("Helvetica", 12, "bold"),
    "normal": ("Helvetica", 10),
    "small": ("Helvetica", 9),
    "button": ("Helvetica", 10, "bold"),
    "status": ("Courier New", 9)
}

# 按钮尺寸 - 确保一致性
BUTTON_SIZES = {
    "width": 20,  # 标准按钮宽度
    "height": 1,  # 标准按钮高度
    "action_width": 15,  # 操作按钮宽度
}

# 样式定义
STYLES = {
    "button": {
        "bg": COLORS["primary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["primary_dark"],
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "width": BUTTON_SIZES["width"],
        "height": BUTTON_SIZES["height"],
        "cursor": "hand2",
        "relief": "flat"
    },
    "secondary_button": {
        "bg": COLORS["secondary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["dark"],
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "width": BUTTON_SIZES["width"],
        "height": BUTTON_SIZES["height"],
        "cursor": "hand2",
        "relief": "flat"
    },
    "action_button": {
        "bg": COLORS["success"],
        "fg": COLORS["white"],
        "activebackground": "#27ae60",  # 深绿色
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "width": BUTTON_SIZES["action_width"],
        "height": BUTTON_SIZES["height"],
        "cursor": "hand2",
        "relief": "flat"
    },
    "label": {
        "bg": COLORS["bg_light"],
        "fg": COLORS["dark"],
        "font": FONTS["normal"],
        "padx": 5
    },
    "title_label": {
        "bg": COLORS["bg_light"],
        "fg": COLORS["primary"],
        "font": FONTS["title"],
        "padx": 5,
        "pady": 5
    },
    "subtitle_label": {
        "bg": COLORS["bg_light"],
        "fg": COLORS["secondary"],
        "font": FONTS["subtitle"],
        "padx": 5,
        "pady": 5
    },
    "status_text": {
        "bg": COLORS["white"],
        "fg": COLORS["dark"],
        "font": FONTS["status"],
        "relief": "sunken",
        "borderwidth": 1,
        "padx": 5,
        "pady": 5
    },
    "frame": {
        "bg": COLORS["bg_light"],
        "padx": 10,
        "pady": 10,
        "relief": "flat"
    },
    "file_frame": {
        "bg": COLORS["primary_light"],
        "padx": 10,
        "pady": 5,
        "relief": "flat",
        "borderwidth": 0
    }
}

# 进度条样式
PROGRESS_STYLE = {
    "troughcolor": COLORS["light"],
    "background": COLORS["bg_light"],
    "foreground": COLORS["success"]
}

# Tab样式
TAB_STYLE = {
    "background": COLORS["primary"],
    "foreground": COLORS["white"],
    "selected_background": COLORS["primary_dark"],
    "selected_foreground": COLORS["white"],
    "padding": [15, 8]  # [x, y] padding
}
