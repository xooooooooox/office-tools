import tkinter as tk
from tkinter import ttk, messagebox


class BaseTab(tk.Frame):
    """
    所有功能Tab的基类，提供通用功能和UI组件
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def create_file_selector(self, row, button_text, label_text, command, file_types=None):
        """创建文件选择器组件（按钮+标签）"""
        frame = tk.Frame(self)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        button = tk.Button(frame, text=button_text, command=command)
        button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        return button, label, frame

    def create_action_button(self, row, text, command):
        """创建操作按钮（如"开始生成"、"开始匹配"等）"""
        button = tk.Button(self, text=text, command=command)
        button.grid(row=row, column=0, columnspan=2, pady=10)
        return button

    def create_progress_bar(self):
        """创建进度条"""
        progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(self, variable=progress_var, maximum=100)
        return progress_var, progress_bar

    def create_status_area(self, row):
        """创建带滚动条的状态文本区域"""
        status_frame = tk.Frame(self)
        status_frame.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(row, weight=1)

        scrollbar = tk.Scrollbar(status_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        status_text = tk.Text(status_frame, width=50, height=10, yscrollcommand=scrollbar.set)
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
