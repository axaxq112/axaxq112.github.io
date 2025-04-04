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


def decrypt_file(encrypted_file_path, key, output_dir):
    # 创建 AES 解密器
    cipher = AES.new(key.encode(), AES.MODE_CBC)

    # 获取加密文件的大小
    encrypted_file_size = os.path.getsize(encrypted_file_path)

    # 打开加密文件进行解密
    with open(encrypted_file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()

        # 解密数据并去除填充
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # 生成解密后文件的路径
        decrypted_filename = os.path.basename(encrypted_file_path).replace(".enc", "")
        decrypted_file_path = os.path.join(output_dir, decrypted_filename)

        # 写入解密后的数据
        with open(decrypted_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

    print(f"解密文件: {decrypted_filename}")
    return decrypted_filename


def decrypt_files_from_info(file_info_json, key, output_dir):
    # 加载 fileInfo.json 文件
    with open(file_info_json, 'r') as json_file:
        file_info = json.load(json_file)

    # 确保解密文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历所有加密文件进行解密
    for file in file_info["files"]:
        total_parts = file["totalParts"]
        filename = file["name"]

        # 解密每个分片
        for part_num in range(1, total_parts + 1):
            encrypted_filename = f"{filename}.part{part_num}.enc"
            encrypted_file_path = os.path.join(config["encrypted_file_dir"], encrypted_filename)

            # 解密文件分片
            decrypt_file(encrypted_file_path, key, output_dir)


def main(config):
    key = str(input("请输入AES-256解密用的Key:"))

    # 解密所有文件
    decrypt_files_from_info("../fileInfo.json", key, config["unencrypted_file_dir"])


if __name__ == "__main__":
    main(config)