

def log(
        message="",
        verbose=True,
        colour=None,
        background=None,
        bold=False,
        underline=False,
        inverted=False,
        run=False,
        ret=False):

    """ log() prints a message that is formatted properly.

        Using ANSI colour and formatting strings, log() prints out a formatted
        string. If run=True, the following print command (or log())
        will appear on the same line.
    """

    if verbose:

        colours = {
            'black':    '90',
            'red':      '91',
            'green':    '92',
            'yellow':   '93',
            'blue':     '94',
            'magenta':  '95',
            'cyan':     '96',
            'white':    '97',
        }

        backgrounds = {
            'default':  '49',
            'black':    '100',
            'red':      '101',
            'green':    '102',
            'yellow':   '103',
            'blue':     '104',
            'magenta':  '105',
            'cyan':     '106',
            'white':    '107'
        }

        if bold:
            message = '\033[1m' + message + '\033[21m'
        if underline:
            message = '\033[4m' + message + '\033[24m'
        if background is not None:
            message = '\033[' + backgrounds[background] + \
                'm' + message + '\033[49m'
        if colour is not None:
            message = '\033[' + colours[colour] + 'm' + message + '\033[0m'
        if inverted:
            message = '\033[7m' + message + '\033[27m'

        if ret:
            return message

        if run:
            print message,
        else:
            print message

    return
