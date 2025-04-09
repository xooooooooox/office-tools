import os
import platform
import sys
import tkinter as tk
import traceback
from tkinter import ttk, messagebox

import pandas as pd
from docxtpl import DocxTemplate

from conversion_tab import ConversionTab
# 引入 court_match.py 中的功能
from court_match import (
    load_district_mapping,
    load_addresses,
    match_addresses_to_court,
    save_results_to_csv
)
from court_match_tab import CourtMatchTab
# 引入自定义模块
from generate_tab import GenerateTab


def setup_exception_logging():
    """设置全局异常日志记录"""
    # 获取应用程序的数据目录
    if getattr(sys, 'frozen', False):
        # 如果是打包的应用程序
        app_dir = os.path.dirname(sys.executable)
    else:
        # 如果是直接运行的脚本
        app_dir = os.path.dirname(os.path.abspath(__file__))

    # 创建日志目录
    log_dir = os.path.join(app_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件路径
    log_file = os.path.join(log_dir, 'error.log')

    # 原始的异常处理函数
    original_hook = sys.excepthook

    # 新的异常处理函数
    def exception_handler(exc_type, exc_value, exc_traceback):
        # 记录到日志文件
        with open(log_file, 'a') as f:
            f.write(f"--- Exception: {exc_type.__name__} ---\n")
            f.write(f"Time: {pd.Timestamp.now()}\n")
            f.write(f"System: {platform.system()} {platform.release()}\n")
            f.write(f"Python: {sys.version}\n")
            f.write("Traceback:\n")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
            f.write("\n\n")

        # 调用原始的异常处理函数
        original_hook(exc_type, exc_value, exc_traceback)

    # 设置新的异常处理函数
    sys.excepthook = exception_handler


def generate_docs(template_path, excel_path, output_dir, progress_callback=None):
    """
    使用 docxtpl + pandas 批量生成 Word 文档。
    excel 的列名与模板 {{变量名}} 对应。
    progress_callback: 用于更新进度的回调函数，形式为 progress_callback(current, total)
    """
    try:
        if not os.path.isfile(template_path):
            raise FileNotFoundError("Word 模板文件不存在！")
        if not os.path.isfile(excel_path):
            raise FileNotFoundError("Excel 数据文件不存在！")
        if not os.path.isdir(output_dir):
            raise NotADirectoryError("输出目录不存在！")

        # 读取 Excel（假设第一行是标题行，列名对应模板中的变量）
        df = pd.read_excel(excel_path, dtype=str)  # 将所有列都以字符串方式读入
        df.fillna("", inplace=True)  # 将所有的 NaN 变成空字符串

        # 加载 Word 模板
        doc = DocxTemplate(template_path)

        # 行号计数，用于遇到空白文件名时兜底
        row_index = 0
        total = len(df)

        for idx, row in df.iterrows():
            # 构建 context 字典：key=列名, value=单元格内容
            context = {}
            for col in df.columns:
                context[col] = row[col]

            # 渲染模板
            doc.render(context)

            # 文件名列 —— 这里假设 Excel 中有 "文件名" 列，如果没有就用 index 命名
            if "文件名" in df.columns and pd.notna(row["文件名"]):
                doc_name = str(row["文件名"])
            else:
                doc_name = f"output_{row_index}"

            row_index += 1

            # 保存文件路径
            save_path = os.path.join(output_dir, f"{doc_name}.docx")
            doc.save(save_path)

            # 更新进度
            if progress_callback:
                progress_callback(idx + 1, total)

        return f"生成完毕，共处理 {total} 条记录！"

    except Exception as e:
        raise e


def main():
    """主程序入口"""
    # 设置异常日志记录
    setup_exception_logging()

    # 创建主窗口
    root = tk.Tk()
    root.title("office-tools")
    root.geometry("600x450")

    # 使窗口可调整大小时，内容也随之调整
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # Tab1: 批量生成起诉状
        generate_tab = GenerateTab(notebook, doc_generator=generate_docs)
        notebook.add(generate_tab, text="批量生成起诉状")

        # Tab2: 辖区法院匹配
        court_match_tab = CourtMatchTab(
            notebook,
            court_matcher=(load_district_mapping, load_addresses, match_addresses_to_court, save_results_to_csv)
        )
        notebook.add(court_match_tab, text="辖区法院匹配")

        # Tab3: 文件格式转换
        conversion_tab = ConversionTab(notebook)
        notebook.add(conversion_tab, text="文件格式转换")

        # 添加版本信息
        version_label = tk.Label(root, text="版本: 1.0.1", anchor="e")
        version_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        root.mainloop()
    except Exception as e:
        # 显示错误对话框
        error_msg = f"程序启动时发生错误: {str(e)}\n\n详细信息已记录到日志文件中。"
        messagebox.showerror("错误", error_msg)
        # 重新抛出异常以便记录到日志
        raise


if __name__ == "__main__":
    main()
