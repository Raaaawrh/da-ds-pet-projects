from typing import Optional


__all__ = [
    'text_to_int',
    'text_to_float',
    'text_to_letters',
    'text_to_name'
]

def text_to_int(text: str) -> Optional[int]:
    if text is None:
        return None
    tmp = ''.join([s for s in text if s.isdigit()])
    tmp = int(tmp) if tmp else None
    return tmp


def text_to_float(text: str) -> Optional[float]:
    if text is None:
        return None
    tmp = ''.join([s for s in text if s in '+-.1234567890'])
    tmp = float(tmp) if tmp else None
    return tmp

def text_to_letters(text: str) -> Optional[str]:
    if text is None:
        return None
    tmp = ''.join([s for s in text if s.isalpha()]).strip()
    return tmp if tmp else None

def text_to_name(text: str) -> Optional[str]:
    if text is None: return None
    tmp = ''.join([s for s in text if s.isalpha() or s in " '-"])
    return tmp