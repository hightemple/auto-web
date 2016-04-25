import paramiko
# from pssh import ParallelSSHClient
import sys

# def para_ssh(ip_lst,user,password,port,cmd):
#     client = ParallelSSHClient(ip_lst, user=user, password=password, port=port)
#     result = client.run_command(cmd)
#     return result


def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #           stdin.write("Y")   #简单交互，输入 ‘Y’
        rtn = stdout.read().decode('ascii')
        #        for x in  stdout.readlines():
        #          print x.strip("n")
        # return '%stOKn'%(ip)
        ssh.close()
    except:
        rtn = '%s Error\n'%(ip)

    return rtn

# if __name__=="__main__":
#     # ip_lst = ['10.74.124.92','10.74.124.94','10.74.124.96','10.74.124.98','10.74.124.100','10.74.124.102']
#     # user = 'root'
#     # password = 'rootroot'
#     # port = 22
#     # cmd = 'df -h'
#
#     ip_lst = sys.argv[1].split()
#     user = sys.argv[2]
#     password = sys.argv[3]
#     port = int(sys.argv[4])
#     cmd = sys.argv[5]
#
#     rst = para_ssh(ip_lst, user, password, port, cmd)
#     for host, output in rst.items():
#         print(host, ":")
#         for line in rst[host]['stdout']:
#             print(line)
