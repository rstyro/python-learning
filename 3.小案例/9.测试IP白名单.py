# 导入Python内置ipaddress模块，专门用于IPv4/IPv6地址、网段解析和包含判断
import ipaddress

# IP白名单列表，支持单个IP(如/32)和CIDR网段(如/27、/24)格式
IP_WHITELIST = [
    "120.197.107.96/27",
    "183.237.254.192/27",
    "183.238.11.130/32",
    "211.25.36.84/32",
    "223.118.32.142/32",
    "223.119.168.0/24",
]

# 预解析所有CIDR为ipaddress网络对象
# strict=False：允许网段写法不是严格网络起始地址（比如1.2.3.4/24也能正常识别成1.2.3.0/24）
IP_NETWORKS = [ipaddress.ip_network(c, strict=False) for c in IP_WHITELIST]

def in_whitelist(ip):
    """
    判断源 IP 是否命中 IP 白名单（CIDR 网段匹配）
    :param ip: 待检测IP字符串，如"223.119.168.100"
    :return: bool，True=在白名单内；False=不在/IP格式非法
    规则：空值、格式错误的IP直接返回False
    """
    # 空IP直接判定不在白名单
    if not ip:
        return False
    try:
        # 把字符串转为IP地址对象，格式非法会抛ValueError
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # 不是合法IPv4/IPv6，直接返回False
        return False
    # 遍历所有白名单网段，只要任意一个网段包含该IP就返回True
    return any(addr in net for net in IP_NETWORKS)


print(in_whitelist("223.119.168.100"))
print(in_whitelist("223.119.168.10"))
print(in_whitelist("223.118.32.143"))


# 测试CIDR

net = ipaddress.ip_network("120.197.107.96/32", strict=False)
print("32网段范围:", net[0], "~", net[-1])
print("掩码:", net.netmask)

net = ipaddress.ip_network("120.197.107.96/31", strict=False)
print("31网段范围:", net[0], "~", net[-1])
print("掩码:", net.netmask)

net = ipaddress.ip_network("120.197.107.96/27", strict=False)
print("27网段范围:", net[0], "~", net[-1])
print("掩码:", net.netmask)


net = ipaddress.ip_network("120.197.107.96/24", strict=False)
print("24网段范围:", net[0], "~", net[-1])
print("掩码:", net.netmask)


net = ipaddress.ip_network("120.197.107.96/16", strict=False)
print("16网段范围:", net[0], "~", net[-1])
print("掩码:", net.netmask)