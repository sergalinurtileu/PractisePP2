import re
import json
file_path = "raw.txt"
def parse_pharmacy_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
       text = f.read()

    
    date_time = re.search(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    
    
    total = re.search(r"ИТОГО:\s+([\d\s,]+)", text)

   
    payment = re.search(r"(Банковская карта|Наличные)", text)

   
    item_pattern = re.compile(r"(\d+)\.\n(.*?)\n.*?\n([\d\s,]+)\nСтоимость", re.DOTALL)
    items = item_pattern.findall(text)

    parsed_items = []
    for item in items:
        parsed_items.append({
            "id": item[0],
            "name": item[1].strip().replace('\n', ' '),
            "line_price": item[2].strip()
        })

    result = {
        "metadata": {
            "date": date_time.group(1) if date_time else None,
            "time": date_time.group(2) if date_time else None,
            "payment_method": payment.group(0) if payment else "Unknown"
        },
        "products": parsed_items,
        "total_sum": total.group(1).strip() if total else "0"
    }

    return result

parsed_data = parse_pharmacy_receipt('raw.txt')
print(json.dumps(parsed_data, indent=4, ensure_ascii=False))