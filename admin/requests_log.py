html = 0
css = 0
javascript = 0
file_r = 0

# HTML: 0
# CSS: 1
# JAVASCRIPT: 2
# FILE: 3
# FILE_NAME_START: 5
# FILE_NAME_END: 6

with open('requests.bin', 'rb') as file:
    for i in file.read():
        match i:
            case 0:
                html += 1
            case 1:
                css += 1
            case 2:
                javascript += 1
            case 3:
                file_r += 1

print(
    html,
    css,
    javascript,
    file_r
)
