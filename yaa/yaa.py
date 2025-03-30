"""yaa 智能体主程序入口

职责：
1. 初始化各模块（会话管理、身份验证、智能体等）
2. 启动服务端服务
3. 处理全局异常和中断
"""

import sys
import argparse
from .Client.BaseClient import BaseClient
from .Config.Config import Config
from .Config.ServerConfig import ServerConfig
from .Server.BaseServer import BaseServer

sys.path.append('..')
def main():
    parser = argparse.ArgumentParser(description='yaa 智能体命令行工具')

    # 定义互斥参数组，--run 和 --serve 不能同时使用
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--run', nargs='?', const='', help='运行智能体（可选值）')
    group.add_argument('--serve', action='store_true', help='启动服务模式')
    parser.add_argument('--config', type=str, help='配置文件路径')

    # serve 模式的可选参数
    parser.add_argument('--port', type=int, default=12345, help='服务端口号，默认 12345')

    args = parser.parse_args()
    
    # 如果指定了配置文件，则加载配置文件
    if args.config:
        Config.update_config(args.config)
    if args.serve:
        try:
            # 构建运行时配置
            runtime_config = {
                'yaa_server': {'port': args.port}
            }
            
            # 合并默认配置和运行时配置
            config = ServerConfig.merge_config(runtime_config)
            server = BaseServer(config=config)
            print(f"启动服务, 端口号: {config['yaa_server']['port']}")
            server.listen()
        except KeyboardInterrupt:
            print("\n服务已停止")
        except Exception as e:
            print(f"服务启动失败: {str(e)}")
    elif args.run:
        # 命令行交互模式
        BaseClient.run(args.run)
    else:
        # 命令行交互模式
        BaseClient.run()

if __name__ == "__main__":
    main()