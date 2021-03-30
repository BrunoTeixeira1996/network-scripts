import ipaddress
import sys


def subnets(ip_address):
    try:
        ip = ipaddress.IPv4Network(ip_address, strict=False)    # strict has to be false to work with IP's and networks
        firstoctet = int(str(ip).split('.')[0])  #split the IP and grab the first octet to work with

        if firstoctet == 0:
            print('Default IP')

        elif firstoctet >= 1 and firstoctet <= 126:
            print('Class A {1. - 126.}')

        elif firstoctet == 127:
           return print('This is the Loopback')

        elif firstoctet >= 128 and firstoctet <= 191:
            print('Class B {128. - 191.}')

        elif firstoctet >= 192 and firstoctet <= 223:
            print('Class C {192. - 223.}')

        elif firstoctet >= 224 and firstoctet <= 239:
            print('Class D {224. - 239.}')

        else:
            print('Class E {240. - .254}')

    except ipaddress.AddressValueError:
        return print('Please type a  valid IP')
    except ipaddress.NetmaskValueError:
        return print('Please type a valid NetMask')


    print('Network: ', ip.with_netmask)
    print('Broadcast:  ', ip.broadcast_address)
    print('Start IP: ', ip.network_address + 1) # +1 because the first one belongs to the network
    print('Finish IP: ', ip.broadcast_address - 1)  # -1 because the last one belongs to the broadcast
    print('Number max of hosts: ', ip.num_addresses - 2) # -2 because the network and broadcast addresses doesnt count


def main():

    if len(sys.argv) > 1:
        subnets(sys.argv[1])
    else:
        print('Usage : subnetcal.py IP/CIDR')

if __name__ == ('__main__'):
    main()
