def route1():
    data = get_user_input()
    data = sanitize_input(data)
    # ok: taint-example
    return html_output(data)

def route2():
    data = get_user_input()
    # ruleid: taint-example
    return html_output(data)