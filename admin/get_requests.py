from dataclasses import dataclass
import json


@dataclass
class Requests:
    html: int = 0
    css: int = 0
    javascript: int = 0
    file: int = 0

    def __repr__(self):
        # return json.dumps({'html': self.html, 'css': self.css, 'javascript': self.javascript, 'file': self.file})
        return json.dumps(
            [["HTML", "CSS", "JavaScript", "Generic File"], [self.html, self.css, self.javascript, self.file]]
        )


with open('requests.bin', 'rb') as file:
    file_data = file.read()

base_rqs = Requests()

# HTML: 0
# CSS: 1
# JAVASCRIPT: 2
# FILE: 3
# FILE_NAME_START: 5
# FILE_NAME_END: 6

# print(file_data)

for _i in file_data:
    match _i:
        case 0:
            base_rqs.html += 1
        case 1:
            base_rqs.css += 1
        case 2:
            base_rqs.javascript += 1
        case 3:
            base_rqs.file += 1

print(base_rqs)
