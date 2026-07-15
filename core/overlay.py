# core/overlay.py
import webview
import json
import os
import time
import ctypes

# Windows OS-Level Transparency Constants
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002

def set_os_opacity(window_title, opacity_percent):
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
        if hwnd:
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            if not (style & WS_EX_LAYERED):
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
            
            alpha = int((opacity_percent / 100.0) * 255)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)
    except Exception:
        pass

class ArceusOverlayAPI:
    def __init__(self, overlay_instance):
        self.overlay = overlay_instance
        self.anchor_x = 0
        self.anchor_y = 0

    def hide_window(self):
        if self.overlay.window:
            self.overlay.window.hide()
            self.overlay.update_state({"action": "none", "playlist": []})

    def start_resize(self):
        """Called the microsecond you click the handle to lock the top-left anchor."""
        if self.overlay.window:
            self.anchor_x = self.overlay.window.x
            self.anchor_y = self.overlay.window.y

    def resize_window(self, width, height):
        """Resizes the window and forcibly pins it to the anchor."""
        if self.overlay.window:
            w = max(400, int(width))
            h = max(225, int(height))
            self.overlay.window.resize(w, h)
            # FIX: Force the OS to maintain the original top-left corner
            self.overlay.window.move(self.anchor_x, self.anchor_y)

    def set_opacity(self, value):
        set_os_opacity('ARCEUS Visual Media', float(value))

    def next_track(self):
        self.overlay.play_next()

    def prev_track(self):
        self.overlay.play_prev()

class ArceusOverlay:
    def __init__(self):
        self.cmd_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "overlay.json"))
        self.window = None
        self.api = ArceusOverlayAPI(self)
        self.playlist = []
        self.track_index = 0

    def play_next(self):
        if not self.playlist: return
        self.track_index = (self.track_index + 1) % len(self.playlist)
        self.apply_current_track()
        self.update_state({"track_index": self.track_index})

    def play_prev(self):
        if not self.playlist: return
        self.track_index = (self.track_index - 1) % len(self.playlist)
        self.apply_current_track()
        self.update_state({"track_index": self.track_index})

    def apply_current_track(self):
        if self.playlist and 0 <= self.track_index < len(self.playlist):
            track = self.playlist[self.track_index]
            title = track['title'].replace("'", "\\'")
            self.window.evaluate_js(f"setStream('{track['url']}', '{title}');")
            self.window.show()

    def update_state(self, data_dict):
        try:
            with open(self.cmd_file, "r") as f:
                data = json.load(f)
            data.update(data_dict)
            with open(self.cmd_file, "w") as f:
                json.dump(data, f)
        except:
            pass

    def loop(self, window):
        self.window = window
        while True:
            time.sleep(0.4)
            if not os.path.exists(self.cmd_file):
                continue
                
            try:
                with open(self.cmd_file, "r") as f:
                    data = json.load(f)

                if data.get("action") == "play_new":
                    self.playlist = data.get("playlist", [])
                    self.track_index = data.get("track_index", 0)
                    self.apply_current_track()
                    data["action"] = "none"
                    self.update_state(data)

                action = data.get("action")
                if action == "pause":
                    window.evaluate_js("document.getElementById('vid-player').pause(); document.getElementById('play-btn').innerHTML = '▶';")
                    self.update_state({"action": "none"})
                elif action == "play":
                    window.evaluate_js("document.getElementById('vid-player').play(); document.getElementById('play-btn').innerHTML = '⏸';")
                    self.update_state({"action": "none"})
                elif action == "next":
                    self.play_next()
                    self.update_state({"action": "none"})
                elif action == "hide":
                    window.hide()
                    self.update_state({"action": "none"})

                if "opacity" in data:
                    target = data["opacity"]
                    window.evaluate_js(f"document.getElementById('opacity-slider').value = {target};")
                    set_os_opacity('ARCEUS Visual Media', float(target))
                    del data["opacity"]
                    with open(self.cmd_file, "w") as f:
                        json.dump(data, f)

            except Exception:
                pass 

# ==========================================
# THE NATIVE INTERACTIVE UI (HTML/CSS/JS)
# ==========================================
LOCAL_PLAYER_UI = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html { 
            margin: 0; padding: 0; width: 100vw; height: 100vh; 
            overflow: hidden; background-color: #000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            user-select: none;
        }
        
        video { 
            width: 100vw; height: 100vh; object-fit: cover; 
            background-color: #000; border-radius: 8px;
        }
        
        #top-bar {
            position: fixed; top: 0; left: 0; width: 100vw; height: 40px;
            background: linear-gradient(to bottom, rgba(0,0,0,0.85), transparent);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 15px; box-sizing: border-box;
            opacity: 0; transition: opacity 0.3s ease; z-index: 9999;
            -webkit-app-region: drag;
        }
        
        #control-deck {
            position: fixed; bottom: 0; left: 0; width: 100vw; height: 60px;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            display: flex; justify-content: center; align-items: center; gap: 20px;
            opacity: 0; transition: opacity 0.3s ease; z-index: 9999;
            -webkit-app-region: no-drag;
        }

        body:hover #top-bar, body:hover #control-deck { opacity: 1; }
        
        .title { color: #00e5ff; font-weight: bold; font-size: 13px; text-shadow: 1px 1px 2px #000; letter-spacing: 1px; }
        
        button { background: none; border: none; color: white; font-size: 18px; cursor: pointer; transition: 0.2s; text-shadow: 0px 0px 5px rgba(0,229,255,0.5); }
        button:hover { color: #00e5ff; transform: scale(1.15); }
        .close-btn { color: #ff4444; text-shadow: none; }
        .close-btn:hover { color: #ff0000; }
        
        .controls-wrapper { display: flex; align-items: center; gap: 15px; }
        
        .slider-container {
            position: absolute; right: 25px; bottom: 20px;
            display: flex; align-items: center; gap: 10px;
        }
        .slider-container span { color: #aaa; font-size: 11px; font-weight: bold; text-transform: uppercase; }
        input[type=range] { cursor: pointer; width: 100px; accent-color: #00e5ff; }

        #resize-handle {
            position: fixed; bottom: 0; right: 0; width: 25px; height: 25px;
            cursor: nwse-resize; z-index: 10000;
            background: linear-gradient(135deg, transparent 50%, rgba(0,229,255,0.7) 50%);
            -webkit-app-region: no-drag; 
        }
    </style>
</head>
<body>
    <div id="top-bar">
        <span class="title" id="vid-title">ARCEUS Media Engine</span>
        <button class="close-btn" style="-webkit-app-region: no-drag;" onclick="closePlayer()">✕</button>
    </div>
    
    <div id="control-deck">
        <div class="controls-wrapper">
            <button onclick="prevTrack()" title="Previous Track">⏮</button>
            <button onclick="skip(-10)" title="Back 10s">↺10</button>
            <button id="play-btn" onclick="togglePlay()" style="font-size: 24px;" title="Play/Pause">⏸</button>
            <button onclick="skip(10)" title="Forward 10s">↻10</button>
            <button onclick="nextTrack()" title="Next Track">⏭</button>
        </div>
        
        <div class="slider-container">
            <span>Opacity</span>
            <input type="range" id="opacity-slider" min="20" max="100" value="100" oninput="if(window.pywebview){ window.pywebview.api.set_opacity(this.value); }">
        </div>
    </div>

    <div id="resize-handle"></div>
    <video id="vid-player" autoplay onended="nextTrack()"></video>
    
    <script>
        let vid = document.getElementById('vid-player');
        let playBtn = document.getElementById('play-btn');

        function setStream(url, title) {
            vid.src = url;
            vid.play();
            document.getElementById('vid-title').innerText = title;
            playBtn.innerHTML = '⏸';
        }
        
        function togglePlay() {
            if (vid.paused) { vid.play(); playBtn.innerHTML = '⏸'; } 
            else { vid.pause(); playBtn.innerHTML = '▶'; }
        }
        
        function skip(seconds) { vid.currentTime += seconds; }
        function closePlayer() { vid.pause(); if(window.pywebview) window.pywebview.api.hide_window(); }
        function nextTrack() { if(window.pywebview) window.pywebview.api.next_track(); }
        function prevTrack() { if(window.pywebview) window.pywebview.api.prev_track(); }

        let handle = document.getElementById('resize-handle');
        let startX, startY, startWidth, startHeight;
        
        // FIX: Hardware Throttle to prevent IPC Flooding
        let isResizing = false;

        handle.addEventListener('mousedown', function(e) {
            e.preventDefault();
            startX = e.screenX;
            startY = e.screenY;
            startWidth = window.innerWidth;
            startHeight = window.innerHeight;
            
            // Tell Python to lock the top-left coordinates immediately
            if(window.pywebview) { window.pywebview.api.start_resize(); }

            document.addEventListener('mousemove', resizeWindow);
            document.addEventListener('mouseup', stopResize);
        });

        function resizeWindow(e) {
            // FIX: requestAnimationFrame limits messages to your monitor's refresh rate (60fps)
            if (!isResizing) {
                isResizing = true;
                requestAnimationFrame(() => {
                    if(window.pywebview) {
                        let newWidth = startWidth + (e.screenX - startX);
                        let newHeight = startHeight + (e.screenY - startY);
                        window.pywebview.api.resize_window(newWidth, newHeight);
                    }
                    isResizing = false;
                });
            }
        }
        
        function stopResize() {
            document.removeEventListener('mousemove', resizeWindow);
            document.removeEventListener('mouseup', stopResize);
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    engine = ArceusOverlay()
    
    window = webview.create_window(
        'ARCEUS Visual Media',
        html=LOCAL_PLAYER_UI,
        frameless=True,
        transparent=False, 
        resizable=True,
        on_top=True,
        width=720,
        height=405,
        x=50,
        y=50,
        hidden=True,
        js_api=engine.api
    )
    
    webview.start(engine.loop, window, gui='edgechromium')