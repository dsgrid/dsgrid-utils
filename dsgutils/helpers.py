
def ensure_enum(cls, val):
    """
    Returns the instance of cls that corresponds to val. cls is expected to be 
    an enum-type class.

    Parameters
    ----------
    cls : an enum class
    val : str or cls object

    Returns
    -------
    cls object
    """
    if isinstance(val, str):
        return cls[val]
    return cls(val)
    