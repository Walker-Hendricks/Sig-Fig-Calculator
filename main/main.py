import webview
import threading
import GUI

def start_panel_server():
    GUI.fireItUp()  # This will start the panel server

# Start the Panel server in a separate thread
server_thread = threading.Thread(target=start_panel_server)
server_thread.daemon = True
server_thread.start()

# Create a webview window displaying the Panel app
webview.create_window('Sig Fig Calculator (With Error!)', 'http://localhost:5006')
webview.start()
