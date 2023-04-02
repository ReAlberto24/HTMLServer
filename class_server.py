import subprocess

from flask import send_file


def file(file_name: str, directory: str) -> tuple[str, int] | str:
    try:
        if directory is None:
            return send_file(f'{file_name}')
        else:
            return send_file(f'{directory}/{file_name}')
    except FileNotFoundError:
        return '', 404
    except Exception:
        return '', 500


def javascript(js_type: str, file_name: str) -> tuple[str, int] | str:
    match js_type.lower():
        case 'vanilla':
            try:
                return send_file(
                    open(f'javascript/{file_name}', 'rb'),
                    'application/javascript'
                )
            except FileNotFoundError:
                return '', 404
            except Exception as e:
                return str(e), 500

        case 'typescript':
            try:
                subprocess.run(['tsc', f'javascript/{file_name}', '--outFile', 'javascript/co.' + file_name],
                               shell=True)
                return send_file(
                    open(f'javascript/co.{file_name}', 'rb'),
                    'application/javascript'
                )
            except FileNotFoundError:
                return '', 404
            except Exception as e:
                return str(e), 500

        case 'auto':
            try:
                is_typescript = bool(file_name.rsplit('.', 1)[1] == 'ts')

                if is_typescript:
                    subprocess.run(['tsc', f'javascript/{file_name}', '--outFile', 'javascript/co.' + file_name],
                                   shell=True)

                return send_file(
                    open(f'javascript/{"co." if is_typescript else ""}{file_name}', 'rb'),
                    'application/javascript'
                )
            except FileNotFoundError:
                return '', 404
            except Exception as e:
                return str(e), 500

        case _:
            return '', 500
