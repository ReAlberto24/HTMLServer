import io
import sys
import textwrap


def parse_html_and_exec_python(html):
    lines = html.splitlines()
    in_python_tag = False
    result = ""
    output = ""
    indentation = 0
    for line in lines:
        if line.strip().startswith("<python>"):
            in_python_tag = True
            indentation = len(line) - len(line.lstrip())
            continue
        elif line.strip().startswith("</python>"):
            in_python_tag = False
            result += output
            output = ""
            continue
        elif in_python_tag:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            exec(textwrap.dedent(line[indentation:]))
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
        else:
            result += line + "\n"
    return result.replace("\n", "<br>")


html = """
<html>
    <body>
        <python>
            for i in range(10):
                print(i)
        </python>
        <p>This is a paragraph.</p>
    </body>
</html>
"""
print(parse_html_and_exec_python(html))
