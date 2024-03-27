from flask import Blueprint, request
from app.services.event_service import EventService

# Create a blueprint
bp = Blueprint('routes', __name__)

def register_routes(app):
    @app.route('/v1/event', methods=['POST'])
    def process_event():
        try:
            event_data = request.json
            EventService.process_event(event_data)
            return "Event processed successfully", 200
        except Exception as e:
            return str(e), 500  # Return error message with HTTP status code 500
