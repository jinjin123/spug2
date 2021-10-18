import os
from passlib.hash import sha512_crypt
import getpass
import random
import string

# 获取所有主机
# f = os.popen("grep -vE '^$|^#|^\[' /etc/ansible/hosts |awk '{print $1}'")
f = os.popen("grep -vE '^$|^#|^\[' ./host |awk '{print $1}'")
host = list(f)
# print(host)
# 显示主机
def randpass(length=10):
    chars = string.ascii_letters + random.choice("!@#$%") + string.digits + str(random.randint(1,10)) + random.choice("!@#$%")
    return ''.join([random.choice(chars) for i in range(length)])

for index, element in enumerate(host):
    m = randpass()
    with open("ip_pwd", "a+") as f:
        f.write(str(index) + ':' + element.strip() + ":" + m + '\n')
    os.system(("""ansible %s -m user -a "name=jin update_password=always password={{ newpassword|password_hash('sha512') }}" -b --extra-vars 'newpassword=%s'""")%(element.strip(),m))
    # print(str(index) + ':' + element.strip() + ":" + randpass())


# def randpass(length=10):
#     chars = string.ascii_letters + string.digits + str(random.randint(1,10)) + random.choice("!@#$%")
#     return ''.join([random.choice(chars) for i in range(length)])
#
#
# # 选择主机
# choice = int(input('请选择主机,填写数字:'))
# mechina = host[choice].strip()
# # 生成密码
# mima = randpass()
# print(mima)
# sha512mima = sha512_crypt.using(rounds=5000).hash(mima)
# print(sha512mima)


# ansible -i hostfile all -m user -a "name=admin update_password=always password={{ newpassword|password_hash('sha512') }}" -b --extra-vars "newpassword=12345678"

# print('\n您选择的主机是:', mechina, '密码是:', mima, '\n')
# # 调用ansible修改密码
# os.system(("ansible %s -m user -a 'name=root password=%s update_password=always'") % (mechina, sha512mima))

#ansible 127.0.0.1 -m user -a "name=root update_password=always password={{ newpassword|password_hash('sha512') }}" -b --extra-vars "newpassword=12345678"