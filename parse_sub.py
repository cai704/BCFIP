import re, base64, sys, urllib.parse
from datetime import datetime, timezone, timedelta

provider = sys.argv[1]
target = sys.argv[2] if len(sys.argv) > 2 else "parsed.txt"


def extract(line):
    m = re.search(r'\{\s*name:\s*"([^"]*)"\s*,\s*server:\s*([^,\s]+)\s*,\s*port:\s*(\d+)', line)
    if m:
        return m.group(1), m.group(2), m.group(3)
    m = re.search(r'\{\s*name:\s*([^,]+?)\s*,\s*server:\s*([^,\s]+)\s*,\s*port:\s*(\d+)', line)
    if m:
        return m.group(1).strip(), m.group(2), m.group(3)
    return None


raw = open("raw_nodes.txt", "r", encoding="utf-8", errors="ignore").read()

nodes = []
for line in raw.splitlines():
    r = extract(line)
    if r:
        nodes.append((r[1], r[2], r[0]))

if not nodes:
    try:
        dec = base64.b64decode(re.sub(r"\s+", "", raw) + "==").decode("utf-8", "ignore")
        if dec and "<" not in dec[:200] and "proxies:" not in dec[:200]:
            raw = dec
    except Exception:
        pass
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        um = re.search(r'@\[?([0-9A-Fa-f:.]+)\]?:(\d+)', line)
        if um:
            nm = re.search(r'#(.*)$', line)
            nodes.append((um.group(1), um.group(2), urllib.parse.unquote(nm.group(1)) if nm else ""))
        else:
            m2 = re.match(r'^\[?([0-9A-Fa-f:.]+)\]?:(\d+)(?:#(.*))?$', line)
            if m2:
                nodes.append((m2.group(1), m2.group(2), m2.group(3) or ""))

seen = set()
rows = []
for server, port, name in nodes:
    s = server.strip("[]")
    if not re.match(r'^(\d{1,3}(\.\d{1,3}){3}|[0-9A-Fa-f:]+)$', s):
        continue
    key = f"{s}:{port}"
    if key in seen:
        continue
    seen.add(key)
    rows.append((key, name))

if len(rows) < 3:
    print(f"解析出 {len(rows)} 个节点，不足 3 个，拒绝写入")
    sys.exit(1)

CN = {
    "US": "美国", "GB": "英国", "UK": "英国", "RU": "俄罗斯", "DE": "德国",
    "MY": "马来西亚", "VN": "越南", "PH": "菲律宾", "TH": "泰国", "IN": "印度",
    "FR": "法国", "CA": "加拿大", "TR": "土耳其", "AU": "澳大利亚", "NL": "荷兰",
    "KR": "韩国", "HK": "香港", "SG": "新加坡", "JP": "日本", "TW": "台湾",
    "AE": "阿联酋", "ID": "印尼", "SA": "沙特", "BR": "巴西", "MX": "墨西哥",
    "IT": "意大利", "ES": "西班牙", "PL": "波兰", "SE": "瑞典", "CH": "瑞士",
    "CZ": "捷克", "UA": "乌克兰", "NZ": "新西兰", "ZA": "南非", "MO": "澳门",
    "PK": "巴基斯坦", "KH": "柬埔寨", "FI": "芬兰", "DK": "丹麦", "NO": "挪威",
    "IE": "爱尔兰", "PT": "葡萄牙", "AT": "奥地利", "BE": "比利时", "GR": "希腊",
    "RO": "罗马尼亚", "HU": "匈牙利", "EG": "埃及", "AR": "阿根廷", "CL": "智利",
}


def flag_to_cc(name):
    m = re.search(r'[\U0001F1E6-\U0001F1FF]{2}', name)
    if m:
        pair = m.group(0)
        return chr(ord(pair[0]) - 0x1F1E6 + 65) + chr(ord(pair[1]) - 0x1F1E6 + 65)
    return None


def region(name):
    cc = flag_to_cc(name)
    if cc and cc in CN:
        return f"{CN[cc]} {cc}"
    ccm = re.search(r'\b([A-Z]{2})\b', name)
    if ccm and ccm.group(1) in CN:
        cc = ccm.group(1)
        return f"{CN[cc]} {cc}"
    for cn, code in CN.items():
        if code == "UK" and "GB" in name:
            continue
        if cn in name:
            return f"{cn} {code}"
    return "未知"


def isp(name):
    if re.search(r'中国移动|移动', name):
        return "移动"
    if re.search(r'中国联通|联通', name):
        return "联通"
    if re.search(r'中国电信|电信', name):
        return "电信"
    return "未知"


def ipver(key):
    ip = key.rsplit(":", 1)[0]
    return "IPv6" if ":" in ip else "IPv4"


now = datetime.now(timezone(timedelta(hours=8))).strftime("%m-%d %H:%M")
out = [f"{rows[0][0]}#{provider}优选 | {now}"]
out += [f"{k}#{provider} | {region(n)} | {ipver(k)} | {isp(n)}" for k, n in rows]
out.append(f"{rows[-1][0]}#{provider}优选")

with open(target, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(f"解析成功，共 {len(rows)} 个节点")
