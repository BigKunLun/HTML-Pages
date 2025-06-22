#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的本地HTTP服务器
用于提供静态文件服务
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def start_server(port=8888, directory=None):
    """
    启动HTTP服务器
    
    Args:
        port (int): 服务器端口，默认8888
        directory (str): 服务目录，默认为当前目录
    """
    if directory is None:
        directory = os.getcwd()
    
    # 切换到指定目录
    os.chdir(directory)
    
    # 创建服务器处理器
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"服务器启动成功！")
            print(f"访问地址: http://localhost:{port}")
            print(f"服务目录: {os.getcwd()}")
            print("按 Ctrl+C 停止服务器")
            print("-" * 50)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"错误: 端口 {port} 已被占用，请尝试其他端口")
        else:
            print(f"启动服务器时出错: {e}")

def main():
    """
    主函数，处理命令行参数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='启动本地HTTP服务器')
    parser.add_argument('-p', '--port', type=int, default=8888, 
                       help='服务器端口 (默认: 8888)')
    parser.add_argument('-d', '--directory', type=str, default=None,
                       help='服务目录 (默认: 当前目录)')
    
    args = parser.parse_args()
    
    # 验证目录是否存在
    if args.directory and not os.path.isdir(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        sys.exit(1)
    
    start_server(args.port, args.directory)

if __name__ == "__main__":
    main()