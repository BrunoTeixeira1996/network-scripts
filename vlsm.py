import sys


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
            'network_first_host' : 0,
            'network_last_host' : 0,
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


# calculates the range of a subnet
def getRange(network: dict) -> int:
    return 256 - int(network['network_subnetmask'].split('.')[-1])


# sums last octect with an int and returns str -> used in subnetaddress and broadcast
def sumStringInt(string: str, number: int) -> str:
    aux = str(int(string.split('.')[-1]) + number)
    return string.replace(string.split('.')[-1],aux)


# sums last octect with an int and returns int -> used in first_host and last_host
def sumIntString(string: str, number: int) -> int:
    return  int(string.split('.')[-1]) + number


# gets info for the first network
def getFirstNetwork(network: dict):

    network['network_subnetaddress'] = network['network_address']
    network['network_first_host'] = sumIntString(network['network_subnetaddress'],1)
    network['network_last_host'] = getRange(network) - 2
    network['network_broadcast'] = sumStringInt(network['network_subnetaddress'], getRange(network) - 1)

# gets info for the remainder networks
def getRemainderNetwork(network: list):

    for idx, val in enumerate(network):
        if idx == 0:
            pass
        else:
            val['network_subnetaddress'] = sumStringInt(network[idx-1]['network_broadcast'], 1)
            val['network_first_host'] = sumIntString(val['network_subnetaddress'],1)
            val['network_last_host'] = val['network_first_host'] + getRange(val) - 3
            val['network_broadcast'] = sumStringInt(val['network_subnetaddress'], getRange(val) - 1)


# calculate the VLSM
def calcVLSM():
    flag = False
    vlsm = getVLSMInfo()

    for i in vlsm:
        # its the first subnet
        if flag == False:
            getFirstNetwork(i)
            flag = True
        # its not the first subnet
        else:
            getRemainderNetwork(vlsm)
    showOutput(vlsm)

def showOutput(network: list):
    for i in network:
        print(f'''

        network_name : {i['network_name']}
        network_address : {i['network_address']}
        network_host_number : {i['network_host_number']}
        network_bits : {i['network_bits']}
        network_cidr : {i['network_cidr']}
        network_subnetmask : {i['network_subnetmask']}
        network_subnetaddress : {i['network_subnetaddress']}
        network_first_host : {i['network_first_host']}
        network_last_host : {i['network_last_host']}
        network_broadcast : {i['network_broadcast']}
        ''')



def main():
    calcVLSM()

if __name__ == '__main__':
    main()
