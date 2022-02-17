import scapy

def binary_to_quad(binary):
    out = ''
    for i in range(0,25,8):
        out += str(int(binary[i:i+8],2)) + '.'
    return out[:-1]

def quad_to_binary(quad):
    pieces = quad.split('.')
    out = ''
    for piece in pieces:
        out += decimalToBinary(int(piece),8)
    return out

def decimalToBinary(n,size=None):
    if size:
        val = bin(n).replace("0b", "")
        out = ''
        for _ in range(size-len(val)):
            out += '0'
        return out + val
    return bin(n).replace("0b", "")

#data = '192.168.100.0/24'
data = input("Enter ip in CIDR Notation: ")

slash = data.rfind('/')
replacable_limit = 2**(32-int(data[slash+1:]))

base_ip = data[:slash]
cidr = int(data[slash+1:])
#print(cidr)

subnet_binary = ''

for _ in range(cidr):
    subnet_binary += '1'

ones = subnet_binary[:]

for _ in range(cidr,32):
    subnet_binary += '0'

subnet_mask = binary_to_quad(subnet_binary)
#print(subnet_mask)

net_id = ''
net_id_cut = ''
binary_base_ip = quad_to_binary(base_ip)
for i in range(len(subnet_binary)):
    if subnet_binary[i] == '1' and binary_base_ip[i] == '1':
        net_id += '1'
        if i < cidr:
            net_id_cut += '1'
    else:
        net_id += '0'
        if i < cidr:
            net_id_cut += '0'

ips = []
for i in range(replacable_limit):
    ips.append(binary_to_quad(net_id_cut + decimalToBinary(i,32-cidr)))

print("Net ID:", binary_to_quad(net_id))
print("Subnet Mask:", subnet_mask)
print("Host IP Range:", ips[1], "to", ips[-2])
