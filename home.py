PLUGIN_METADATA = {
    'id': 'home',
    'version': '1.0.0',
    'name': 'home',  
    'author': 'otae',
    'dependencies': {
        'mcdreforged': '<1.0.0',
    }
}

import json
import time

#帮助信息
help_msg = '''=-=-= §aMCDR Home插件帮助信息 §f=-=-=
§b!!home help §f- §c显示帮助消息
§b!!sethome [家名]§f- §c设置家,默认值为home
§b!!delhome [家名]§f- §c删除家,默认值为home
§b!!home [家名]§f- §c传送回家,默认值为home
§b!!home list§f- §c显示已有home列表
§f=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='''

tp_tran = {
    0: 'minecraft:overworld',
    -1: 'minecraft:the_nether',
    1: 'minecraft:overworld',
    'minecraft:overworld': 'minecraft:overworld',
    'minecraft:the_nether': 'minecraft:the_nether',
    'minecraft:the_end': 'minecraft:the_end'
}

dim_tran = {
    0: '§a主世界',
    -1: '§c地狱',
    1: '§6末地',
    'minecraft:overworld': '§a主世界',
    'minecraft:the_nether': '§c地狱',
    'minecraft:the_end': '§6末地'
}

json_filename = 'config/home.json'

homes = {}

def on_info(server,info):
    if info.is_player == 1:
        if info.content.startswith('!!home'):
            args = info.content.split(' ')
            if len(args) == 1:
                home = "home"
                back_home(info,server,home)
            elif len(args) == 2:
                if args[1] == 'help':
                    server.tell(info.player,help_msg)
                elif args[1] == "list":
                    print_home(info,server)
                else:
                    home = args[1]
                    back_home(info,server,home)
            else:
                server.tell(info.player,"格式错误,输入!!home help来查看帮助信息")
        elif info.content.startswith('!!sethome'):
            args = info.content.split(' ')
            if len(args) == 1:
                home = "home"
                sethome(info,server,home)
            elif len(args) == 2:
                home = args[1]
                sethome(info,server,home)
            else:
                server.tell(info.player,"格式错误,输入!!home help来查看帮助信息")
        elif info.content.startswith("!!delhome"):
            args = info.content.split(' ')
            if len(args) == 1:
                delhome = 'home'
                del_home(info,server,delhome)
            elif len(args) == 2:
                delhome = args[1]
                del_home(info,server,delhome)
            else:
                server.tell(info.player,"格式错误,输入!!home help来查看帮助信息")


#回家
def back_home(info,server,home):
    if info.player in homes:
        error = True
        for i in range(len(homes[info.player])):
            if home in homes[info.player][i]:
                server.tell(info.player, "§b将在3秒后传送回家")
                dim = homes[info.player][i][home][0]
                x = homes[info.player][i][home][1]
                y = homes[info.player][i][home][2]
                z = homes[info.player][i][home][3]
                time.sleep(3)
                server.execute('execute in {} run tp {} {} {} {}'.format(tp_tran[dim], info.player, x, y, z))
                error = False
        if error:
            server.tell(info.player,("§b没有名为",'"'+home+'"',"§b的家"))
    else:
        server.tell(info.player,"§b请先建立家")

#创建家
def sethome(info,server,home):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
    x = int(pos[0])
    y = int(pos[1])
    z = int(pos[2])
    dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
    if info.player in homes:
        error = True
        for i in range(len(homes[info.player])):
            if home in homes[info.player][i]:
                server.tell(info.player,"你已经有一个名为"+'"'+home+''+"的家了,请使用!!delhome删除后再创建")
                error = False
            print(homes[info.player][i])
        if error:
            homes[info.player].append({home:[dim,x,y,z]})
            saveJson()
            server.tell(info.player,"§b已成功设定家")
    else:
        homes[info.player] = [{home:[dim,x,y,z]}]
        saveJson()
        server.tell(info.player,"§b已成功设定家")

#删除家
def del_home(info,server,delhome):
    if info.player in homes:
        error = True
        for i in range(len(homes[info.player])):
            if delhome in homes[info.player][i]:
                del homes[info.player][i]
                error = False
                saveJson()
                server.tell(info.player,("§b已成功删除名为"+'"'+delhome+'"'+"的家"))
                break
        if error:
            server.tell(info.player,"没有可删除的家,请先建立")
    else:
        server.tell(info.player,"没有可删除的家,请先建立")


def on_load(server, old):
    global homes
    server.add_help_message('!!home help', 'Home插件帮助')
    try:
        with open(json_filename) as f:
            homes = json.load(f, encoding='utf8')
    except:
        saveJson()

#打印Home列表
def print_home(info,server):
    server.tell(info.player,"§bHome列表")
    if info.player in homes:
        for i in range(len(homes[info.player])):
            for key, values in homes[info.player][i].items():
                dim = values[0]
                x = values[1]
                y = values[2]
                z = values[3]
                if len(values) == 4:
                    server.tell(info.player,"名称:{} 坐标: §r{} §e{}, {}, {}".format(key, dim_tran[dim], x, y, z))
    else:
        server.tell(info.player,"没有已创建的家,请先建立")

#保存json
def saveJson():
    with open(json_filename, 'w') as f:
        json.dump(homes, f, indent=4)