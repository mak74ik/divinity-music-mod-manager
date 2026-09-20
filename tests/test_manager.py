"""
Unit & Integration Tests for Divinity Music Mod Manager
"""

import os
import sys
import struct
import lz4.block
import tempfile
import unittest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from core.taxonomy import CATEGORIES, TRACKS, get_track_by_wid, get_tracks_by_category
from core.wem_encoder import convert_audio_to_wem
from core.lspk_packer import build_lspk_pak
from app import ModManagerApi

class TestDivinityMusicManager(unittest.TestCase):
    def test_01_taxonomy(self):
        """Verify all 106 in-game music tracks and categories."""
        self.assertEqual(len(TRACKS), 106, "Must contain exactly 106 in-game music tracks")
        self.assertGreater(len(CATEGORIES), 5, "Must have defined categories")

        # Verify main menu track exists
        menu_track = get_track_by_wid("73372589")
        self.assertIsNotNone(menu_track, "Main menu track 73372589 must exist")
        self.assertEqual(menu_track["category"], "menu")

        # Verify combat tracks exist
        combat_tracks = get_tracks_by_category("combat")
        self.assertGreaterEqual(len(combat_tracks), 10, "Combat category must have 10+ tracks")

    def test_02_audio_to_wem_conversion(self):
        """Test audio conversion from MP3 to Wwise Vorbis WEM format."""
        test_mp3 = "/tmp/test_sine.mp3"
        self.assertTrue(os.path.exists(test_mp3), "Test MP3 must exist")

        wem_bytes = convert_audio_to_wem(test_mp3)
        self.assertGreater(len(wem_bytes), 1000, "WEM bytes must be non-empty")
        self.assertTrue(wem_bytes.startswith(b"RIFF"), "Must start with RIFF")
        self.assertIn(b"WAVE", wem_bytes[:16], "Must be WAVE format")
        self.assertIn(b"fmt ", wem_bytes[:32], "Must contain fmt chunk")
        self.assertIn(b"data", wem_bytes[:300], "Must contain data chunk")

        # Verify seek table interval (interval of 8192 samples)
        # Parse fmt chunk to verify codebook UID 0xa61035a7
        fmt_pos = wem_bytes.find(b"fmt ")
        self.assertNotEqual(fmt_pos, -1)
        fmt_size = struct.unpack("<I", wem_bytes[fmt_pos+4:fmt_pos+8])[0]
        fmt_data = wem_bytes[fmt_pos+8:fmt_pos+8+fmt_size]
        # uHashCodebook is located at offset 60 in extra fmt chunk
        codebook_uid = struct.unpack("<I", fmt_data[60:64])[0]
        self.assertEqual(hex(codebook_uid), "0xa61035a7", "Must match engine codebook UID 0xa61035a7")

    def test_03_lspk_packing_and_deduplication(self):
        """Test LSPK v13 package builder with LZ4 compression and deduplication."""
        test_mp3 = "/tmp/test_sine.mp3"
        wem_bytes = convert_audio_to_wem(test_mp3)

        payloads = {
            "Public/Main/Assets/Sound/73372589.wem": wem_bytes,
            "Public/Main/Assets/Sound/210066779.wem": wem_bytes, # Same payload -> should deduplicate
            "Public/Main/Assets/Sound/226631273.wem": wem_bytes,
        }

        with tempfile.NamedTemporaryFile(suffix=".pak", delete=False) as tmp_pak:
            tmp_pak_path = tmp_pak.name

        try:
            count, size_bytes = build_lspk_pak(payloads, tmp_pak_path, priority=150)
            self.assertEqual(count, 3, "Should pack 3 entries")

            # Size of pak with deduplication should be slightly larger than 1 payload, not 3x!
            self.assertLess(size_bytes, len(wem_bytes) * 2, "Deduplication should keep pak small")

            # Decompress and verify LSPK v13 trailer
            with open(tmp_pak_path, "rb") as f:
                f.seek(-40, 2)
                trailer = f.read(40)
                v, fl_off, fl_sz, parts, flags, prio, _, _, sig = struct.unpack("<IIIHBB16sI4s", trailer)
                self.assertEqual(v, 13, "LSPK version must be 13")
                self.assertEqual(sig, b"LSPK", "Signature must be LSPK")
                self.assertEqual(parts, 1, "NumParts must be strictly 1")
                self.assertEqual(prio, 150, "Priority must be 150")

                # Decompress file list
                f.seek(fl_off)
                fl_block = f.read(fl_sz)
                num_entries = struct.unpack("<I", fl_block[:4])[0]
                self.assertEqual(num_entries, 3)
                decomp = lz4.block.decompress(fl_block[4:], uncompressed_size=num_entries * 280)
                self.assertEqual(len(decomp), num_entries * 280)
        finally:
            if os.path.exists(tmp_pak_path):
                os.remove(tmp_pak_path)

    def test_04_api_bridge(self):
        """Test ModManagerApi data fetching and audio preview encoding."""
        api = ModManagerApi()
        init_data = api.get_initial_data()
        self.assertIn("categories", init_data)
        self.assertIn("tracks", init_data)
        self.assertEqual(len(init_data["tracks"]), 106)

        test_mp3 = "/tmp/test_sine.mp3"
        data_url = api.get_audio_data_url(test_mp3)
        self.assertTrue(data_url.startswith("data:audio/"), "Must return valid audio data URL")

if __name__ == "__main__":
    unittest.main()
