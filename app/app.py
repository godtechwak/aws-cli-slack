import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient

token = {slack token}
app = Flask(__name__)
client = WebClient(token)


def get_day_of_week():
    weekday_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y %m %d")
    result = '{}({})'.format(date, weekday)
    return result

def get_time():
    return datetime.today().strftime("%H %M %S")


def get_answer(text):
    trim_text = text.replace(" ", "")

    answer_dict = {
        'endpoint': '```aws rds describe-db-cluster-endpoints --region {region} --db-cluster-endpoint-identifier {custom endpoint}```',
        'logfile': '```aws rds describe-db-log-files --db-instance-identified --filename-contains --file-size {file size}```',
        'recovery/clusterinfo': '```aws rds describe-db-clusters --db-cluster-identifier {db cluster} ```',
        'rds': '```aws rds describe-db-clusters --db-cluster-identifier {db cluster}```',
        'day': ':calendar: Today is {}'.format(get_day_of_week()),
        'time': ':clock9: Time is {}'.format(get_time()),
    }

    if trim_text == '' or None:
        return "Try, anithing!"
    elif trim_text in answer_dict.keys():
        return answer_dict[trim_text]
    else:
        for key in answer_dict.keys():
            if key.find(trim_text) != -1:
                return "Related command is [" + key + "].\n" + answer_dict[key]

        for key in answer_dict.keys():
            if answer_dict[key].find(text[1:]) != -1:
                return "Similar command is [" + key + "].\n"+ answer_dict[key]

    return text + " is terrable"


def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)

    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
                answer = get_answer(user_query)
                result = client.chat_postMessage(channel=channel,
                                                 text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass

    message = "[%s] cannot find event handler" % event_type

    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
