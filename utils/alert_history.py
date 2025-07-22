import json

def update_alert_history(current_time, message, platform):
    data = json.load(open('data/alert_history.json'))
    data['history'].append({
        "id": data['history'][-1]['id'] + 1,
        "message": str(message),
        "alert_date": str(current_time),
        "platform": platform
    })
    with open('data/alert_history.json', 'w') as file:
        json.dump(data, file)
        print("Alert History Updated")