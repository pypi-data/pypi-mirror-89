import slack
import pymsteams
import pathlib
import json
import socket
import codecs


def _load_setting_file():
    setting_file_path = pathlib.Path.home()
    setting_file_path = setting_file_path.joinpath(".nosyupylib/settings.json")

    try:
        with codecs.open(setting_file_path, "r", "utf-8") as json_f:
            settings = json.load(json_f)
    except FileNotFoundError:
        raise FileNotFoundError

    return settings


def _convert_msg_to_markdown(body_msg):
    cur_host = socket.gethostname()

    if isinstance(body_msg, str):
        body_msg = body_msg.replace("\n", "\n\n")

        return "Location: {}\n\nMsg:\n\n{}".format(cur_host, body_msg)

    output_list = list()
    output_list.append("Location: {}".format(cur_host))
    for one_key, one_value in body_msg.items():
        output_list.append("{}: {}".format(one_key, one_value))

    return "\n\n".join(output_list)


def _notify_slack(settings, body_msg):
    sc = slack.WebClient(settings['slack_token'], timeout=30)

    sc.api_call(
        "chat.postMessage",
        json={
            'channel': '{}'.format(settings['slack_nosyu_channel']),
            'text': body_msg,
            'as_user': True
        }
    )


def _notify_teams(settings, body_msg):
    body_msg = _convert_msg_to_markdown(body_msg)

    webhook_url = settings["teams_Alert_NoSyu_webhook_url"]

    team_message = pymsteams.connectorcard(webhook_url)
    team_message.text(body_msg)
    team_message.send()


def alert_end_program(body_msg, channel='teams'):
    settings = _load_setting_file()

    if 'teams' == channel:
        _notify_teams(settings, body_msg)
    elif 'slack' == channel:
        _notify_slack(settings, body_msg)
    else:
        raise KeyError


def _test():
    body_msg = """
Hello! I am NoSyu.
    """

    alert_end_program(body_msg)
    alert_end_program({'a': 'b'})


if __name__ == "__main__":
    _test()
