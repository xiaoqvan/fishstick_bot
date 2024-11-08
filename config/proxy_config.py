# proxy_config.py
import os
import configparser

def get_proxy_config():
    config_file = 'config/config.ini'
    config = configparser.ConfigParser()

    # 检查是否存在 config/config.ini 文件
    if not os.path.exists(config_file):
        # 询问用户是否使用代理
        use_proxy = input("是否使用代理? (y/n): ").strip().lower() == 'y'

        # 如果使用代理，获取代理设置
        if use_proxy:
            while True:
                choice = input("请选择代理协议 (1: socks5, 2: http): ").strip()
                if choice == '1':
                    scheme = 'socks5'
                    break
                elif choice == '2':
                    scheme = 'http'
                    break
                else:
                    print("无效的选择，请输入 '1' 或 '2'")

            proxy = {
                "scheme": scheme,
                "hostname": input("请输入代理主机名: ").strip(),
                "port": int(input("请输入代理端口: ").strip())
            }
        else:
            proxy = None

        # 生成 config.ini 文件并记录代理选项
        config['PROXY'] = {
            'use_proxy': str(use_proxy),
            'scheme': proxy['scheme'] if use_proxy else '',
            'hostname': proxy['hostname'] if use_proxy else '',
            'port': str(proxy['port']) if use_proxy else ''
        }
        with open(config_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    else:
        # 读取 config.ini 文件中的代理设置
        config.read(config_file, encoding='utf-8')
        use_proxy = config.getboolean('PROXY', 'use_proxy')
        if use_proxy:
            proxy = {
                "scheme": config['PROXY']['scheme'],
                "hostname": config['PROXY']['hostname'],
                "port": int(config['PROXY']['port'])
            }
        else:
            proxy = None

    return proxy