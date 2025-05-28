class Color:
    BLACK   = [ 0.0, 0.0, 0.0 ]
    BLUE    = [ 0.0, 0.0, 1.0 ]
    GREEN   = [ 0.0, 1.0, 0.0 ]
    RED     = [ 1.0, 0.0, 0.0 ]
    CYAN    = [ 0.0, 1.0, 1.0 ]
    YELLOW  = [ 1.0, 1.0, 0.0 ]
    MAGENTA = [ 1.0, 0.0, 1.0 ]
    WHITE   = [ 1.0, 1.0, 1.0 ]
    TRIDECAGRAM = [ 0.16862745098039217, 0.6196078431372549, 0.4470588235294118 ]

    # TODO: Make this configurable
    OUTER_CUT = WHITE
    INNER_CUT = TRIDECAGRAM
    ANNOTATIONS = RED
    ETCHING = GREEN
    ETCHING_DEEP = CYAN
