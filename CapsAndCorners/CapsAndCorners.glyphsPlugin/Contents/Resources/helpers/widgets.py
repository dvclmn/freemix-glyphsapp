def match_widget(owner, widget, prefix):
    """
    Given a widget and a prefix, return:
        (i, cname, ctype)
    or (None, None, None) if not matched.
    """

    cc = owner.cc
    limit = owner.NUMBER_OF_FIELDS

    for i, (cname, ctype) in enumerate(cc[:limit]):
        w = getattr(owner.w, f"{prefix}{i}", None)
        if widget is w:
            return i, cname, ctype

    return None, None, None


#
