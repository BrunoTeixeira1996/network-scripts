import sys
import ipaddress


# get the VLSM network info
def getVLSMInfo() -> list:
    network_layout = []

    print("Type 'done' in the network_name input to stop the input")

    while True:
        network_name =  str(input('Name: '))
        if network_name == 'done':
            break
        network_host_number = int(input('Number of hosts: '))
        network_layout.append({
            'network_name' : network_name,
            'network_host_number' : network_host_number,
            'network_bits' : 0,
            'network_cidr' : 0,
            'network_subnetmask' : ''
        })

    return network_layout

# get how many bits every subnet needs
def getBitsSubnet(network: list) -> list:

    for i in network:
        if i['network_host_number'] == 1:
            i['network_bits'] = 0
        elif i['network_host_number'] == 2:
            i['network_bits'] = 2
        elif i['network_host_number'] >= 3 and i['network_host_number'] <= 6:
            i['network_bits'] = 3
        elif i['network_host_number'] >= 7 and i['network_host_number'] <= 14:
            i['network_bits'] = 4
        elif i['network_host_number'] >= 15 and i['network_host_number'] <= 30:
            i['network_bits'] = 5
        elif i['network_host_number'] >= 31 and i['network_host_number'] <= 62:
            i['network_bits'] = 6
        elif i['network_host_number'] >= 63 and i['network_host_number'] <= 126:
            i['network_bits'] = 7
        elif i['network_host_number'] >= 127 and i['network_host_number'] <= 254:
            i['network_bits'] = 8
        elif i['network_host_number'] >= 255 and i['network_host_number'] <= 510:
            i['network_bits'] = 9
        elif i['network_host_number'] >= 511 and i['network_host_number'] <= 1022:
            i['network_bits'] = 10
    return network

# get the mask for every subnet
def getMaskSubnet(network: list) -> list:

    for i in network:
        i['network_cidr'] = 32 - i['network_bits']

    return network

# transform cidr to original mask
def transformMask(network: list) -> list:

    for i in network:
        if i['network_cidr'] == 24:
            i['network_subnetmask'] = '255.255.255.0'
        elif i['network_cidr'] == 25:
            i['network_subnetmask'] = '255.255.255.128'
        elif i['network_cidr'] == 26:
            i['network_subnetmask'] = '255.255.255.192'
        elif i['network_cidr'] == 27:
            i['network_subnetmask'] = '255.255.255.224'
        elif i['network_cidr'] == 28:
            i['network_subnetmask'] = '255.255.255.240'
        elif i['network_cidr'] == 29:
            i['network_subnetmask'] = '255.255.255.248'
        elif i['network_cidr'] == 30:
            i['network_subnetmask'] = '255.255.255.252'
        elif i['network_cidr'] == 31:
            i['network_subnetmask'] = '255.255.255.254'
        elif i['network_cidr'] == 32:
            i['network_subnetmask'] = '255.255.255.255'
    return network

# calculate the VLSM
def calcVLSM() -> str:
    subnets = getVLSMInfo()

    # get the number of bits for every subnet
    network_bits = getBitsSubnet(subnets)

    # get the mask for every subnet
    network_mask = getMaskSubnet(network_bits)
    network_original_mask = transformMask(network_mask)

    # get the range for a specific subnet (256 - network_mask last octet)
    #fazer um dicionario para cada subrede


    print(network_original_mask)


def main():
    if len(sys.argv) > 1:
        calcVLSM()
    else:
        print('bad input')


if __name__ == '__main__':
    main()
