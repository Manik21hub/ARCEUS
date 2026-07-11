# core/overlay.py
import webview
import json
import os
import time

class ArceusOverlayAPI:
    def __init__(self, cmd_file):
        self.window = None
        self.cmd_file = cmd_file

    def hide_window(self):
        """Called by the HTML UI when you click the 'X' button."""
        if self.window:
            self.window.hide()
            try:
                with open(self.cmd_file, "r") as f:
                    data = json.load(f)
                data["stream_url"] = "" # Wipe URL so it doesn't auto-play later
                with open(self.cmd_file, "w") as f:
                    json.dump(data, f)
            except:
                pass

class ArceusOverlay:
    def __init__(self):
        self.cmd_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "overlay.json"))
        self.current_url = ""
        self.api = ArceusOverlayAPI(self.cmd_file)

    def loop(self, window):
        self.api.window = window
        while True:
            time.sleep(0.5)
            if not os.path.exists(self.cmd_file):
                continue
                
            try:
                with open(self.cmd_file, "r") as f:
                    data = json.load(f)

                # 1. Play New Stream
                if "stream_url" in data and data["stream_url"] != self.current_url:
                    self.current_url = data["stream_url"]
                    if self.current_url.strip():
                        # We inject the raw stream and title directly into our custom HTML UI
                        title = data.get("title", "ARCEUS Media").replace("'", "\\'")
                        window.evaluate_js(f"setStream('{self.current_url}', '{title}');")
                        window.show()
                    else:
                        window.hide()

                # 2. Controls
                action = data.get("action")
                if action == "pause":
                    window.evaluate_js("document.getElementById('vid-player').pause();")
                    data["action"] = "none"
                    self._save_state(data)
                elif action == "play":
                    window.evaluate_js("document.getElementById('vid-player').play();")
                    data["action"] = "none"
                    self._save_state(data)
                elif action == "hide":
                    window.hide()
                    data["action"] = "none"
                    self._save_state(data)

            except Exception:
                pass 

    def _save_state(self, data):
        try:
            with open(self.cmd_file, "w") as f:
                json.dump(data, f)
        except:
            pass

# ==========================================
# THE NATIVE CUSTOM PLAYER UI (HTML/CSS)
# ==========================================
LOCAL_PLAYER_UI = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html { 
            margin: 0; padding: 0; width: 100vw; height: 100vh; 
            overflow: hidden; background-color: transparent; 
            font-family: 'Segoe UI', sans-serif; 
        }
        /* The pure video element, stretched edge-to-edge seamlessly */
        video { 
            width: 100vw; height: 100vh; object-fit: cover; 
            background-color: black; border-radius: 8px;
        }
        
        /* The custom floating UI bar */
        #arceus-ui {
            position: fixed; top: 0; left: 0; width: 100vw; height: 50px;
            background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 15px; box-sizing: border-box;
            opacity: 0; transition: opacity 0.3s ease; z-index: 9999;
            -webkit-app-region: drag; /* Makes the top bar draggable by your mouse */
        }
        
        /* Show UI when mouse hovers over the window */
        body:hover #arceus-ui { opacity: 1; }
        
        .tools { display: flex; align-items: center; gap: 15px; -webkit-app-region: no-drag; }
        .title { color: #00e5ff; font-weight: bold; font-size: 13px; text-shadow: 1px 1px 2px #000; }
        label { color: white; font-size: 12px; font-weight: bold;}
        
        /* Opacity Slider */
        input[type=range] { cursor: pointer; }
        
        /* Close Button */
        .close-btn { 
            background: none; border: none; color: #ff4444; 
            font-size: 20px; font-weight: bold; cursor: pointer; 
            -webkit-app-region: no-drag; transition: 0.2s;
        }
        .close-btn:hover { color: #ff0000; transform: scale(1.1); }
    </style>
</head>
<body>
    <div id="arceus-ui">
        <div class="tools">
            <span class="title" id="vid-title">ARCEUS Media</span>
            <label>Opacity:</label>
            <input type="range" min="10" max="100" value="100" oninput="document.body.style.opacity = this.value / 100;">
        </div>
        <button class="close-btn" onclick="closePlayer()">✕</button>
    </div>
    
    <video id="vid-player" autoplay></video>
    
    <script>
        // Called by Python to inject the raw URL and start playing
        function setStream(url, title) {
            let vid = document.getElementById('vid-player');
            vid.src = url;
            vid.play();
            document.getElementById('vid-title').innerText = title;
        }
        
        // Called by the HTML button to tell Python to hide the window
        function closePlayer() {
            document.getElementById('vid-player').pause();
            if(window.pywebview) { window.pywebview.api.hide_window(); }
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    engine = ArceusOverlay()
    
    # Generate the transparent, frameless native window
    window = webview.create_window(
        'ARCEUS Visual Media',
        html=LOCAL_PLAYER_UI, # <--- Loads our custom UI instead of YouTube.com
        frameless=True,
        transparent=True,     # <--- Allows the opacity slider to reveal your desktop behind it
        on_top=True,
        width=720,
        height=405,
        x=50,
        y=50,
        hidden=True,
        js_api=engine.api
    )
    
    webview.start(engine.loop, window, gui='edgechromium')