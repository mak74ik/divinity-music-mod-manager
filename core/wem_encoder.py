"""
WEM Encoder for Divinity: Original Sin Enhanced Edition
Converts any audio file (MP3, WAV, FLAC, OGG, etc.) to Audiokinetic Wwise Vorbis .wem
matching the engine requirements: aoTuV b6.03, q=0.9, codebook UID 0xa61035a7, seek table interval 8192.
"""

import os
import sys
import struct
import subprocess
import tempfile
from pathlib import Path

# Add parent directory to path to import convert_ogg_to_wem
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CORE_DIR)

try:
    from core.convert_ogg_to_wem import (
        load_codebook_library, extract_ogg_packets, strip_setup
    )
except ImportError:
    from convert_ogg_to_wem import (
        load_codebook_library, extract_ogg_packets, strip_setup
    )

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.dirname(CORE_DIR)

def find_ffmpeg():
    base = get_base_dir()
    bundled = os.path.join(base, "bin", "ffmpeg")
    if os.path.exists(bundled) and os.access(bundled, os.X_OK):
        return bundled
    import shutil
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg
    for p in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/usr/bin/ffmpeg"]:
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return "ffmpeg"

def get_aotuv_bin():
    return os.path.join(get_base_dir(), "bin", "aotuv_enc")

def get_codebooks_bin():
    return os.path.join(get_base_dir(), "assets", "packed_codebooks_aoTuV_603.bin")

def get_default_chunks_bin():
    return os.path.join(get_base_dir(), "assets", "default_cue_list.bin")

_PCB_LIB = None
_CUE_LIST_CHUNKS = None

def get_codebook_lib():
    global _PCB_LIB
    if _PCB_LIB is None:
        c_bin = get_codebooks_bin()
        if not os.path.exists(c_bin):
            raise FileNotFoundError(f"Codebooks library not found at {c_bin}")
        _PCB_LIB = load_codebook_library(c_bin)
    return _PCB_LIB

def get_default_cue_list():
    global _CUE_LIST_CHUNKS
    if _CUE_LIST_CHUNKS is None:
        d_bin = get_default_chunks_bin()
        if os.path.exists(d_bin):
            with open(d_bin, "rb") as f:
                _CUE_LIST_CHUNKS = f.read()
        else:
            _CUE_LIST_CHUNKS = b""
    return _CUE_LIST_CHUNKS

def ogg_packet_to_wem(op):
    if len(op) <= 2:
        val = int.from_bytes(op, 'little')
        mode = (val >> 1) & 1
        return bytes([mode])
    val = int.from_bytes(op, 'little')
    mode = (val >> 1) & 1
    if mode == 0:
        wem_val = val >> 1
    else:
        wem_val = 1 | ((val >> 4) << 1)
    target_len = max(1, (wem_val.bit_length() + 7) // 8)
    return wem_val.to_bytes(target_len, 'little')

def convert_audio_to_wem(input_path: str, ffmpeg_bin: str = None) -> bytes:
    """
    Converts any audio file to Wwise Vorbis WEM format bytes.
    Applies EBU R128 loudness normalization and resamples to 44.1kHz stereo.
    """
    if ffmpeg_bin is None:
        ffmpeg_bin = find_ffmpeg()

    pcb_lib = get_codebook_lib()
    cue_list = get_default_cue_list()
    cue_chunk = cue_list[:84] if len(cue_list) >= 84 else b""
    list_chunk = cue_list[84:184] if len(cue_list) >= 184 else b""

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_pcm = os.path.join(tmp_dir, "audio.raw")
        ogg_path = os.path.join(tmp_dir, "audio.ogg")

        # 1. Normalize loudness and resample to 44.1kHz 16-bit stereo raw PCM
        cmd_ffmpeg = [
            ffmpeg_bin, "-y", "-i", input_path,
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-ar", "44100", "-ac", "2", "-f", "s16le", raw_pcm
        ]
        res = subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg audio processing failed for {input_path}")

        # 2. Encode with aoTuV at quality 0.9
        cmd_enc = [
            get_aotuv_bin(), raw_pcm, ogg_path, "0.9", "2", "44100"
        ]
        res = subprocess.run(cmd_enc, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            raise RuntimeError("aoTuV Vorbis encoding failed")

        # 3. Read OGG
        with open(ogg_path, "rb") as f:
            ogg_bytes = f.read()

        packets, granules = extract_ogg_packets(ogg_bytes)
        channels = 2
        sample_rate = 44100
        bs0 = 8
        bs1 = 11
        short_bs = 1 << bs0
        long_bs = 1 << bs1

        setup_bytes, mode_blockflag, mode_bits = strip_setup(packets[2], channels, pcb_lib)
        setup_chunk = struct.pack('<H', len(setup_bytes)) + setup_bytes
        setup_chunk_len = len(setup_chunk)

        sample_count = max((g for g in granules if g >= 0), default=0)

        audio_blob = bytearray()
        seek_table = bytearray()
        max_packet = 0
        prev_bs = -1
        cum = 0
        last_sample = 0
        last_offset = 0
        seek_interval = 8192

        for p in packets[3:]:
            payload = ogg_packet_to_wem(p)
            mode = (p[0] >> 1) & 1
            cur_bs = long_bs if mode == 1 else short_bs
            if prev_bs >= 0:
                cum += (prev_bs + cur_bs) // 4
            prev_bs = cur_bs

            pkt_offset = setup_chunk_len + len(audio_blob)
            if (cum - last_sample) >= seek_interval:
                seek_table.extend(struct.pack('<H', cum - last_sample))
                seek_table.extend(struct.pack('<H', pkt_offset - last_offset))
                last_sample = cum
                last_offset = pkt_offset

            if len(payload) > max_packet:
                max_packet = len(payload)
            audio_blob.extend(struct.pack('<H', len(payload)))
            audio_blob.extend(payload)

        last_granule_extra = max(0, cum - sample_count)
        data_payload = bytes(seek_table) + setup_chunk + bytes(audio_blob)
        seek_size = len(seek_table)
        audio_offset = seek_size + setup_chunk_len
        data_size = len(data_payload)

        avg_bytes = 34557
        decode_alloc = 19776
        x64_alloc = 20272
        uid = 0xa61035a7
        subtype = 3

        fmtc = struct.pack('<HHIIHH' 'H' 'H' 'I' 'I' 'I' 'I' 'H' 'H' 'I' 'I' 'H' 'H' 'I' 'I' 'I' 'BB',
            0xFFFF, channels, sample_rate, avg_bytes, 0, 0,
            0x30,
            0,
            subtype,
            sample_count,
            setup_chunk_len,
            data_size - seek_size,
            0,
            last_granule_extra,
            seek_size,
            audio_offset,
            max_packet,
            last_granule_extra,
            decode_alloc,
            x64_alloc,
            uid,
            bs0, bs1
        )

        riff_body = bytearray()
        riff_body.extend(b'WAVE')
        riff_body.extend(b'fmt ')
        riff_body.extend(struct.pack('<I', len(fmtc)))
        riff_body.extend(fmtc)
        if cue_chunk:
            riff_body.extend(cue_chunk)
        if list_chunk:
            riff_body.extend(list_chunk)
        riff_body.extend(b'data')
        riff_body.extend(struct.pack('<I', len(data_payload)))
        riff_body.extend(data_payload)

        wem = b'RIFF' + struct.pack('<I', len(riff_body)) + bytes(riff_body)
        return wem
