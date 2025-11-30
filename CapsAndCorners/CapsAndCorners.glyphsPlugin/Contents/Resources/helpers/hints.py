def iter_matching_hints(layer, cname, ctype):
    """Yield hints whose (name, type) matches."""
    for hint in layer.hints:
        if hint.name == cname and hint.type == ctype:
            yield hint


def update_hint_scale(hint, dimension, new_value):
    """
    Mutate the scale of `hint` and return True if it changed.
    Handles sign preservation and dimension switching.
    """

    scale = hint.pyobjc_instanceMethods.scale()

    if dimension == "widt":
        current = scale.x
    else:
        current = scale.y

    # No meaningful change?
    if abs(current - new_value) < 1e-5:
        return False

    # Preserve sign
    signed_value = new_value if current >= 0 else -new_value

    if dimension == "widt":
        scale.x = signed_value
    else:
        scale.y = signed_value

    hint.setScale_(scale)
    return True


#
