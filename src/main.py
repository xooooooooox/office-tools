import os
import tkinter as tk
from tkinter import ttk

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
    root = tk.Tk()
    root.title("office-tools")
    root.geometry("600x450")

    # 使窗口可调整大小时，内容也随之调整
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

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

    root.mainloop()


if __name__ == "__main__":
    main()
