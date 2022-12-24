import re,sys,argparse
from subprocess import PIPE,Popen

def init_masscan(ip):
    if ip.count('.') == 3:
        ipcheck = ip.split('.')
        count = 0
        for each in ipcheck:
            if int(each) > 255:
                count += 1
        if count > 0:
            print('IP address is invalid, please provide a valid IP')
            sys.exit()
    if args.masscan != None:
        masscan_options = args.masscan
    else:
        masscan_options = '-p0-65535 --rate 1000'
    command = 'sudo masscan {} {}'.format(ip,masscan_options)
    print("Scanning with the following command: {}".format(command))
    proc = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
    results,error = proc.communicate()
    results = results.decode().split('\n')
    ports = set()
    proto = set()
    hosts = set()
    for each in results:
        regex = re.search(r'port ([\d]{1,5})/(tcp|udp) on ([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})', each)
        if regex != None:
            ports.add(regex.groups()[0])
            proto.add(regex.groups()[1])
            hosts.add(regex.groups()[2])
            print(regex.groups()[1].upper(),"Port",regex.groups()[0],"Discovered on",regex.groups()[2])
            
        else:
            continue
    
    init_nmapscan(ports,hosts,proto)

def init_nmapscan(ports,hosts,proto):
    print("\nImporting hosts and ports into nmap")
    ports = ",".join(ports)
    hosts = ",".join(hosts)
    proto = list(proto)
    tcp = proto.count('tcp')
    udp = proto.count('udp')
    if args.nmap != None:
        nmap_options = args.nmap + ' -p {} {}'.format(ports,hosts)
    else:
        if tcp == 1 and udp == 1:
            nmap_options = '-sTUVC -p {} {} --open -Pn'.format(ports,hosts)
        elif tcp == 1 and udp == 0:
            nmap_options = '-sTVC -p {} {} --open -Pn'.format(ports,hosts)
        elif tcp == 0 and udp == 1:
            nmap_options = '-sUVC -p {} {} --open -Pn'.format(ports,hosts)
        else:
            print('No protocol detected...exiting')
            sys.exit()
    command = 'sudo nmap {}'.format(nmap_options)
    print("\nScanning with the following command: {}".format(command))
    proc = Popen(command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
    results,error = proc.communicate()
    print(results.decode())

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--ip',help='IP address of the host, can be a range or a file containing the IPs',required=True,action='store')
    parser.add_argument('-n','--nmap',help='NMAP scan options to override the default options',required=False,action='store')
    parser.add_argument('-m','--masscan',help='Masscan options to override the default options',required=False,action='store')
    parser.add_argument('-o','--outfile',help='Output file which gets written to by both nmap',required=False,action='store')

    args = parser.parse_args()

    ip = args.ip
      
    
    init_masscan(ip)
