import os
from tkinter import filedialog

from base_tab import BaseTab


class CourtMatchTab(BaseTab):
    """
    "辖区法院匹配"功能 Tab
    """

    def __init__(self, master=None, court_matcher=None):
        super().__init__(master)
        self.master = master
        self.court_matcher = court_matcher

        self.mapping_file = ""
        self.address_file = ""
        self.output_file = ""

        self.create_widgets()

    def create_widgets(self):
        """创建UI组件"""
        # 选取"区划 CSV"按钮
        self.mapping_btn, self.mapping_label, _ = self.create_file_selector(
            row=0,
            button_text="选取辖区法院明细 CSV",
            label_text="未选择辖区法院明细 CSV",
            command=self.choose_mapping_file,
            file_types=[("CSV文件", "*.csv")]
        )

        # 选取"地址 TXT"按钮
        self.address_btn, self.address_label, _ = self.create_file_selector(
            row=1,
            button_text="选取地址明细 TXT",
            label_text="未选择地址明细 TXT",
            command=self.choose_address_file,
            file_types=[("文本文件", "*.txt")]
        )

        # 选取"输出 CSV"按钮
        self.output_btn, self.output_label, _ = self.create_file_selector(
            row=2,
            button_text="选择输出 CSV",
            label_text="未选择输出文件",
            command=self.choose_output_file
        )

        # "开始匹配"按钮
        self.match_btn = self.create_action_button(
            row=3,
            text="开始匹配",
            command=self.start_match
        )

        # 状态输出区
        self.status_text = self.create_status_area(row=4)

    def choose_mapping_file(self):
        """选择辖区法院明细CSV文件"""
        path = filedialog.askopenfilename(
            title="选取辖区法院明细 CSV 文件",
            filetypes=[("CSV文件", "*.csv")]
        )
        if path:
            self.mapping_file = path
            self.mapping_label.config(text=os.path.basename(path))

    def choose_address_file(self):
        """选择地址明细TXT文件"""
        path = filedialog.askopenfilename(
            title="选取地址明细 TXT 文件",
            filetypes=[("文本文件", "*.txt")]
        )
        if path:
            self.address_file = path
            self.address_label.config(text=os.path.basename(path))

    def choose_output_file(self):
        """选择输出CSV文件"""
        path = filedialog.asksaveasfilename(
            title="输出结果 CSV",
            filetypes=[("CSV 文件", "*.csv")],
            defaultextension=".csv"
        )
        if path:
            self.output_file = path
            self.output_label.config(text=os.path.basename(path))

    def start_match(self):
        """开始匹配处理"""
        self.update_status("", clear=True)

        if not (self.mapping_file and self.address_file and self.output_file):
            self.update_status("请先选择辖区明细 CSV、地址明细 TXT 和输出 CSV 路径！")
            return

        try:
            # 执行匹配操作
            load_district_mapping, load_addresses, match_addresses_to_court, save_results_to_csv = self.court_matcher

            # 1) 读取区划映射
            district_to_court_map = load_district_mapping(self.mapping_file)
            # 2) 读取地址
            addresses = load_addresses(self.address_file)
            # 3) 匹配
            matched_results = match_addresses_to_court(addresses, district_to_court_map)
            # 4) 保存
            save_results_to_csv(matched_results, self.output_file)

            msg = f"匹配完成，结果已写入 {self.output_file}"
            self.update_status(msg)
            self.show_message("提示", msg)
        except Exception as e:
            err_msg = f"匹配失败：{e}"
            self.update_status(err_msg)
            self.show_message("错误", err_msg, error=True)
