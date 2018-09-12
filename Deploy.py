#!/usr/bin/python

import paramiko
import socket
import time
from os import system
from ipaddress import ip_address

def check_ip():
    system('cls')
    print(180 * '-' + '\n')
    ip_add = input('Please enter the ip-address of your server: ')
    try:
        ip_address(ip_add)
    except ValueError:
        ip_add = input('Please enter IP-address in like format XXX.XXX.XXX.XXX where XXX is number between 0 and 255: ')
    print('Your IP-address: '+(ip_add))
    print('Now I will be check the accessibility of your server for work!\n')
    print(180 * '-' + '\n')
    return(ip_add)

	

def deploy_proxy(ip_add):
    system('cls')
    print(180 * '-' + '\n')
    print('IP-address you entered is workless.')
    print('Now we will deploy proxy server SQUID to your server with Linux CentOS!')
    print('ATTENTION! This script can work only with Linux CentOS 7!\n')
    print(180 * '-' + '\n')
    passwd = input(
        "Please enter the password for make SSH connection to your server: ")
    while(passwd == ''):
        passwd = input(
            "You should definitely ENTER the password for make SSH connection to your server : ")
    proxy_login = input(
        "Please enter the login name for connect to proxy-server [default - test]: ")
    if(proxy_login == ''):
        proxy_login = 'test'
    proxy_password = input(
        "Please enter the password for connect to proxy-server [default - test]: ")
    if(proxy_password == ''):
        proxy_password = 'test'
    proxy_port = input(
        "Please enter the port for proxy-server [default - 3128]: ")
    if(proxy_port == ''):
        proxy_port = '3128'
    print(180 * '-' + '\n')
    print('%20s' % (
        "Now we will deploy the proxy-server SQUID into the server with IP-address " + ip_add + " !\n"))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip_add, username='root',
                   password=passwd)
    stdin, stdout, stderr = client.exec_command("yum -y update")
    print('Updating your CentOS: ', end='', flush=True)
    while not stdout.channel.exit_status_ready():
        print('.', end='', flush=True)
        time.sleep(1)
    print('OK')
    client.close()
    client.connect(hostname=ip_add, username='root',
                   password=passwd)
    stdin, stdout, stderr = client.exec_command(
        "yum -y install squid; yum -y install httpd-tools; rm -f /etc/squid/squid.conf; touch /etc/squid/squid.conf; htpasswd -cb /etc/squid/users " + proxy_login + " " + proxy_password + "; echo 'auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/users\nauth_param basic realm =NoName Proxy-Server=\nauth_param basic credentialsttl 8 hours\n\nacl localhost src 127.0.0.1/32 ::1\nacl users proxy_auth REQUIRED\nacl SSL_ports port 443\nacl Safe_ports port 80          # http\nacl Safe_ports port 21          # ftp\nacl Safe_ports port 443         # https\nacl Safe_ports port 70          # gopher\nacl Safe_ports port 210         # wais\nacl Safe_ports port 1025-65535  # unregistered ports\nacl Safe_ports port 280         # http-mgmt\nacl Safe_ports port 488         # gss-http\nacl Safe_ports port 591         # filemaker\nacl Safe_ports port 777         # multiling http\nacl CONNECT method CONNECT\n\nhttp_access allow manager localhost\nhttp_access deny manager\n\nhttp_access deny !Safe_ports\nhttp_access deny CONNECT !SSL_ports\nhttp_access allow localhost\nhttp_access deny !users\nhttp_port " + proxy_port + "\n\ncoredump_dir /var/spool/squid3\n\nrefresh_pattern ^ftp:           1440    20%     10080\nrefresh_pattern ^gopher:        1440    0%      1440\nrefresh_pattern -i (/cgi-bin/|\?) 0     0%      0\nrefresh_pattern .               0       20%     4320\nacl my_ip_" + ip_add + " myip " + ip_add + "\ntcp_outgoing_address " + ip_add + " my_ip_" + ip_add + "' > /etc/squid/squid.conf")
    print('\nInstalling the tools and SQUID3: ', end='', flush=True)
    while not stdout.channel.exit_status_ready():
        print('.', end='', flush=True)
        time.sleep(1)
    print('OK')
    client.close()
    client.connect(hostname=ip_add, username='root',
                   password=passwd)
    stdin, stdout, stderr = client.exec_command("systemctl enable squid; systemctl start squid")
    print('\nRunning the SQUID3: ', end='', flush=True)
    while not stdout.channel.exit_status_ready():
        print('.', end='', flush=True)
        time.sleep(1)
    print('OK')
    client.close()
    file = open("proxy.txt", "a")
    file.write(ip_add + ":" + proxy_port + ":" +
               proxy_login + ":" + proxy_password + "\n")
    file.close()
    print('\n' + 180 * '-' + '\n')
    print('%20s' % ("Proxy-server SQUID was installed the server " +
                    " with IP-address = " + ip_add + " and port " + proxy_port + " !"))
    print('\n' + 180 * '-')
    input("Please press any key for exit!")
    print("Information about your new proxies you can read in file proxy.txt!")
    return()

ip_add=check_ip()
try:
    sock = socket.socket()
    sock.connect((ip_add, 22))
    sock.close()
    deploy_proxy(ip_add)
except socket.error:
    sock.close()
    system('cls')
    print(180 * '-' + '\n')
    print('The IP-address you entered has not access for work!')
    print('For work with another server please start this scrip again.\n')
    print(180 * '-' + '\n')
    print('%90s' % ("Thank You! Good By!\n"))
    print(180 * '-')
    input("Please press any key!")
