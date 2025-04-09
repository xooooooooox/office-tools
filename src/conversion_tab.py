import os
import subprocess
import tkinter as tk
from tkinter import filedialog

from base_tab import BaseTab


class ConversionTab(BaseTab):
    """
    文件格式转换功能 Tab，用于将选中的 Word 文件（.doc 或 .docx）批量转换为 PDF
    使用 LibreOffice 的命令行模式进行转换。
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.word_files = []  # 待转换的文件列表
        self.output_dir = ""
        self.create_widgets()

    def create_widgets(self):
        """创建UI组件"""
        # 选择文件
        self.files_btn, self.files_label, _ = self.create_file_selector(
            row=0,
            button_text="选择 Word 文件",
            label_text="未选择文件",
            command=self.choose_word_files
        )

        # 选择输出目录
        self.output_btn, self.output_label, _ = self.create_file_selector(
            row=1,
            button_text="选择输出目录",
            label_text="未选择输出目录",
            command=self.choose_output_dir
        )

        # 转换按钮
        self.convert_btn = self.create_action_button(
            row=2,
            text="开始转换",
            command=self.start_conversion
        )

        # 进度条
        self.progress_var, self.progress_bar = self.create_progress_bar()

        # 状态文本区
        self.status_text = self.create_status_area(row=3)

    def choose_word_files(self):
        """选择Word文件"""
        files = filedialog.askopenfilenames(
            title="选择 Word 文件",
            filetypes=[("Word 文件", ("*.doc", "*.docx"))]
        )
        if files:
            self.word_files = list(files)
            # 只显示文件数量而不是所有文件名
            self.files_label.config(text=f"已选择 {len(self.word_files)} 个文件")

    def choose_output_dir(self):
        """选择输出目录"""
        dir_ = filedialog.askdirectory(title="选择输出目录")
        if dir_:
            self.output_dir = dir_
            self.output_label.config(text=dir_)

    def start_conversion(self):
        """开始转换处理"""
        self.update_status("", clear=True)
        self.progress_var.set(0)

        if not self.word_files or not self.output_dir:
            self.update_status("请先选择 Word 文件和输出目录！")
            return

        # 显示进度条
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # 禁用按钮，防止重复操作
        self.toggle_buttons(enabled=False)

        try:
            self.convert_files()
        finally:
            # 无论成功失败，最后都要重新启用按钮
            self.toggle_buttons(enabled=True)

    def toggle_buttons(self, enabled=True):
        """启用或禁用按钮"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.files_btn.config(state=state)
        self.output_btn.config(state=state)
        self.convert_btn.config(state=state)

    def convert_files(self):
        """执行文件转换"""
        total = len(self.word_files)
        success_count = 0

        for idx, file in enumerate(self.word_files):
            base_name = os.path.splitext(os.path.basename(file))[0]

            try:
                # 调用 LibreOffice 的命令行转换功能
                subprocess.run([
                    "soffice",
                    "--headless",
                    "--convert-to", "pdf",
                    file,
                    "--outdir", self.output_dir
                ], check=True)

                self.update_status(f"已转换: {os.path.basename(file)} -> {base_name}.pdf")
                success_count += 1
            except subprocess.CalledProcessError as e:
                self.update_status(f"转换失败: {os.path.basename(file)}，错误信息: {e}")

            # 更新进度条
            progress_percentage = ((idx + 1) / total) * 100
            self.progress_var.set(progress_percentage)
            self.master.update_idletasks()

        msg = f"转换完成，共转换 {success_count}/{total} 个文件！"
        self.update_status(msg)
        self.show_message("提示", msg)
