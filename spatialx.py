from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

# URL of the Notification Service
NOTIFICATION_SERVICE_URL = "http://localhost:5001/v1/notify"

# In-memory storage for events (for demonstration purpose)
events = []


@app.route('/v1/event', methods=['POST'])
def receive_event():
    try:
        # Receive event data from the frontend mobile app
        data = request.json
        # Process the event
        process_event(data)
        return "Event received", 200
    except Exception as e:
        return str(e), 500


def process_event(event):
    try:
        # Store the event (for demonstration purpose)
        events.append(event)

        # Check the type of event and perform actions accordingly
        if event['type'] == "training_program_finished":
            # Calculate the duration of the training program
            duration = (datetime.datetime.now() - datetime.datetime.strptime(event['time_stamp'],
                                                                             "%Y-%m-%d %H:%M:%S")).seconds // 60
            # If duration is greater than 30 minutes, send a notification
            if duration > 30:
                send_notification(event['user_id'], f"Congratulations! You trained for {duration} minutes.")
        elif event['type'] == "app_launch":
            # Check if the user started a training program within 10 minutes of app launch
            launch_time = datetime.datetime.strptime(event['time_stamp'], "%Y-%m-%d %H:%M:%S")
            within_10_minutes = any(
                e['type'] == "training_program_started" and (
                            datetime.datetime.now() - datetime.datetime.strptime(e['time_stamp'],
                                                                                 "%Y-%m-%d %H:%M:%S")).seconds <= 600
                for e in events if e['user_id'] == event['user_id']
            )
            # If not, send a notification to start training
            if not within_10_minutes:
                send_notification(event['user_id'], "Start training now!")
    except Exception as e:
        # Log the exception
        print(f"Error processing event: {str(e)}")


def send_notification(user_id, message):
    try:
        # Send a notification to the user via the Notification Service
        url = f"{NOTIFICATION_SERVICE_URL}/{user_id}"
        data = {"message": message}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Notification sent to {user_id}: {message}")
        else:
            print(f"Failed to send notification to {user_id}")
    except Exception as e:
        # Log the exception
        print(f"Error sending notification: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
