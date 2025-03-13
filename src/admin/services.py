''''''

import os
import time
import re
import json

from src.common.logger_setup import get_logger

logger = get_logger(__name__)

def read_src_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.rstrip() for line in file]

def save_to_dest_file(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def divide_to_chunks(subtile_text):
    """"""
    chunks = []
    chunk_value = ''
    for line in subtile_text:
        if line.strip():
            if re.match(r"\d", line) is not None:
                if chunk_value != '':
                    n = sum(c.isdigit() for c in line)
                    s = line[n]
                    if s != '.':
                        # If it is not new chunks id
                        chunk_value += line + '\n'
                    chunk = {"chank": chunk_value}
                    chunks.append(chunk)
                    chunk_value = ''
                continue
            else:
                chunk_value += line + '\n'
    # last chunk
    if chunk_value != '':
        chunk = {"chank": chunk_value}
        chunks.append(chunk)
    
    return chunks


def convert_file(input_file: str, name: str):
    ''''''
    try:
        original_text = read_src_file(input_file)
        chunks = divide_to_chunks(original_text)

        project_root = os.getcwd()
        content_path = f'{project_root}/content'
        output_file = os.path.join(content_path, f'{name}.json')
        
        output_data = {
            "name": name,
            "content": chunks
        }
        save_to_dest_file(output_data, output_file)

        logger.info(f"File {input_file} converted to {output_file}")
    except Exception as e:
        logger.error(f"Error {e} convert ile {input_file} to {output_file}")