import os
from tkinter import filedialog

from base_tab import BaseTab


class GenerateTab(BaseTab):
    """
    批量生成 Word 文档的功能 Tab
    """

    def __init__(self, master=None, doc_generator=None):
        super().__init__(master)
        self.master = master
        self.doc_generator = doc_generator

        self.template_path = ""
        self.excel_path = ""
        self.output_dir = ""

        self.create_widgets()

    def create_widgets(self):
        """创建UI组件"""
        # 选择 Word 模板
        self.template_btn, self.template_label, _ = self.create_file_selector(
            row=0,
            button_text="选择 Word 模板",
            label_text="未选择模板",
            command=self.choose_template,
            file_types=[("Word 文件", "*.docx")]
        )

        # 选择 Excel 数据
        self.excel_btn, self.excel_label, _ = self.create_file_selector(
            row=1,
            button_text="选择 Excel 数据",
            label_text="未选择 Excel",
            command=self.choose_excel,
            file_types=[("Excel 文件", "*.xlsx *.xls")]
        )

        # 选择输出目录
        self.output_btn, self.output_dir_label, _ = self.create_file_selector(
            row=2,
            button_text="选择输出目录",
            label_text="未选择输出目录",
            command=self.choose_output_dir
        )

        # 进度条（默认未显示，开始生成后显示）
        self.progress_var, self.progress_bar = self.create_progress_bar()

        # 生成按钮
        self.generate_btn = self.create_action_button(
            row=4,
            text="开始生成",
            command=self.start_generate
        )

        # 状态输出区
        self.status_text = self.create_status_area(row=5)

    def choose_template(self):
        """选择Word模板文件"""
        path = filedialog.askopenfilename(
            title="选择 Word 模板",
            filetypes=[("Word 文件", "*.docx")]
        )
        if path:
            self.template_path = path
            self.template_label.config(text=os.path.basename(path))

    def choose_excel(self):
        """选择Excel数据文件"""
        path = filedialog.askopenfilename(
            title="选择 Excel 文件",
            filetypes=[("Excel 文件", "*.xlsx *.xls")]
        )
        if path:
            self.excel_path = path
            self.excel_label.config(text=os.path.basename(path))

    def choose_output_dir(self):
        """选择输出目录"""
        dir_ = filedialog.askdirectory(title="选择输出目录")
        if dir_:
            self.output_dir = dir_
            self.output_dir_label.config(text=dir_)

    def start_generate(self):
        """开始生成文档"""
        self.update_status("", clear=True)
        self.progress_var.set(0)

        if not (self.template_path and self.excel_path and self.output_dir):
            self.update_status("请先选择 Word 模板、Excel 文件和输出目录！")
            return

        # 显示进度条
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        def progress_callback(current, total):
            """更新进度条的回调函数"""
            progress_percentage = (current / total) * 100
            self.progress_var.set(progress_percentage)
            self.master.update_idletasks()

        try:
            msg = self.doc_generator(
                self.template_path,
                self.excel_path,
                self.output_dir,
                progress_callback=progress_callback
            )
            self.update_status(msg)
            self.show_message("提示", msg)
        except Exception as e:
            err_msg = f"生成失败：{e}"
            self.update_status(err_msg)
            self.show_message("错误", err_msg, error=True)
