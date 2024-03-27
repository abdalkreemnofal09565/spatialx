from flask import Flask, request

app = Flask(__name__)

@app.route('/v1/notify/<user_id>', methods=['POST'])
def send_notification(user_id):
    try:
        # Receive the notification message from the Event Processing Service
        data = request.json
        message = data['message']
        # Logic to send the notification to the user
        print(f"Notification sent to user {user_id}: {message}")
        return "Notification sent", 200
    except Exception as e:
        # Log the exception
        print(f"Error sending notification: {str(e)}")
        return "Error sending notification", 500

if __name__ == '__main__':
    app.run(debug=True)