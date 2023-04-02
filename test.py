import os
import threading

import keyboard

x, y = os.get_terminal_size()
text = [str(i) for i in range(y - 1)]

text[-1] = f'\033[{y}A'
print('\033[?25l')


def cao():
    global text
    encountered = False
    is_maiusc = False
    is_maius = False
    in_text = ''
    while True:
        hey = keyboard.read_key()
        # hey = keyboard.on_press_key()
        if hey == 'MAIUSC' or hey == 'maiusc':
            is_maiusc = not is_maiusc

        elif hey == 'backspace':
            in_text = in_text[:-1]

        else:
            if not encountered:
                match hey:
                    case 'space':
                        in_text += ' '

                    case 'ctrl':
                        pass
                    case 'alt':
                        pass
                    case 'enter':
                        pass
                    case 'tab':
                        in_text += '    '
                    case 'bloc maius':
                        is_maius = not is_maius
                    case _:
                        if is_maiusc or is_maius:
                            in_text += hey.upper()
                        else:
                            in_text += hey

                encountered = True
            else:
                encountered = False

        # text[-3] = '"' + hey + '"            '
        text[-2] = in_text


threading.Thread(target=cao, daemon=True).start()

while True:
    for x, i in enumerate(text):
        print(x, i)
        # time.sleep(0.2)

print('\033[?25h')
