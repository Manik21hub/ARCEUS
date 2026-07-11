# core/features.py
import json
import re
import os
from pathlib import Path
import yt_dlp

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

    def _extract_direct_stream(self, query):
        """Uses yt-dlp to silently extract the raw, ad-free .mp4 URL."""
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1' # Grabs the #1 search result instantly
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                    return entry['url'], entry.get('title', 'ARCEUS Media')
        except Exception as e:
            print(f"[Stream Extraction Error]: {e}")
        return None, None

    def execute_structural_intent(self, ai_output):
        print(f"[Engine Received]: {ai_output}")
        if not ai_output or ai_output == "None":
            return "Cognitive frame dropped."

        # 1. PLAY MEDIA INTENT
        if "[INTENT:PLAY]" in ai_output:
            query_match = re.search(r'\[QUERY:(.*?)\]', ai_output)
            if query_match:
                query = query_match.group(1).strip()
                
                print(f"[System] Extracting raw stream for: {query}...")
                stream_url, title = self._extract_direct_stream(query)
                
                if stream_url:
                    self._update_overlay({"stream_url": stream_url, "title": title, "action": "none"})
                    return f"Deploying {query} to the visual overlay."
                return f"I could not extract a clean stream for {query}."
            return "The playback request arrived without attributes."

        # 2. MEDIA CONTROLS
        elif "[INTENT:MEDIA]" in ai_output:
            action_match = re.search(r'\[ACTION:(.*?)\]', ai_output)
            if action_match:
                action = action_match.group(1).strip().upper()
                if action == "PAUSE":
                    self._update_overlay({"action": "pause"})
                    return "Media paused."
                elif action in ["PLAY", "RESUME"]:
                    self._update_overlay({"action": "play"})
                    return "Media resumed."

        # 3. CHAT INTENT
        elif "[INTENT:CHAT]" in ai_output:
            resp_match = re.search(r'\[RESPONSE:(.*?)\]', ai_output)
            if resp_match:
                return resp_match.group(1).strip()

        clean_text = re.sub(r'\[INTENT:.*?\]|\[RESPONSE:.*?\]|\[QUERY:.*?\]|\[ACTION:.*?\]', '', ai_output)
        return clean_text.strip() if clean_text.strip() else "Executed."