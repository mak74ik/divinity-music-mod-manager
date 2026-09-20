#!/usr/bin/env python3
"""
Divinity Music Mod Manager
A modern, minimalist, Windows 11-style audio modding application for Divinity: Original Sin Enhanced Edition.
Created for modder Mizuqa (Nexus Mods).
"""

import os
import sys
import base64
import mimetypes
import platform
import subprocess
import webbrowser
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = get_base_dir()
sys.path.insert(0, PROJECT_DIR)

import webview
from core.taxonomy import CATEGORIES, TRACKS
from core.wem_encoder import convert_audio_to_wem
from core.lspk_packer import build_lspk_pak

class ModManagerApi:
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def get_initial_data(self):
        """Returns categories and track metadata to frontend."""
        return {
            "categories": CATEGORIES,
            "tracks": TRACKS
        }

    def pick_audio_file(self):
        """Opens native file open dialog for audio files."""
        if not self._window:
            return None

        # On Cocoa, pass clean extensions without wildcards for better compatibility
        file_types = (
            'Audio Files (*.mp3;*.wav;*.flac;*.ogg;*.m4a;*.aac)',
        )
        try:
            res = self._window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG,
                allow_multiple=False,
                file_types=file_types
            )
            if res and len(res) > 0:
                file_path = res[0]
                return {
                    "filePath": file_path,
                    "fileName": os.path.basename(file_path)
                }
        except Exception as e:
            print(f"pick_audio_file error: {e}")
        return None

    def upload_audio_file(self, wid, file_name, base64_data):
        """
        Saves base64 audio data received from browser Drag & Drop or HTML file input
        to a local directory, guaranteeing file replacement works on all platforms.
        """
        try:
            cache_dir = os.path.expanduser("~/.divinity_music_manager/custom_tracks")
            os.makedirs(cache_dir, exist_ok=True)
            if "," in base64_data:
                base64_data = base64_data.split(",", 1)[1]
            raw_bytes = base64.b64decode(base64_data)
            safe_name = "".join(c for c in file_name if c.isalnum() or c in "._- ")
            out_path = os.path.join(cache_dir, f"{wid}_{safe_name}")
            with open(out_path, "wb") as f:
                f.write(raw_bytes)
            return {
                "filePath": out_path,
                "fileName": file_name
            }
        except Exception as e:
            print(f"upload_audio_file error: {e}")
            return None

    def pick_save_location(self, default_name="z_Custom_Music.pak"):
        """Opens native save file dialog for output pak."""
        if not self._window:
            return None

        # Check default game directory if it exists
        default_dir = os.path.expanduser("~/Desktop")
        game_data_mac = os.path.expanduser(
            "~/Library/Application Support/Steam/steamapps/common/Divinity Original Sin Enhanced Edition/Divinity - Original Sin.app/Contents/Data"
        )
        if os.path.exists(game_data_mac):
            default_dir = game_data_mac

        try:
            res = self._window.create_file_dialog(
                dialog_type=webview.SAVE_DIALOG,
                directory=default_dir,
                save_filename=default_name,
                file_types=('Larian Package (*.pak)',)
            )
            if res:
                if isinstance(res, (list, tuple)):
                    return res[0] if len(res) > 0 else None
                return str(res)
        except Exception as e:
            print(f"pick_save_location error: {e}")
        return None

    def get_audio_data_url(self, file_path):
        """Encodes local audio file to base64 data URL for in-app preview."""
        if not os.path.exists(file_path):
            return None

        mime, _ = mimetypes.guess_type(file_path)
        if not mime:
            mime = "audio/mpeg"

        try:
            with open(file_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode('ascii')
            return f"data:{mime};base64,{b64}"
        except Exception as e:
            print(f"Error reading audio preview: {e}")
            return None

    def build_mod(self, mappings, save_path):
        """
        Converts audio files to WEM and packs into LSPK v13 package.
        Emits progress events to webview.
        """
        if not mappings:
            return {"success": False, "error": "No tracks selected for replacement"}

        try:
            total = len(mappings)
            # Find unique audio inputs to convert each only once
            unique_inputs = {}
            for m in mappings:
                inp = m["inputAudioPath"]
                if inp not in unique_inputs:
                    unique_inputs[inp] = m["fileName"]

            unique_total = len(unique_inputs)
            converted_wems = {}

            # Convert each unique audio file
            for i, (audio_path, file_name) in enumerate(unique_inputs.items()):
                percent = int(((i) / unique_total) * 90)
                if self._window:
                    clean_name = file_name.replace("'", "\\'")
                    self._window.evaluate_js(
                        f"window.onBuildProgress({i + 1}, {unique_total}, '{clean_name}', {percent})"
                    )

                wem_bytes = convert_audio_to_wem(audio_path)
                converted_wems[audio_path] = wem_bytes

            # Map into { pak_path: wem_bytes }
            if self._window:
                self._window.evaluate_js(
                    f"window.onBuildProgress({unique_total}, {unique_total}, 'Packing LSPK archive...', 95)"
                )

            payloads = {}
            for m in mappings:
                pak_rel_path = m["pakPath"]
                audio_path = m["inputAudioPath"]
                payloads[pak_rel_path] = converted_wems[audio_path]

            # Build final LSPK v13 pak
            count, size_bytes = build_lspk_pak(payloads, save_path, priority=150)
            size_mb = round(size_bytes / (1024 * 1024), 2)

            return {
                "success": True,
                "sizeMb": size_mb,
                "entries": count
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def open_folder(self, file_path):
        """Reveals file in system file manager (Finder / Explorer)."""
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.run(["open", "-R", file_path])
            elif system == "Windows":
                subprocess.run(["explorer", "/select,", os.path.normpath(file_path)])
            else:
                subprocess.run(["xdg-open", os.path.dirname(file_path)])
        except Exception as e:
            print(f"Error opening folder: {e}")

    def open_external_url(self, url):
        """Opens URL in default web browser."""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening browser: {e}")

def main():
    api = ModManagerApi()
    html_path = os.path.join(PROJECT_DIR, "web", "index.html")

    window = webview.create_window(
        title="Divinity Music Mod Manager — by Mizuqa",
        url=f"file://{html_path}",
        js_api=api,
        width=1160,
        height=780,
        min_size=(960, 640),
        background_color="#121212"
    )
    api.set_window(window)

    webview.start(debug=False)

if __name__ == "__main__":
    main()
