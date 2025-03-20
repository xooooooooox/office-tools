import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
from docxtpl import DocxTemplate

# 引入 court_match.py 中的功能
from court_match import (
    load_district_mapping,
    load_addresses,
    match_addresses_to_court,
    save_results_to_csv
)


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
        df = pd.read_excel(excel_path, dtype=str) # 将所有列都用字符串读入
        df.fillna("", inplace=True) # 把所欲欧 NaN 变成空字符串

        # 加载 Word 模板
        doc = DocxTemplate(template_path)

        # 行号计数，用于遇到空白文件名时兜底
        row_index = 0
        total = len(df)

        for idx, row in df.iterrows():
            # 构建字典，key=列名, value=单元格内容
            context = {}
            for col in df.columns:
                val = row[col]
                context[col] = row[col]

            # 渲染模板
            doc.render(context)

            # 文件名列  - 假设用 Excel 中 “文件名” 这一列作为输出名
            # 如果没有这个列，则自动根据 index 命名
            if "文件名" in df.columns and pd.notna(row["文件名"]):
                doc_name = str(row["文件名"])
            else:
                doc_name = f"output_{row_index}"

            row_index += 1

            # 输出路径
            save_path = os.path.join(output_dir, f"{doc_name}.docx")
            doc.save(save_path)

            # 每处理完一条，更新进度
            if progress_callback:
                progress_callback(idx + 1, total)

        return f"生成完毕，共处理 {total} 条记录！"

    except Exception as e:
        raise e


class GenerateTab(tk.Frame):
    """
    原先的批量生成 Word 的功能，放到一个独立的 Tab 里
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.template_path = ""
        self.excel_path = ""
        self.output_dir = ""

        self.create_widgets()

    def create_widgets(self):
        # 选择 Word 模板 按钮
        self.select_template_btn = tk.Button(self, text="选择 Word 模板", command=self.choose_template)
        self.select_template_btn.grid(row=0, column=0, padx=5, pady=5)

        self.template_label = tk.Label(self, text="未选择模板")
        self.template_label.grid(row=0, column=1, padx=5, pady=5)

        # 选择 Excel 按钮
        self.select_excel_btn = tk.Button(self, text="选择 Excel 数据", command=self.choose_excel)
        self.select_excel_btn.grid(row=1, column=0, padx=5, pady=5)

        self.excel_label = tk.Label(self, text="未选择 Excel")
        self.excel_label.grid(row=1, column=1, padx=5, pady=5)

        # 选择输出目录 按钮
        self.select_output_btn = tk.Button(self, text="选择输出目录", command=self.choose_output_dir)
        self.select_output_btn.grid(row=2, column=0, padx=5, pady=5)

        self.output_dir_label = tk.Label(self, text="未选择输出目录")
        self.output_dir_label.grid(row=2, column=1, padx=5, pady=5)

        # 进度条
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        # 一开始不显示，等点击“开始生成”再显示
        # self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # 生成 按钮
        self.generate_btn = tk.Button(self, text="开始生成", command=self.start_generate)
        self.generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # 状态输出区
        self.status_text = tk.Text(self, width=50, height=10)
        self.status_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def choose_template(self):
        path = filedialog.askopenfilename(
            title="选择 Word 模板",
            filetypes=[("Word 文件", "*.docx")],
        )
        if path:
            self.template_path = path
            self.template_label.config(text=os.path.basename(path))

    def choose_excel(self):
        path = filedialog.askopenfilename(
            title="选择 Excel 文件",
            filetypes=[("Excel 文件", "*.xlsx *.xls")],
        )
        if path:
            self.excel_path = path
            self.excel_label.config(text=os.path.basename(path))

    def choose_output_dir(self):
        dir_ = filedialog.askdirectory(title="选择输出目录")
        if dir_:
            self.output_dir = dir_
            self.output_dir_label.config(text=dir_)

    def start_generate(self):
        self.status_text.delete("1.0", tk.END)
        self.progress_var.set(0)

        if not (self.template_path and self.excel_path and self.output_dir):
            self.status_text.insert(tk.END, "请先选择 Word 模板、Excel 文件和输出目录！\n")
            return

        # 点击“开始生成”后再将进度条放到界面上
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        def progress_callback(current, total):
            progress_percentage = (current / total) * 100
            self.progress_var.set(progress_percentage)
            self.master.update_idletasks()

        try:
            msg = generate_docs(
                self.template_path,
                self.excel_path,
                self.output_dir,
                progress_callback=progress_callback
            )
            self.status_text.insert(tk.END, msg + "\n")
            messagebox.showinfo("提示", msg)
        except Exception as e:
            err_msg = f"生成失败：{e}"
            self.status_text.insert(tk.END, err_msg + "\n")
            messagebox.showerror("错误", err_msg)


class CourtMatchTab(tk.Frame):
    """
    新增的 '辖区法院匹配' 功能 Tab
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.mapping_file = ""
        self.address_file = ""
        self.output_file = ""

        self.create_widgets()

    def create_widgets(self):
        # 选取“区划 CSV”按钮
        self.select_mapping_btn = tk.Button(self, text="选取辖区法院明细 CSV", command=self.choose_mapping_file)
        self.select_mapping_btn.grid(row=0, column=0, padx=5, pady=5)

        self.mapping_label = tk.Label(self, text="未选择辖区法院明细 CSV")
        self.mapping_label.grid(row=0, column=1, padx=5, pady=5)

        # 选取“地址 TXT”按钮
        self.select_address_btn = tk.Button(self, text="选取地址明细 TXT", command=self.choose_address_file)
        self.select_address_btn.grid(row=1, column=0, padx=5, pady=5)

        self.address_label = tk.Label(self, text="未选择地址明细 TXT")
        self.address_label.grid(row=1, column=1, padx=5, pady=5)

        # 选取“输出 CSV”按钮
        self.select_output_btn = tk.Button(self, text="选择输出 CSV", command=self.choose_output_file)
        self.select_output_btn.grid(row=2, column=0, padx=5, pady=5)

        self.output_label = tk.Label(self, text="未选择输出文件")
        self.output_label.grid(row=2, column=1, padx=5, pady=5)

        # “开始匹配”按钮
        self.match_btn = tk.Button(self, text="开始匹配", command=self.start_match)
        self.match_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # 状态输出区
        self.status_text = tk.Text(self, width=50, height=10)
        self.status_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def choose_mapping_file(self):
        path = filedialog.askopenfilename(
            title="选取辖区法院明细 CSV 文件",
            filetypes=[("CSV文件", "*.csv")],
        )
        if path:
            self.mapping_file = path
            self.mapping_label.config(text=os.path.basename(path))

    def choose_address_file(self):
        path = filedialog.askopenfilename(
            title="选取地址明细 TXT 文件",
            filetypes=[("文本文件", "*.txt")],
        )
        if path:
            self.address_file = path
            self.address_label.config(text=os.path.basename(path))

    def choose_output_file(self):
        path = filedialog.asksaveasfilename(
            title="输出结果 CSV",
            filetypes=[("CSV 文件", "*.csv")],
            defaultextension=".csv"
        )
        if path:
            self.output_file = path
            self.output_label.config(text=os.path.basename(path))

    def start_match(self):
        # 每次点击前，清空状态信息
        self.status_text.delete("1.0", tk.END)

        if not (self.mapping_file and self.address_file and self.output_file):
            self.status_text.insert(tk.END, "请先选择辖区明细 CSV、地址明细 TXT 和输出 CSV 路径！\n")
            return

        try:
            # 1) 读取区划映射
            district_to_court_map = load_district_mapping(self.mapping_file)
            # 2) 读取地址
            addresses = load_addresses(self.address_file)
            # 3) 匹配
            matched_results = match_addresses_to_court(addresses, district_to_court_map)
            # 4) 保存
            save_results_to_csv(matched_results, self.output_file)

            msg = f"匹配完成，结果已写入 {self.output_file}"
            self.status_text.insert(tk.END, msg + "\n")
            messagebox.showinfo("提示", msg)
        except Exception as e:
            err_msg = f"匹配失败：{e}"
            self.status_text.insert(tk.END, err_msg + "\n")
            messagebox.showerror("错误", err_msg)


def main():
    root = tk.Tk()
    root.title("office-tools")
    root.geometry("600x400")

    # 用 Notebook 管理多个 Tab
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # 第一个 Tab：批量生成 Word
    generate_tab = GenerateTab(notebook)
    notebook.add(generate_tab, text="批量生成起诉状")

    # 第二个 Tab：辖区法院匹配
    court_match_tab = CourtMatchTab(notebook)
    notebook.add(court_match_tab, text="辖区法院匹配")

    root.mainloop()


if __name__ == "__main__":
    main()
