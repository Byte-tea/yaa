"""yaa 智能体主程序入口

职责：
1. 初始化各模块（会话管理、身份验证、智能体等）
2. 启动服务端服务
3. 处理全局异常和中断
"""

import sys
import argparse
from .Config.ServerConfig import ServerConfig
from .Server.BaseServer import BaseServer

sys.path.append('..')
def main():
    parser = argparse.ArgumentParser(description='yaa 智能体命令行工具')

    # 定义互斥参数组，--run 和 --serve 不能同时使用
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--run', type=str, help='运行智能体')
    group.add_argument('--serve', action='store_true', help='启动服务模式')

    # serve 模式的可选参数
    parser.add_argument('--port', type=int, default=12345, help='服务端口号，默认 12345')
    parser.add_argument('--config', type=str, help='配置文件路径')

    args = parser.parse_args()

    if args.run:
        # TODO 命令行交互式应用模式运行此提示词
        # print(f"输入的提示词: {args.run}")
        pass
    elif args.serve:
        try:
            # 构建运行时配置
            runtime_config = {
                'yaa_server': {'port': args.port},
                'security': {}
            }
            # 如果指定了配置文件，则加载配置文件
            if args.config:
                # print(f"使用配置文件: {args.config}")
                # TODO: 从配置文件加载配置
                pass
            
            # 合并默认配置和运行时配置
            config = ServerConfig.merge_config(runtime_config)
            server = BaseServer(config=config)
            print(f"启动服务, 端口号: {config['yaa_server']['port']}")
            server.listen()
        except KeyboardInterrupt:
            print("\n服务已停止")
        except Exception as e:
            print(f"服务启动失败: {str(e)}")
    else:
        # TODO 命令行交互式应用模式
        # print("命令行应用模式")
        pass

if __name__ == "__main__":
    main()