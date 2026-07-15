# core/features.py
import json
import re
import os
from pathlib import Path
import yt_dlp
import webbrowser
import subprocess
import urllib.parse
import time
import pyautogui

class FeatureManager:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        config_dir = project_root / "config"
        config_dir.mkdir(exist_ok=True)
        self.cmd_file = str(config_dir / "overlay.json")

    def _update_overlay(self, data_dict):
        try:
            current_state = {}
            if os.path.exists(self.cmd_file):
                with open(self.cmd_file, "r") as f:
                    current_state = json.load(f)
        except:
            current_state = {}
            
        current_state.update(data_dict)
        with open(self.cmd_file, "w") as f:
            json.dump(current_state, f)

    def _extract_playlist(self, query):
        """Extracts a queue of 3 related tracks for the next/prev buttons."""
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True, # <--- This kills the terminal spam
            'default_search': 'ytsearch3' 
        }
        playlist = []
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        url = entry.get('url')
                        if url:
                            playlist.append({
                                "url": url,
                                "title": entry.get('title', 'ARCEUS Media')
                            })
        except Exception as e:
            print(f"[Queue Extraction Error]: {e}")
        return playlist

    def execute_structural_intent(self, ai_output):
        print(f"[Engine Received]: {ai_output}")
        if not ai_output or ai_output == "None":
            return "Cognitive frame dropped."
        
        

        # 1. PLAY MEDIA INTENT
        if "[INTENT:PLAY]" in ai_output:
            query_match = re.search(r'\[QUERY:(.*?)\]', ai_output)
            if query_match:
                query = query_match.group(1).strip()
                print(f"[System] Building media queue for: {query}...")
                
                playlist = self._extract_playlist(query)
                
                if playlist:
                    # Send the full playlist array and trigger the 'play_new' action
                    self._update_overlay({
                        "playlist": playlist,
                        "track_index": 0,
                        "action": "play_new"
                    })
                    return f"Deploying a {len(playlist)}-track queue for {query}."
                return f"I could not extract a clean stream for {query}."

        # 2. MEDIA CONTROLS & OPACITY ADJUSTMENT
        elif "[INTENT:MEDIA]" in ai_output:
            action_match = re.search(r'\[ACTION:(.*?)\]', ai_output)
            if action_match:
                action = action_match.group(1).strip().upper()
                
                if "OPACITY_" in action:
                    try:
                        opacity_val = int(action.split("_")[1])
                        self._update_overlay({"opacity": opacity_val})
                        return f"Setting player transparency to {opacity_val} percent."
                    except Exception:
                        pass
                
                if action == "PAUSE":
                    self._update_overlay({"action": "pause"})
                    return "Media paused."
                elif action in ["PLAY", "RESUME"]:
                    self._update_overlay({"action": "play"})
                    return "Media resumed."
                elif action == "NEXT":
                    self._update_overlay({"action": "next"})
                    return "Skipping to the next track."

        # 3. CHAT INTENT
        elif "[INTENT:CHAT]" in ai_output:
            resp_match = re.search(r'\[RESPONSE:(.*?)\]', ai_output)
            if resp_match:
                return resp_match.group(1).strip()
            
        elif "[INTENT:SYSTEM]" in ai_output:
            action_match = re.search(r'\[ACTION:(.*?)\]', ai_output)
            target_match = re.search(r'\[TARGET:(.*?)\]', ai_output)
            
            if action_match and target_match:
                action = action_match.group(1).strip().upper()
                target = target_match.group(1).strip().lower()
                
                if action == "OPEN":
                    # Simple OS routing for common Windows applications
                    try:
                        if "browser" in target or "chrome" in target:
                            subprocess.Popen("start chrome", shell=True)
                        elif "code" in target or "vs" in target:
                            subprocess.Popen("code", shell=True)
                        elif "spotify" in target:
                            subprocess.Popen("start spotify", shell=True)
                        elif "notepad" in target:
                            subprocess.Popen("notepad", shell=True)
                        elif "calculator" in target:
                            subprocess.Popen("calc", shell=True)
                        else:
                            # Fallback: Ask Windows to try and find the app natively
                            subprocess.Popen(f"start {target}", shell=True)
                            
                        return f"Initializing {target}."
                    except Exception as e:
                        return f"I encountered a system error attempting to launch {target}."

                elif action == "CLOSE":
                    try:
                        # Force kills the app in Windows
                        subprocess.Popen(f"taskkill /F /IM {target}.exe", shell=True)
                        return f"Terminating {target}."
                    except:
                        return f"I could not locate a running process for {target}."
                
                elif action == "COMMAND":
                    if "lock" in target:
                        subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
                        return "Locking system workstation."
            
            return "System directive was incomplete."

        # 4. WEB SEARCH INTENT
        elif "[INTENT:SEARCH]" in ai_output:
            query_match = re.search(r'\[QUERY:(.*?)\]', ai_output)
            if query_match:
                search_query = query_match.group(1).strip()
                print(f"[System] Initiating Web Search: {search_query}")
                
                # Formats the query for Google and opens it in your default browser
                url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
                webbrowser.open(url)
                
                return f"Running a global search protocol for {search_query}."


        # 3. AUTONOMOUS AGENT INTENT (Multi-Step Thinking)
       # 3. AUTONOMOUS AGENT INTENT (Multi-Step Thinking & OS Control)
        elif "[INTENT:AGENT]" in ai_output:
            thought_match = re.search(r'\[THOUGHT:(.*?)\]', ai_output)
            if thought_match:
                print(f"\n[ARCEUS Cognitive Process]: {thought_match.group(1).strip()}\n")

            commands = re.findall(r'\[CMD:(.*?)\|(.*?)\]', ai_output)
            if not commands:
                return "My agentic loop failed to generate an execution sequence."

            print(f"[System] Executing {len(commands)}-step autonomous sequence...")
            
            for action, target in commands:
                action = action.strip().upper()
                target = target.strip().lower() # Lowercase ensures hotkeys map correctly
                
                try:
                    if action == "OPEN":
                        if "chrome" in target or "browser" in target:
                            subprocess.Popen("start chrome", shell=True)
                        elif "brave" in target:
                            subprocess.Popen("start brave", shell=True)
                        else:
                            subprocess.Popen(f"start {target}", shell=True)
                        time.sleep(1.2) # Allow OS to bring window to foreground
                        
                    elif action == "SEARCH":
                        url = f"https://www.google.com/search?q={urllib.parse.quote(target)}"
                        webbrowser.open(url)
                        time.sleep(1.5)
                        
                    elif action == "TYPE":
                        pyautogui.write(target, interval=0.02)
                        
                    elif action == "HOTKEY":
                        # Splits complex chords (ctrl+w) or executes single keys (playpause)
                        keys = target.split('+')
                        pyautogui.hotkey(*keys)
                        time.sleep(0.3)
                        
                except Exception as e:
                    print(f"[Agent Warning] Step failed: {action}|{target} - {e}")
            
            return "Task sequence complete, sir."   

        clean_text = re.sub(r'\[INTENT:.*?\]|\[RESPONSE:.*?\]|\[QUERY:.*?\]|\[ACTION:.*?\]', '', ai_output)
        return clean_text.strip() if clean_text.strip() else "Executed."