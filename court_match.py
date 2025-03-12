import csv
import re

def load_district_mapping(mapping_file):
    """
    从类似于:
    
        基层人民法院,管辖区域
        北京市东城区人民法院,"东城区、通州区、顺义区、怀柔区、平谷区、密云区"
        北京市西城区人民法院,西城区、大兴区
        北京市朝阳区人民法院,朝阳区
        ...
    
    的文件中读取映射。
    
    最终返回一个 dict，如:
    {
      "东城区": "北京市东城区人民法院",
      "通州区": "北京市东城区人民法院",
      "顺义区": "北京市东城区人民法院",
      "怀柔区": "北京市东城区人民法院",
      "平谷区": "北京市东城区人民法院",
      "密云区": "北京市东城区人民法院",
      "西城区": "北京市西城区人民法院",
      "大兴区": "北京市西城区人民法院",
      "朝阳区": "北京市朝阳区人民法院",
      "海淀区": "北京市海淀区人民法院",
      ...
    }
    """
    district_to_court = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            court_name = row["基层人民法院"].strip()  # 例如 "北京市东城区人民法院"
            region_str = row["管辖区域"].strip()      # 例如 "东城区、通州区、顺义区、怀柔区、平谷区、密云区"

            # 将可能的引号去掉（如果 CSV 某些字段带了引号）
            region_str = region_str.strip('"').strip("'")

            # 拆分成单独区名
            # 假设使用中文顿号 "、" 或英文逗号 "," 或混合为分隔符时：
            # 这里我们优先匹配中文顿号，也做一个冗余替换，把英文逗号也替换成中文顿号再分
            region_str = region_str.replace(",", "、")
            region_list = [r.strip() for r in region_str.split("、") if r.strip()]

            for district in region_list:
                district_to_court[district] = court_name
    
    return district_to_court

def load_addresses(address_file):
    """
    从 address_list.txt 逐行读取地址
    """
    addresses = []
    with open(address_file, 'r', encoding='utf-8') as f:
        for line in f:
            address = line.strip()
            if address:
                addresses.append(address)
    return addresses

def match_addresses_to_court(addresses, district_to_court):
    """
    根据 district_to_court 映射，对地址进行批量匹配。
    如果地址中包含某个区名(如 "东城区")，返回映射的法院；否则返回 "无"。
    
    注意：
    - 脚本假设地址中必定含 "xx区" 字样才能匹配，比如 "朝阳区"、"海淀区" 等。
    - 如果一个地址里出现多个区名，按需求可做自定义处理。
      这里假设一个地址只会匹配到一个区(或第一个匹配到的区)。
    """
    if not district_to_court:
        return [(addr, "无") for addr in addresses]
    
    # 构造正则：将所有可能出现的区名用 “|” 拼接
    # 例如 "东城区|通州区|顺义区|怀柔区|平谷区|密云区|西城区|..."
    pattern_keys = list(district_to_court.keys())
    pattern = re.compile("|".join(re.escape(k) for k in pattern_keys))

    results = []
    for addr in addresses:
        match = pattern.search(addr)
        if match:
            matched_district = match.group(0)  # 如 "东城区"
            court = district_to_court.get(matched_district, "无")
        else:
            court = "无"
        results.append((addr, court))
    return results

def save_results_to_csv(results, output_file):
    """
    将 (地址, 法院) 列表写入 CSV 文件
    """
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写表头
        writer.writerow(["Address", "Court"])
        # 写数据
        for addr, court in results:
            writer.writerow([addr, court])

if __name__ == "__main__":
    # 1) 根据实际文件路径进行修改
    mapping_file = "district_mapping.csv"   # 包含 “基层人民法院,管辖区域” 两列
    address_file = "address_list.txt"       # 每行一个地址
    output_file = "match_results.csv"       # 输出结果文件
    
    # 2) 读取法院-管辖区域映射
    district_to_court_map = load_district_mapping(mapping_file)

    # 3) 读取地址
    addresses = load_addresses(address_file)

    # 4) 批量匹配
    matched_results = match_addresses_to_court(addresses, district_to_court_map)

    # 5) 结果输出到 CSV
    save_results_to_csv(matched_results, output_file)
    print(f"匹配完成，结果已写入 {output_file}")