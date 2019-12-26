from ._version import __version__

class DSGridError(Exception): pass

class DSGridAttributeError(DSGridError, AttributeError): pass

class DSGridIndexError(DSGridError, IndexError): pass

class DSGridNotImplementedError(DSGridError, NotImplementedError): pass

class DSGridRuntimeError(DSGridError, RuntimeError): pass

class DSGridValueError(DSGridError, ValueError): pass
