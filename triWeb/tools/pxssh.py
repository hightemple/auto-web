from pssh import ParallelSSHClient

def para_ssh(ip_lst,user,password,port,cmd):
    client = ParallelSSHClient(ip_lst, user=user, password=password, port=port)
    result = client.run_command(cmd)
    return result




if __name__=="__main__":
    ip_lst = ['10.74.124.92','10.74.124.94','10.74.124.96','10.74.124.98','10.74.124.100','10.74.124.102']
    user = 'root'
    password = 'rootroot'
    port = 22
    cmd = 'df -h'

    rst=para_ssh(ip_lst,user,password,port,cmd)
    for host,output in rst.items():
        print(host,":")
        for line in rst[host]['stdout']:
            print(line)

