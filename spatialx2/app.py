from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/notify', methods=['POST'])
def process_event():
    try:
        print("===========================")
        print(request)
        event_data = request.json
        print(event_data)
        print("===========================")
        return jsonify({'success': True, 'message': 'Notification sent successfully'}), 200

    except Exception as e:
        return str(e), 500  # Return error message with HTTP status code 500

if __name__ == "__main__":
    app.run(debug=True,port=5001)
