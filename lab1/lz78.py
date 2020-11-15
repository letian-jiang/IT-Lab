"""Codes for first group homework of Information Theory and Coding. 
Author: Hongbin Chen
Modified date: 2020-11-08
Version: 1

Some tips:
1. About python class 'bytes', data is 'bytes' object, data[0] is 'int'
    type while data[0:1] is 'bytes' type. 
2. In LZ77, I use one byte (0-255) to represent the offset or max common 
    length, if you need to use a larger buffer size, please use two bytes 
    to represent the offset and max common length. 
3. You may need to install python-docx by pip. 
"""
import time
from docx import Document

def read_file(file_path):
    """Read a .docx file and return its text with binary bytes. 
    Args:
        file_path: The directory of file. 
    
    Returns:
        The byte stream of source file, which's type is <class 'bytes'>. 
    """
    file = Document(file_path)
    str_data = []
    for p in file.paragraphs:
        str_data.append(p.text)
    str_data = '\r\n'.join(str_data)
    bytes_data = bytes(str_data, encoding="utf-8")
    # str_data = str(bytes_data, encoding="utf-8")
    return bytes_data

def LZ78_encoding(source_data):
    """Encoding function for LZ78. 

    The source data is in binary format. We consider each byte as a symbol to be 
    encoded. The index in tuple (first element in tuple) is represented by two 
    bytes. Codeword of a symbol is itself.

    Args:
        source_data: <class 'bytes'> The source data to be encoded. 
    
    Returns:
        <class 'bytes'> Encoded data of source data. The encoded data is organized 
        by three-bytes tuples. Each tuple consists of two-bytes index and one-byte 
        codeword of first symbol following the match. 
    """
    total_len = len(source_data)

    # dictionary format: {entry: index}
    dictionary = {}
    encoded_data = []
    encoding_pointer = 0
    while encoding_pointer < total_len:
        entry_length = 1
        while encoding_pointer + entry_length < total_len and\
              source_data[encoding_pointer: encoding_pointer+entry_length] in dictionary:
              entry_length += 1

        entry = source_data[encoding_pointer: encoding_pointer+entry_length]
        if entry_length > 1:
            prefix = entry[:-1]
            index = dictionary[prefix]
            index_high = index >> 8
            index_low = index - (index_high << 8)
            encoded_data.append(bytes([index_high, index_low, entry[-1]]))
        else:
            encoded_data.append(bytes([0, 0, source_data[encoding_pointer]]))
        dict_index = len(dictionary) + 1
        dictionary[entry] = dict_index

        encoding_pointer += entry_length
    encoded_data = b''.join(encoded_data)
    return encoded_data


def LZ78_decoding(encoded_data):
    """Decoding function for LZ78
    Args:
        encoded_data: <class 'bytes'> Encoded data to be decoded. 
    
    Returns:
        <class 'bytes'> Decoded data of given encoded data. 
    """
    total_len = len(encoded_data)
    decoded_data = []
    dictionary = []
    for i in range(0, total_len, 3):
        index = (encoded_data[i]<<8) + encoded_data[i+1]
        codeword = encoded_data[i+2: i+3]
        if index == 0:
            dictionary.append(codeword)
            decoded_data.append(codeword)
        else:
            entry = b''.join([dictionary[index-1], codeword])
            dictionary.append(entry)
            decoded_data.append(entry)
    decoded_data = b''.join(decoded_data)
    return decoded_data


def main():
    file_path = "data.docx"
    source_data = read_file(file_path)
    source_space = len(source_data)

    print("Compression by LZ78...")
    start_t = time.time()
    encoded_data_LZ78 = LZ78_encoding(source_data)
    end_t = time.time()
    encoded_space_LZ78 = len(encoded_data_LZ78)
    print("Source data length: {}".format(source_space))
    print("Encoded data length: {}".format(encoded_space_LZ78))
    print("Compression rate: {:.2f}%".format(encoded_space_LZ78/source_space*100))
    print("Encoding cost time: {:.2f} ms".format((end_t - start_t)*1000))
    start_t = time.time()
    decoded_data_LZ78 = LZ78_decoding(encoded_data_LZ78)
    end_t = time.time()
    print("Decoding cost time: {:.2f} ms".format((end_t-start_t)*1000))
    print("Source data == decoded data:", decoded_data_LZ78==source_data)

if __name__ == "__main__":
    main()