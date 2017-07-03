"""Utility module used for setting up configurations interactively"""
import ujson as json  # pylint: disable=import-error


def ask_input(prompt, choices=None, default=None):
    """Interactively asks for input with optional choices and default answer"""
    hint = " '%s'" % default if default else ''
    if choices:
        hint = ' [%s%s]' % ('/'.join(choices), hint)
    while 1:
        resp = input('%s%s: ' % (prompt, hint))
        chosen = choices and resp in choices or not choices and resp
        if chosen or not resp and default:
            return resp if resp else default


def ask_confirmation(prompt, default=None):
    """Interactively asks for confirmation (y or n) with an optional default"""
    default_answer = 'y' if default else 'n' if default is not None else None
    answer = ask_input(prompt, ('y', 'n'), default_answer)
    return answer and answer.lower() == 'y'


def ask_number(prompt, default=None):
    """Interactively asks for confirmation (y or n) with an optional default"""
    default_answer = str(default) if default is not None else None
    while 1:
        try:
            answer = ask_input(prompt, None, default_answer)
            return int(answer)
        except ValueError:
            print("'%s' is not a valid number" % answer)


def ask_json(prompt, default=None):
    """Interactively asks for json data with an optional default"""
    default_answer = json.dumps(default) if default is not None else None
    while 1:
        try:
            answer = ask_input(prompt, None, default_answer)
            return json.loads(answer)
        except ValueError:
            print("'%s' is not valid json" % answer)


def ask_dict(prompt, default=None):
    """Interactively asks for a dictionary with an optional default"""
    default_answer = default if isinstance(default, dict) else {}
    while 1:
        answer = ask_json(prompt, default_answer)
        if isinstance(answer, dict):
            return answer
        else:
            print("'%s' is not a valid dictionary" % answer)
