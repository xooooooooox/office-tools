import os
import platform
import subprocess
import tkinter as tk
import traceback
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
        # 添加标题
        self.create_title("文件格式转换 (Word → PDF)")

        # 选择文件
        self.files_btn, self.files_label, _ = self.create_file_selector(
            row=1,
            button_text="选择 Word 文件",
            label_text="未选择文件",
            command=self.choose_word_files
        )

        # 选择输出目录
        self.output_btn, self.output_label, _ = self.create_file_selector(
            row=2,
            button_text="选择输出目录",
            label_text="未选择输出目录",
            command=self.choose_output_dir
        )

        # 转换按钮
        self.convert_btn = self.create_action_button(
            row=4,
            text="开始转换",
            command=self.start_conversion
        )

        # 进度条
        self.progress_var, self.progress_bar = self.create_progress_bar()

        # 状态文本区
        self.status_text = self.create_status_area(row=5)

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

    def find_libreoffice_path(self):
        """
        查找 LibreOffice 可执行文件的路径
        返回可执行文件路径或 None（如果未找到）
        """
        # 常见的 LibreOffice 可执行文件路径
        possible_paths = []

        if platform.system() == "Darwin":  # macOS
            possible_paths = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "/Applications/OpenOffice.app/Contents/MacOS/soffice",
                "/usr/local/bin/soffice"
            ]
        elif platform.system() == "Windows":  # Windows
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                r"C:\Program Files\OpenOffice\program\soffice.exe",
                r"C:\Program Files (x86)\OpenOffice\program\soffice.exe"
            ]
        else:  # Linux 和其他系统
            possible_paths = [
                "/usr/bin/soffice",
                "/usr/local/bin/soffice",
                "/opt/libreoffice/program/soffice"
            ]

        # 检查命令是否存在于 PATH 中
        import shutil
        soffice_in_path = shutil.which("soffice")
        if soffice_in_path:
            possible_paths.insert(0, soffice_in_path)

        # 检查每个可能的路径
        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

        return None

    def start_conversion(self):
        """开始转换处理"""
        self.update_status("", clear=True)
        self.progress_var.set(0)

        if not self.word_files or not self.output_dir:
            self.update_status("请先选择 Word 文件和输出目录！")
            return

        # 显示进度条
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # 禁用按钮，防止重复操作
        self.toggle_buttons(enabled=False)

        # 查找 LibreOffice 路径
        libreoffice_path = self.find_libreoffice_path()
        if not libreoffice_path:
            error_msg = "无法找到 LibreOffice 可执行文件。请确保已安装 LibreOffice 并且可以从命令行访问。"
            self.update_status(error_msg)
            self.show_message("错误", error_msg, error=True)
            self.toggle_buttons(enabled=True)
            return

        self.update_status(f"使用 LibreOffice: {libreoffice_path}")

        try:
            self.convert_files(libreoffice_path)
        except Exception as e:
            error_msg = f"转换过程中发生错误: {str(e)}"
            self.update_status(error_msg)
            self.update_status(traceback.format_exc())
            self.show_message("错误", error_msg, error=True)
        finally:
            # 无论成功失败，最后都要重新启用按钮
            self.toggle_buttons(enabled=True)

    def toggle_buttons(self, enabled=True):
        """启用或禁用按钮"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.files_btn.config(state=state)
        self.output_btn.config(state=state)
        self.convert_btn.config(state=state)

    def convert_files(self, libreoffice_path):
        """执行文件转换"""
        total = len(self.word_files)
        success_count = 0

        for idx, file in enumerate(self.word_files):
            base_name = os.path.splitext(os.path.basename(file))[0]

            try:
                # 确保文件路径是绝对路径
                abs_file_path = os.path.abspath(file)
                abs_output_dir = os.path.abspath(self.output_dir)

                self.update_status(f"正在转换: {os.path.basename(file)}")

                # 创建一个临时日志文件来捕获输出
                log_file = os.path.join(abs_output_dir, f"conversion_log_{base_name}.txt")

                # 构建命令
                cmd = [
                    libreoffice_path,
                    "--headless",
                    "--convert-to", "pdf",
                    abs_file_path,
                    "--outdir", abs_output_dir
                ]

                # 在 Windows 上，使用 shell=True 可能更可靠
                use_shell = platform.system() == "Windows"

                # 执行命令，将输出重定向到日志文件
                with open(log_file, 'w') as log:
                    process = subprocess.Popen(
                        cmd,
                        stdout=log,
                        stderr=log,
                        shell=use_shell,
                        text=True
                    )

                    # 等待进程完成，设置超时
                    try:
                        process.wait(timeout=60)  # 60秒超时
                    except subprocess.TimeoutExpired:
                        process.kill()
                        raise Exception(f"转换超时: {os.path.basename(file)}")

                # 检查进程返回码
                if process.returncode != 0:
                    with open(log_file, 'r') as log:
                        error_output = log.read()
                    raise Exception(f"转换失败，返回码: {process.returncode}\n{error_output}")

                # 检查PDF是否实际生成
                expected_pdf = os.path.join(abs_output_dir, f"{base_name}.pdf")
                if not os.path.exists(expected_pdf):
                    raise Exception(f"PDF文件未生成: {expected_pdf}")

                self.update_status(f"已转换: {os.path.basename(file)} -> {base_name}.pdf")
                success_count += 1

                # 删除临时日志文件
                try:
                    os.remove(log_file)
                except:
                    pass

            except Exception as e:
                self.update_status(f"转换失败: {os.path.basename(file)}，错误信息: {str(e)}")

            # 更新进度条
            progress_percentage = ((idx + 1) / total) * 100
            self.progress_var.set(progress_percentage)
            self.master.update_idletasks()

        msg = f"转换完成，共转换 {success_count}/{total} 个文件！"
        self.update_status(msg)
        self.show_message("提示", msg)
