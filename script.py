import sys
import ipaddress


# get the VLSM network info
def getVLSMInfo() -> dict:
    network_layout = {}
    print("Type 'done' in the network_name input to stop the input")

    while True:
        network_name =  str(input('Name: '))
        if network_name == 'done':
            break
        network_host_number = int(input('Number of hosts: '))
        network_layout[network_name] = network_host_number

    return network_layout

# get how many bits every subnet needs
def getBitsSubnet(network: dict) -> dict:
    network_bits = network

    #fill bits for every subnet
    for i in network:
        if network[i] == 1:
            network_bits[i] = 0
        elif network[i] == 2:
            network_bits[i] = 2
        elif network[i] >= 3 and network[i] <= 6:
            network_bits[i] = 3
        elif network[i] >= 7 and network[i] <= 14:
            network_bits[i] = 4
        elif network[i] >= 15 and network[i] <= 30:
            network_bits[i] = 5
        elif network[i] >= 31 and network[i] <= 62:
            network_bits[i] = 6
        elif network[i] >= 63 and network[i] <= 126:
            network_bits[i] = 7
        elif network[i] >= 127 and network[i] <= 254:
            network_bits[i] = 8
        elif network[i] >= 255 and network[i] <= 510:
            network_bits = 9
        elif network[i] >= 511 and network[i] <= 1022:
            network_bits = 10

    return network_bits

# get the mask for every subnet
def getMaskSubnet(network_bits: dict) -> dict:
    network_mask = network_bits
    for i in network_bits:
        network_mask[i] = 32 - network_mask[i]

    return network_mask

# transform /mask to original mask
def transformMask(network_mask: dict) -> dict:
    network_original = network_mask
    for i in network_mask:
        if network_mask[i] == 24:
            network_original[i] = 0
        elif network_mask[i] == 25:
            network_original[i] = '255.255.255.128'
        elif network_mask[i] == 26:
            network_original[i] = '255.255.255.192'
        elif network_mask[i] == 27:
            network_original[i] = '255.255.255.224'
        elif network_mask[i] == 28:
            network_original[i] = '255.255.255.240'
        elif network_mask[i] == 29:
            network_original[i] = '255.255.255.248'
        elif network_mask[i] == 30:
            network_original[i] = '255.255.255.252'
        elif network_mask[i] == 31:
            network_original[i] = '255.255.255.254'
        elif network_mask[i] == 32:
            network_original[i] = '255.255.255.255'

    return network_original

# calculate the VLSM
def calcVLSM() -> str:
    network_unsorted = getVLSMInfo()

    # rearrange networks with more hosts
    network_sorted = dict(sorted(network_unsorted.items(), key = lambda i : i[1], reverse=True))

    # get the number of bits for every subnet
    network_bits = getBitsSubnet(network_sorted)

    # get the mask for every subnet
    network_mask = getMaskSubnet(network_bits)
    network_original_mask = transformMask(network_mask)

    # get the range for a specific subnet (256 - network_mask last octet)



    print(network_original_mask)


def main():
    if len(sys.argv) > 1:
        calcVLSM()
    else:
        print('bad input')

if __name__ == '__main__':
    main()
