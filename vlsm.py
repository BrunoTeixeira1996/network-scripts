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


# calculates the range for every subnet
def getRange(network: dict) -> int:
    return 256 - int(network['network_subnetmask'].split('.')[-1])

'''
ir buscar o range de cada subnet
ter uma flag para ver se é a primeira rede logo o subnet_address começa  no network_address
se for a primeira subnet, o network_address fica = 0
se for a primeira subnet, o first usable host fica = 1
se for a primeira subnet, o last usable host fica range - 2
se for a primeira subnet, o broadcast fica range -1


se nao for a primeira subnet, o network_address fica = broadcast anterior + 1
se nao for a primeira subnet, o first usable host fica = subnet_address + 1
se nao for a primeira subnet, o last usable host fica = range atual - 2
se nao for a primeira subnet, o broadcast fica range - 1
'''

# gets the Broadcast, first usable host, last usable host and subnet address
def getLastInfo(network: dict):

    network['network_first_host'] = 1
    network['network_last_host'] = getRange(network) - 2
    last_octet = int(network['network_address'].split('.')[-1])
    res = getRange(network) + last_octet
    s = list(network['network_address'])
    s[-1] = str(res - 1)
    network['network_broadcast'] = ''.join(s)
    network['network_subnetaddress'] = network['network_address']

# sums last octect with an int and returns str
def sumStringInt(string: str, number: int) -> str:
    s = list(string)
    s[-1] = str(number + int(s[-1]))
    return ''.join(s)

# sums last octect with an int and returns int
def sumIntString(string: str, number: int) -> int:
    return  int(string.split('.')[-1]) + number

def sumIntStringAux(string: str, number: int) -> int:

    #split every octect but the last one
    splited_string = string.split('.')[:-1]
    #joined every octect with dots
    result_string = '.'.join(splited_string)
    #result is the sum of the last octect + the range of the network
    result = str(int(string.split('.')[-1]) + number)


    return result_string + '.' + result


def getLol(network: list):

    for idx, val in enumerate(network):
        if idx == 0:
            pass
        else:
            val['network_subnetaddress'] = sumStringInt(network[idx-1]['network_broadcast'], 1)
            val['network_first_host'] = sumIntString(val['network_subnetaddress'],1)
            val['network_last_host'] = val['network_first_host'] + getRange(val) - 3
            val['network_broadcast'] = sumIntStringAux(val['network_subnetaddress'], getRange(val) - 1)


# calculate the VLSM
def calcVLSM():
    flag = False
    vlsm = getVLSMInfo()

    for i in vlsm:
        # its the first subnet
        if flag == False:
            getLastInfo(i)
            flag = True
        # its not the first subnet
        else:
            getLol(vlsm)
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
    if len(sys.argv) > 1:
        calcVLSM()
    else:
        print('bad input')


if __name__ == '__main__':
    main()


'''
BUG ao passar de "network_broadcast":"222.37.34.239" para o "network_subnetaddress":"222.37.34.2310",
BUG tambem aqui  "network_broadcast":"222.37.34.2317"

'''
