import os


def convert_bytes(byte_value):
    # define conversion factors
    KB = 1024.0
    MB = KB ** 2
    GB = KB ** 3
    TB = KB ** 4

    # convert bytes to the appropriate unit
    if byte_value < KB:
        return f"{byte_value} bytes"
    elif KB <= byte_value < MB:
        return f"{byte_value / KB:.2f} Kb"
    elif MB <= byte_value < GB:
        return f"{byte_value / MB:.2f} Mb"
    elif GB <= byte_value < TB:
        return f"{byte_value / GB:.2f} Gb"
    else:
        return f"{byte_value / TB:.2f} Tb"


def get_folder_size(folder_path):
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size


size = get_folder_size('.')
print(f'<span>Total used space: {convert_bytes(size)}</span>')
