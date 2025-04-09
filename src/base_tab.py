import sys
import tkinter as tk
import traceback
from tkinter import ttk, messagebox

from ui_styles import COLORS, STYLES, PROGRESS_STYLE


class BaseTab(tk.Frame):
    """
    所有功能Tab的基类，提供通用功能和UI组件
    """

    def __init__(self, master=None):
        super().__init__(master, bg=COLORS["bg_light"], padx=15, pady=15)
        self.master = master

        # 创建标题样式
        self.style = ttk.Style()
        self.style.configure("Custom.TProgressbar",
                             troughcolor=PROGRESS_STYLE["troughcolor"],
                             background=PROGRESS_STYLE["background"],
                             foreground=PROGRESS_STYLE["foreground"])

    def create_title(self, text):
        """创建标题标签"""
        title_frame = tk.Frame(self, bg=COLORS["bg_light"])
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 15))

        title = tk.Label(title_frame, text=text, **STYLES["title_label"])
        title.pack(side=tk.LEFT, fill=tk.X)

        return title_frame

    def create_file_selector(self, row, button_text, label_text, command, file_types=None):
        """创建文件选择器组件（按钮+标签）"""
        frame = tk.Frame(self, **STYLES["file_frame"])
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=8)

        # 使用固定宽度的按钮
        button = tk.Button(frame, text=button_text, command=self.safe_execute(command), **STYLES["button"])
        button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # 创建一个框架来包含标签，并设置固定宽度
        label_frame = tk.Frame(frame, bg=COLORS["primary_light"])
        label_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        frame.columnconfigure(1, weight=1)  # 让标签框架可以扩展

        label = tk.Label(label_frame, text=label_text, anchor="w", **STYLES["label"])
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        return button, label, frame

    def create_action_button(self, row, text, command):
        """创建操作按钮（如"开始生成"、"开始匹配"等）"""
        button_frame = tk.Frame(self, bg=COLORS["bg_light"])
        button_frame.grid(row=row, column=0, columnspan=2, pady=15)

        # 使用固定宽度的按钮
        button = tk.Button(button_frame, text=text, command=self.safe_execute(command), **STYLES["action_button"])
        button.pack(padx=10, pady=5)

        return button

    def create_progress_bar(self):
        """创建进度条"""
        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(self, style="Custom.TProgressbar", variable=progress_var, maximum=100)
        return progress_var, progress_bar

    def create_status_area(self, row):
        """创建带滚动条的状态文本区域"""
        status_frame = tk.Frame(self, bg=COLORS["bg_light"], padx=5, pady=5)
        status_frame.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(row, weight=1)

        # 添加状态区标题
        status_label = tk.Label(status_frame, text="状态信息", anchor="w", **STYLES["subtitle_label"])
        status_label.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        # 创建内部框架用于文本和滚动条
        text_frame = tk.Frame(status_frame, bg=COLORS["white"], relief="sunken", borderwidth=1)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        status_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, **STYLES["status_text"])
        status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=status_text.yview)

        return status_text

    def show_message(self, title, message, error=False):
        """显示消息对话框"""
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    def update_status(self, text, clear=False):
        """更新状态文本区域"""
        if clear:
            self.status_text.delete("1.0", tk.END)
        self.status_text.insert(tk.END, text + "\n")
        self.status_text.see(tk.END)  # 自动滚动到底部
        # 强制更新UI
        self.update_idletasks()

    def safe_execute(self, func):
        """
        包装函数以捕获和显示异常
        这样用户界面不会因为未捕获的异常而崩溃
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"操作过程中发生错误: {str(e)}"
                if hasattr(self, 'status_text'):
                    self.update_status(error_msg)
                    self.update_status(traceback.format_exc())
                self.show_message("错误", error_msg, error=True)
                # 记录到控制台
                print(error_msg, file=sys.stderr)
                traceback.print_exc()

        return wrapper
