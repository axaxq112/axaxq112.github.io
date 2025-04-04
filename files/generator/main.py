import os
import sys
import datetime
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

# 配置项
config = {
    "unencrypted_file_dir": "C:/Users/Administrator/Documents/unecrypted_files",  # 未加密文件夹路径
    "encrypted_file_dir": "C:/Users/Administrator/Desktop/githubProjects/axaxq112.github.io/files/files",  # 加密后文件夹路径
    "max_split_chunk_size": 90,  # 分片最大大小 (MB)
}

# 分片加密的函数
def encrypt_file(file_path, key, max_chunk_size_mb):
    file_info = {
        "name": os.path.basename(file_path),
        "size": None,
        "uploadTime": str(datetime.datetime.now()),
        "totalParts": 0,
        "currentPart": 0
    }

    # 获取文件大小
    file_size = os.path.getsize(file_path)
    file_info["size"] = f"{file_size / (1024 * 1024):.2f} MB"

    # 计算总的分片数
    chunk_size = max_chunk_size_mb * 1024 * 1024  # 转换为字节
    total_parts = (file_size + chunk_size - 1) // chunk_size  # 向上取整
    file_info["totalParts"] = total_parts

    # 生成 AES 加密器
    cipher = AES.new(key.encode(), AES.MODE_CBC)

    # 打开文件进行分片和加密
    with open(file_path, 'rb') as f:
        for part_num in range(total_parts):
            file_info["currentPart"] = part_num + 1
            # 计算当前分片的起始位置和结束位置
            start = part_num * chunk_size
            end = min((part_num + 1) * chunk_size, file_size)
            f.seek(start)
            chunk = f.read(end - start)

            # 对文件分片进行加密
            encrypted_chunk = cipher.encrypt(pad(chunk, AES.block_size))

            # 保存加密后的分片文件
            encrypted_filename = f"{file_info['name']}.part{part_num + 1}.enc"
            encrypted_path = os.path.join(config["encrypted_file_dir"], encrypted_filename)

            with open(encrypted_path, 'wb') as enc_file:
                enc_file.write(encrypted_chunk)

    return file_info

# 生成 fileInfo.json 文件
def generate_file_info_json(file_info_list):
    data = {
        "fileAmount": len(file_info_list),
        "totalSize": sum([os.path.getsize(f"{config['encrypted_file_dir']}/{file['name']}.part1.enc") / (1024 * 1024) for file in file_info_list]),
        "lastUpdated": str(datetime.datetime.now()),
        "files": file_info_list
    }

    # 写入 JSON 文件
    with open("C:/Users/Administrator/Desktop/githubProjects/axaxq112.github.io/files/fileInfo.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)

# 主程序
def main(config):
    key = str(input("AES-256-加密用的Key:"))

    # 确保加密文件夹存在
    if not os.path.exists(config["encrypted_file_dir"]):
        os.makedirs(config["encrypted_file_dir"])

    file_info_list = []

    # 遍历未加密文件夹中的所有文件
    for root, dirs, files in os.walk(config["unencrypted_file_dir"]):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                print(f"正在加密文件: {file_path}")
                file_info = encrypt_file(file_path, key, config["max_split_chunk_size"])
                file_info_list.append(file_info)

    # 生成 fileInfo.json 文件
    generate_file_info_json(file_info_list)

if __name__ == "__main__":
    main(config)
