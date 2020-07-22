#! python3
# pw.py - 保存和使用密码

import sys
import pyperclip
import shelve
import string
import secrets
import json
from datetime import datetime

sout = '''
##########################
# 这是一个不安全的保存密码的脚本, 唯一的优点是快速保存和查找密码
# 使用前请新建一个目录，用来存放此脚本，此后保存和导出密码都将存放在此目录中
# 请勿删除目录中名为pwd的文件
##########################
# 用法：
######
# pw                       查看用法
# pw save [名字] -g        随机生成一个16位的强密码并保存
# pw save [名字] -g [位数] 生成指定位数的强密码
# pw save [名字] [密码]    保存密码
# pw list                 查看当前保存的所有密码
# pw rm [名字]             从当前列表中移除一个密码
# pw export                格式化导出当前所有密码（json）
# pw import                格式化导入密码（此功能还未实现）
# pw [名字]                查找密码并复制到剪贴板（如果存在）
##########################
'''


##########################
# 生成密码
##########################
def gen_pwd(k):
    seq_str = [x.strip() for x in string.printable.split('\n\t')][0]
    while True:
        password = ''.join(secrets.choice(seq_str) for i in range(k))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


if len(sys.argv) < 2:
    print(sout)
    sys.exit()

pwdShelf = shelve.open('pwd')


##########################
# 导出密码
##########################
def export_pwd():
    pwd_dict = {}
    for key, value in zip(pwdShelf.keys(), pwdShelf.values()):
        pwd_dict[key] = value
    pwd_dict = json.dumps(pwd_dict, sort_keys=True, indent=4)
    return pwd_dict


##########################
# 操作密码
##########################
if len(sys.argv) == 5 and sys.argv[1].lower() == 'save' and sys.argv[3] == '-g':
    if sys.argv[4].isdigit():
        pwdShelf[sys.argv[2]] = gen_pwd(int(sys.argv[4]))
        pyperclip.copy(pwdShelf[sys.argv[2]])
        print(sys.argv[2] + '已保存，并且已经将密码复制到剪贴板，pw list查看')
    else:
        print('请输入数字')

elif len(sys.argv) == 4 and sys.argv[1].lower() == 'save' and sys.argv[3] == '-g':
    pwdShelf[sys.argv[2]] = gen_pwd(16)
    pyperclip.copy(pwdShelf[sys.argv[2]])
    print(sys.argv[2] + '已保存，并且已经将密码复制到剪贴板，pw list查看')

elif len(sys.argv) == 4 and sys.argv[1].lower() == 'save':
    pwdShelf[sys.argv[2]] = sys.argv[3]
    print(sys.argv[2] + '已经保存。')

elif len(sys.argv) == 3 and sys.argv[1].lower() == 'rm':
    del pwdShelf[sys.argv[2]]
    print(sys.argv[2] + '已经删除')

elif len(sys.argv) == 2:
    if sys.argv[1].lower() == 'list':
        print('当前已经保存的密码： ' + str(list(pwdShelf.keys())))

    elif sys.argv[1].lower() == 'export':
        tm = '-'.join(datetime.now().isoformat('-').split(':')[:-1])
        with open('pw_export_' + tm + '.json', 'wt', encoding='utf-8') as f:
            f.write(str(export_pwd()))
        print('已经保存到pw_export_' + tm + '.json文件中')

    elif sys.argv[1] in pwdShelf:
        pyperclip.copy(pwdShelf[sys.argv[1]])
        print(sys.argv[1] + '的密码已经拷贝到剪贴板了')

    else:
        print('没有' + sys.argv[1] + '这个名字')

pwdShelf.close()
