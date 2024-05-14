import sys
import shutil
from datetime import datetime
import os
import subprocess

def copy_file_to_post_and_git_commit(file_path, commit_message, header):
    # 获取当前时间并转化为指定格式的字符串
    now = datetime.now().strftime("%Y-%m-%d")
    
    # 构造目标文件的路径
    file_name = os.path.basename(source_file_path)  # 获取原文件的文件名
    print(file_name)
    new_file_name = f"{now}-{file_name}"  # 添加时间前缀并且变为.md文件
    print(new_file_name)
    target_dir = "_posts"
    os.makedirs(target_dir, exist_ok=True)  # 确保目标目录存在，如果不存在则创建
    target_file_path = os.path.join(target_dir, new_file_name)
    
    # 复制文件
    shutil.copy2(source_file_path, target_file_path)
    print(f"File copied to {target_file_path}")

    # 在目标文件的最顶部添加自定义信息
    with open(target_file_path, 'r+', encoding='utf-8') as f:
        content = f.read()  # 读取文件内容
        f.seek(0, 0)  # 移动文件指针到文件开头
        f.write(header + '\n' + content)  # 在文件开头写入自定义信息和原始内容
    print(f"Header added to {target_file_path}")

    # Git add
    # subprocess.run(f"git add {target_file_path}", check=True, shell=True)
    
    # Git commit
    # subprocess.run(f'git commit -m "{commit_message}"', check=True, shell=True)
    
    # Git push
    # subprocess.run("git push", check=True, shell=True)
    # print(f"Changes pushed to remote repository.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py source_file_path")
    else:
        source_file_path = sys.argv[1]
        commit_message = f"Add {os.path.basename(source_file_path)}"
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = rf"""---
title: 
tags: Archive
# date: {formatted_time}
# sidebar:
#  nav: llm
# published: false
# aside:
#  toc: true
---
"""        
        copy_file_to_post_and_git_commit(source_file_path, commit_message, header)
