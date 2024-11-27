import websocket
import threading
import time
import json

# User details
username = "test_user"  

def on_message(ws, message):
    # Parse the incoming message
    try:
        # WebSocket protocol prepends '42' to custom messages
        if message.startswith("42"):
            data = json.loads(message[2:])  # Remove '42' and parse JSON
            event = data[0]
            payload = data[1]
            
            if event == "room_message":
                msg_username = payload.get("username", "Unknown")
                msg_text = payload.get("message", "")
                print(f"{msg_username}: {msg_text}")  # Format as 'username: message'
            else:
                print(f"Unhandled event: {event}")
        else:
            print(f"Non-standard message: {message}")
    except Exception as e:
        print(f"Error parsing message: {e}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    def send_messages():
        # Join the room
        join_event = json.dumps(["join", {"room": "test_room"}, {"username": username}])
        ws.send(f'42{join_event}')
        print(f"{username} joined room 'test_room'")

        time.sleep(1)  # Wait briefly before sending a message

        # Send a message with the username included
        message_event = json.dumps([
            "send_message",
            {"room": "test_room", "message": "Hello World!", "username": username}
        ])
        ws.send(f'42{message_event}')
        print(f"Message sent: {username}: Hello World!")

    threading.Thread(target=send_messages).start()

ws = websocket.WebSocketApp(
    "ws://127.0.0.1:5000/socket.io/?EIO=4&transport=websocket&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjcxOTA4NSwianRpIjoiM2JkYmMyZDUtYTNiMi00ZDZkLTk4MGYtOWNhZTY0ZDYyNTJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJhcnJ5IiwibmJmIjoxNzMyNzE5MDg1LCJjc3JmIjoiOTNjOTYxZWMtNTM2MS00NzVhLTlhNTUtYzlhYTgxOGJlYjQ1IiwiZXhwIjoxNzMyNzIyNjg1LCJ1c2VyX2lkIjoiMSJ9.7fWkRubkeCYN29shneqH_sm3oxH2wIQbSaPP-5-WysM",
    on_message=on_message,
    on_error=on_error
)
ws.on_open = on_open
ws.run_forever()