#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的本地HTTP服务器
用于提供静态文件服务
支持中文文件名显示和增强的错误处理
"""

import http.server
import socketserver
import os
import sys
import urllib.parse
import webbrowser
from pathlib import Path
from datetime import datetime

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    自定义HTTP请求处理器，支持中文URL解码显示
    """
    
    def log_message(self, format, *args):
        """重写日志方法，解码中文URL"""
        decoded_args = []
        for arg in args:
            if isinstance(arg, str) and '%' in arg:
                try:
                    # 解码URL中的中文字符
                    decoded_arg = urllib.parse.unquote(arg, encoding='utf-8')
                    decoded_args.append(decoded_arg)
                except Exception:
                    decoded_args.append(arg)
            else:
                decoded_args.append(arg)
        
        # 添加时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.address_string()
        print(f"[{timestamp}] {client_ip} - {format % tuple(decoded_args)}")
    
    def end_headers(self):
        """添加CORS头和缓存控制"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def start_server(port=8888, directory=None, auto_open=False):
    """
    启动HTTP服务器
    
    Args:
        port (int): 服务器端口，默认8888
        directory (str): 服务目录，默认为当前目录
        auto_open (bool): 是否自动打开浏览器
    """
    if directory is None:
        directory = os.getcwd()
    
    # 验证并切换到指定目录
    if not os.path.isdir(directory):
        print(f"❌ 错误: 目录 '{directory}' 不存在")
        return False
    
    os.chdir(directory)
    
    # 使用自定义处理器
    handler = CustomHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            server_url = f"http://localhost:{port}"
            print("\n" + "=" * 60)
            print("🚀 HTTP服务器启动成功！")
            print("=" * 60)
            print(f"📍 访问地址: {server_url}")
            print(f"📁 服务目录: {os.getcwd()}")
            print(f"🔌 监听端口: {port}")
            print(f"⏰ 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\n💡 提示:")
            print("   - 按 Ctrl+C 停止服务器")
            print("   - 访问日志中的中文URL已自动解码显示")
            print("   - 支持CORS跨域访问")
            print("=" * 60 + "\n")
            
            # 自动打开浏览器
            if auto_open:
                try:
                    webbrowser.open(server_url)
                    print(f"🌐 已自动打开浏览器: {server_url}\n")
                except Exception as e:
                    print(f"⚠️  无法自动打开浏览器: {e}\n")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
        print(f"⏰ 停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except OSError as e:
        if e.errno == 48 or 'Address already in use' in str(e):
            print(f"❌ 错误: 端口 {port} 已被占用")
            print("💡 建议: 请尝试其他端口，如: python server.py -p 8889")
        else:
            print(f"❌ 启动服务器时出错: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def main():
    """
    主函数，处理命令行参数
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='启动本地HTTP服务器 - 支持中文文件名和增强功能',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python server.py                    # 使用默认设置
  python server.py -p 8080            # 指定端口
  python server.py -d /path/to/dir    # 指定目录
  python server.py -p 8080 -o         # 指定端口并自动打开浏览器
        """
    )
    
    parser.add_argument('-p', '--port', type=int, default=8888, 
                       help='服务器端口 (默认: 8888)')
    parser.add_argument('-d', '--directory', type=str, default=None,
                       help='服务目录 (默认: 当前目录)')
    parser.add_argument('-o', '--open', action='store_true',
                       help='启动后自动打开浏览器')
    parser.add_argument('--version', action='version', version='HTTP Server v2.0')
    
    args = parser.parse_args()
    
    # 验证端口范围
    if not (1 <= args.port <= 65535):
        print("❌ 错误: 端口号必须在 1-65535 范围内")
        sys.exit(1)
    
    # 验证目录
    if args.directory:
        if not os.path.exists(args.directory):
            print(f"❌ 错误: 目录 '{args.directory}' 不存在")
            sys.exit(1)
        if not os.path.isdir(args.directory):
            print(f"❌ 错误: '{args.directory}' 不是一个目录")
            sys.exit(1)
    
    # 启动服务器
    success = start_server(args.port, args.directory, args.open)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()