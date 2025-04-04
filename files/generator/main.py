import os
import sys
import datetime

config = {
    "unencrypted_file_dir" : "../../files",
    "encrypted_file_dir" : "./files",
    "max_split_chunk_size" : "90" #单位: MB
}


def main(config):
    print(config)















if __name__ == "__main__":
    encryptKey = str(input("加密用的Key:"))
    encryptIv = int(input("加密用的IV:"))
    main(config)