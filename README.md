# autoscanner.py
Automates scanning with masscan and importing the results into nmap. It will initiate a masscan and once the scan is complete it takes the open ports and scans them with nmap to gather more in-depth information

~~~python
usage: autoscanner.py [-h] -i IP [-n NMAP] [-m MASSCAN] [-o OUTFILE]

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP address of the host, can be a range or a file containing the IPs
  -n NMAP, --nmap NMAP  NMAP scan options to override the default options
  -m MASSCAN, --masscan MASSCAN
                        Masscan options to override the default options
~~~

