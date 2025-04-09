"""
UI样式定义模块
包含应用程序的颜色、字体和其他样式常量
"""

# 颜色定义
COLORS = {
    "primary": "#4a6fa5",       # 主色调 - 蓝色
    "primary_light": "#dbe4f0", # 浅主色调
    "secondary": "#6c757d",     # 次要色调 - 灰色
    "success": "#28a745",       # 成功色调 - 绿色
    "danger": "#dc3545",        # 危险色调 - 红色
    "warning": "#ffc107",       # 警告色调 - 黄色
    "info": "#17a2b8",          # 信息色调 - 青色
    "light": "#f8f9fa",         # 浅色
    "dark": "#343a40",          # 深色
    "white": "#ffffff",         # 白色
    "bg_light": "#f5f5f5",      # 背景浅色
    "border": "#dee2e6"         # 边框颜色
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

# 样式定义
STYLES = {
    "button": {
        "bg": COLORS["primary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["secondary"],
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "padx": 10,
        "pady": 5,
        "cursor": "hand2"
    },
    "secondary_button": {
        "bg": COLORS["secondary"],
        "fg": COLORS["white"],
        "activebackground": COLORS["dark"],
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "padx": 10,
        "pady": 5,
        "cursor": "hand2"
    },
    "action_button": {
        "bg": COLORS["success"],
        "fg": COLORS["white"],
        "activebackground": "#218838",  # 深绿色
        "activeforeground": COLORS["white"],
        "font": FONTS["button"],
        "borderwidth": 0,
        "padx": 15,
        "pady": 8,
        "cursor": "hand2"
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
        "bg": COLORS["bg_light"],
        "padx": 10,
        "pady": 5,
        "relief": "groove",
        "borderwidth": 1
    }
}

# 进度条样式
PROGRESS_STYLE = {
    "troughcolor": COLORS["light"],
    "background": COLORS["bg_light"],
    "foreground": COLORS["success"]
}
