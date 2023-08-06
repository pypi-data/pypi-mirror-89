import slack


def slack_notify(body_msg):
    sc = slack.WebClient(slack_token, timeout=30)

    sc.api_call(
        "chat.postMessage",
        json={
            'channel': '{}'.format(slack_nosyu_channel),
            'text': body_msg,
            'as_user': True
        }
    )


def main():
    line_stack = list()

    for line in sys.stdin:
        line_stack.append(line)

    body_msg = "".join(line_stack)

    send_msg(body_msg)