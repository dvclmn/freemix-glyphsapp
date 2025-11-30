def parse_percent(editText):
    """
    Convert "12%" → 0.12 (float)
    Return None if invalid.
    """
    try:
        txt = editText.get().strip("%")
        return float(txt) * 0.01
    except Exception:
        return None


#
