import paramiko


def sendFlow(hostname,username,password,command):
    if "tcpreplay" not in command:
        print("发包命令错误!!!")
        return False
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        _, stdout, stderr = ssh.exec_command(command)
        stdoutput = stdout.read().decode()  # read读取整个文件，readline读取一行
        stderrput = stderr.read().decode()  # read读取整个文件，readline读取一行
        if stderrput:
            print("标准错误输出:\n",stderrput)
            return False
        elif stdoutput:
            print("标准输出:\n",stdoutput)
            return True
        else:
            print("没有输出")
            return False
    except Exception as e:
        print("发送流量错误:",str(e))
        return False
    finally:
        ssh.close()

