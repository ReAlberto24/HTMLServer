import m_logger

for value, key in m_logger.ForegroundColors.__dict__.items():
    try:
        if key[0:1] == '__' and key[-1:-2] == '__':
            continue
        print(key, value)

    except Exception:
        pass
