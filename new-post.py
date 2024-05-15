import sys
import shutil
from datetime import datetime
import os
import subprocess
import os
import shutil
from datetime import datetime

import os
import shutil
from datetime import datetime

def update_content_with_or_without_yaml(source_file_path, target_file_path, header):
    # 读取目标文件当前内容，检查是否有YAML部分
    with open(target_file_path, 'r', encoding='utf-8') as target_file:
        target_content = target_file.read()
        yaml_content = ""
        if target_content.startswith('---'):
            # 如果目标文件有YAML部分，提取出来
            yaml_end_index = target_content.find('---', 3)
            if yaml_end_index != -1:
                yaml_content = target_content[:yaml_end_index + 3]  # 包括YAML的结束标记
    
    # 读取源文件内容
    with open(source_file_path, 'r', encoding='utf-8') as src_file:
        source_content = src_file.read()
    
    # 将源文件内容复制到目标文件，并根据YAML信息进行调整
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        if yaml_content:
            # 如果原目标文件中有YAML信息，保留该信息，并附加源文件内容
            target_file.write(yaml_content + '\n\n' + source_content)
        else:
            # 如果原目标文件中没有YAML信息，添加header，并附加源文件内容
            target_file.write(header + '\n\n' + source_content)
        print(f"Content updated in {target_file_path}")

def update_copy_file_and_update_with_header(source_file_path, commit_message, header):
    # 获取当前时间作为时间戳
    now = datetime.now().strftime("%Y-%m-%d")
    
    # 构造新的文件名和目标路径
    file_name = os.path.basename(source_file_path)
    new_file_name = f"{now}-{file_name}"
    target_dir = "_posts"
    os.makedirs(target_dir, exist_ok=True)  # 确保目录存在
    target_file_path = os.path.join(target_dir, new_file_name)
    
    if not os.path.exists(target_file_path):
        # 如果目标文件不存在，则创建文件并且添加header
        shutil.copy(source_file_path, target_file_path)
        with open(target_file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)
            file.write(header + '\n\n' + content)
        print(f"Created {target_file_path} with header.")
    else:
        # 如果目标文件存在，更新其内容，保持或添加YAML信息
        update_content_with_or_without_yaml(source_file_path, target_file_path, header)
        print(f"Updated {target_file_path}, maintaining YAML header if present.")

# legacy
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
        update_copy_file_and_update_with_header(source_file_path, commit_message, header)
