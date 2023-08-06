
# 使用办法:
    >>> from nacla import nacla
    >>> nacla.predict("ming")
    (-1.36) Scottish
    (-1.66) English
    (-1.71) German
    >>> nacla.predict("qiang")
    (-1.96) English
    (-2.01) Dutch
    (-2.14) Italian
    >>> nacla.predict("xiao ming")
    (-0.82) Scottish
    (-1.89) English
    (-2.20) Greek
    >>> nacla.predict("ai guo")
    (-0.82) Portuguese
    (-1.72) Italian
    (-1.93) Spanish
