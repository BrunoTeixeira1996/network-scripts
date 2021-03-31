import sys
import ipaddress


# get the VLSM network info
def getVLSMInfo() -> list:
    network_layout = []

    print("Type 'done' in the network_name input to stop the input")
    network_address = str(input('Network address: '))

    while True:
        network_name =  str(input('Name: '))
        if network_name == 'done':
            break
        network_host_number = int(input('Number of hosts: '))
        network_layout.append({
            'network_name' : network_name,
            'network_address' : network_address,
            'network_host_number' : network_host_number,
            'network_bits' : 0,
            'network_cidr' : 0,
            'network_subnetmask' : '',
            'network_subnetaddress' : '',
            'network_first_host' : '',
            'network_last_host' : '',
            'network_broadcast' : ''
        })

    # get the number of bits for every subnet
    getBitsSubnet(network_layout)

    # get the mask for every subnet
    getMaskSubnet(network_layout)

    # transform cidr mask to a original one
    transformMask(network_layout)
    return network_layout

# get how many bits every subnet needs
def getBitsSubnet(network: list):

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

# get the mask for every subnet
def getMaskSubnet(network: list):

    for i in network:
        i['network_cidr'] = 32 - i['network_bits']

# transform cidr to original mask
def transformMask(network: list):

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


# calculates the range for every subnet
def getRange(network: dict) -> int:
    return 256 - int(network['network_subnetmask'].split('.')[-1])

'''
ir buscar o range de cada subnet
ter uma flag para ver se é a primeira rede logo o subnet_address começa  no network_address
se for a primeira subnet, o subnet_address fica = 0
se for a primeira subnet, o first usable host fica = 1
se for a primeira subnet, o last usable host fica range - 2
se for a primeira subnet, o broadcast fica range -1


se nao for a primeira subnet, o subnet_address fica = broadcast anterior + 1
se nao for a primeira subnet, o first usable host fica = subnet_address + 1
se nao for a primeira subnet, o last usable host fica = range atual - 2
se nao for a primeira subnet, o broadcast fica range - 1
'''

'''
# calculates the range for every subnet
def getRange(network: dict) -> int:
    network_range = 256 - int(network['network_subnetmask'].split('.')[-1])
    last_octet = int(network['network_address'].split('.')[-1])

    # sum network_range + last_octect, convert to string, replace last octect from this result
    res = network_range + last_octet
    s = list(network['network_address'])
    s[-1] =  str(res - 1)
    network['network_broadcast'] = ''.join(s)
    print(network['network_broadcast'])

    return network
'''

# calculate the VLSM
def calcVLSM() -> str:
    #print(getVLSMInfo())
    for i in getVLSMInfo():
        print(getRange(i))


    return 'someting'

def main():
    if len(sys.argv) > 1:
        calcVLSM()
    else:
        print('bad input')


if __name__ == '__main__':
    main()
