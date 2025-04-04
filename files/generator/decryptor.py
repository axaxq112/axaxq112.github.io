import os
import json
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


config = {
    "base_url": "https://axaxq112.github.io/files/files/",  # 你的 base URL
    "unencrypted_file_dir": "C:/Users/Administrator/Documents/decrypted_files",  # 解密文件夹路径
    "encrypted_file_dir": "../files",  # 加密后文件夹路径
    "max_split_chunk_size": 90,  # 分片最大大小 (MB)
}


def decrypt_file(encrypted_file_path, key):
    """ 解密单个文件分片 """
    # 创建 AES 解密器
    cipher = AES.new(key.encode(), AES.MODE_CBC)

    # 打开加密文件进行解密
    with open(encrypted_file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()

        # 解密数据并去除填充
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    return decrypted_data


def merge_file_parts(file_info, key, output_dir):
    """ 合并文件分片为一个完整的文件 """
    file_name = file_info["name"]
    total_parts = file_info["totalParts"]

    # 创建一个文件来合并所有分片
    merged_file_path = os.path.join(output_dir, file_name)

    with open(merged_file_path, 'wb') as merged_file:
        # 按照顺序解密并合并每个分片
        for part_num in range(1, total_parts + 1):
            encrypted_filename = f"{file_name}.part{part_num}.enc"
            encrypted_file_path = os.path.join(config["encrypted_file_dir"], encrypted_filename)

            # 解密文件分片
            decrypted_data = decrypt_file(encrypted_file_path, key)

            # 将解密后的数据写入合并文件
            merged_file.write(decrypted_data)

    print(f"文件 {file_name} 合并完成，保存在 {merged_file_path}")
    return merged_file_path


def decrypt_files_from_info(file_info_json, key, output_dir):
    """ 根据 fileInfo.json 解密所有文件并合并分片 """
    # 加载 fileInfo.json 文件
    with open(file_info_json, 'r') as json_file:
        file_info = json.load(json_file)

    # 确保解密文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 解密并合并所有文件
    for file in file_info["files"]:
        print(f"开始解密文件: {file['name']}")
        # 合并文件分片
        merge_file_parts(file, key, output_dir)


def main(config):
    key = str(input("请输入AES-256解密用的Key:"))

    # 解密并合并所有文件
    decrypt_files_from_info("../fileInfo.json", key, config["unencrypted_file_dir"])


if __name__ == "__main__":
    main(config)
