from flask import Flask, request
from app.services.event_service import EventService

app = Flask(__name__)

@app.route('/v1/event', methods=['POST'])
def process_event():
    try:
        event_data = request.json
        msg = EventService.process_event(event_data)
        return "Event processed successfully - "+ msg, 200
    except Exception as e:
        return str(e), 500  # Return error message with HTTP status code 500

if __name__ == "__main__":
    app.run(debug=True)
