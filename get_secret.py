import time
import re
import paramiko

# postavljanje podataka za spajanje
hname = '10.99.15.110'
uname = 'user'
passwd = 'pass'

# ssh cursor
ssh = paramiko.SSHClient()

# dodavanje ssh public key-a
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# log fajl koji se prati
log_file = "/var/log/loghost/f5prim.mo.hr/local0.log"

# regex za extract podataka 
pattern = r"\b(\w+):=([A-Z0-9]+)\b"

# output datoteka
output_file = "/var/log/f5_apm/matched_text.txt"

# otvaranje log fajla
d=open(log_file, 'r')

# output fajl gdje se smjesta matchirani tekst
f=open(output_file, "a", buffering = 1)


def process(line):
    match=re.search(pattern, line)
    if not match:
        return
    name = re.sub(r'[^a-zA-Z0-9]', '', match.group(1)).lower()
    #name = str(match.group(1)).strip()
    value = str(match.group(2)).strip()
    print("Ovo je ime: " +  name + " ovo je value " + value)
    ssh.connect(hostname=hname, username=uname, password=passwd)
    print("Search prosao")
    stdin, stdout, stderr = ssh.exec_command('modify ltm data-group internal ga_test_dg records add {"%s" {data "%s"}}' % (name, value))
    stdin.close()
    ssh.close()
    matched_text = name + ":=" + value
    f.write(matched_text + "\n")
    f.flush()
    print("Match")

# algoritam koji glumi tail -f u linuxu
while True:
    line = ''
    d.seek(0,2)
    while len(line) == 0 or line[-1] != '\n':
        tail = d.readline()
        if tail == '':
            time.sleep(0.1)
            continue
        line += tail
    process(line)
