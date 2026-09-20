"""
LSPK Package Builder for Divinity: Original Sin Enhanced Edition
Constructs valid LSPK version 13 packages with LZ4 compression, Priority 150,
and payload deduplication.
"""

import os
import struct
import binascii
import lz4.block
from typing import Dict, Tuple

def build_lspk_pak(file_payloads: Dict[str, bytes], output_pak_path: str, priority: int = 150) -> Tuple[int, int]:
    """
    Builds an LSPK v13 package from a dictionary of { pak_relative_path: file_bytes }.
    
    Returns:
        (total_entries, pak_size_in_bytes)
    """
    if not file_payloads:
        raise ValueError("Cannot build an empty pak file")

    # 1. Deduplicate payloads
    # Hash -> (offset, size, crc, raw_bytes)
    unique_payloads = {}
    current_offset = 0
    file_data_blocks = []

    for path, data in sorted(file_payloads.items()):
        crc = binascii.crc32(data) & 0xffffffff
        payload_key = (crc, len(data))
        if payload_key not in unique_payloads:
            unique_payloads[payload_key] = (current_offset, len(data), crc)
            file_data_blocks.append(data)
            current_offset += len(data)
            pad = (4 - (current_offset % 4)) % 4
            if pad > 0:
                file_data_blocks.append(b'\x00' * pad)
                current_offset += pad

    # 2. Build 280-byte FileEntry10 records
    file_entries = []
    for rel_path in sorted(file_payloads.keys()):
        data = file_payloads[rel_path]
        crc = binascii.crc32(data) & 0xffffffff
        payload_key = (crc, len(data))
        off, size, _ = unique_payloads[payload_key]

        name_bytes = rel_path.encode('utf-8')
        if len(name_bytes) > 255:
            raise ValueError(f"Path is too long (> 255 bytes): {rel_path}")
        name_buf = name_bytes + b'\x00' * (256 - len(name_bytes))
        # Struct: offset(4), size_on_disk(4), uncompressed_size(4), part(4), flags(4), crc(4)
        entry = name_buf + struct.pack('<IIIIII', off, size, size, 0, 0, crc)
        file_entries.append(entry)

    # 3. Compress file list using LZ4
    file_list_raw = b''.join(file_entries)
    file_list_comp = lz4.block.compress(file_list_raw, store_size=False)
    file_list_offset = current_offset
    file_list_block = struct.pack('<I', len(file_entries)) + file_list_comp
    file_list_size = len(file_list_block)

    # 4. 40-byte LSPK v13 Trailer
    # struct: Version(4)=13, FileListOffset(4), FileListSize(4), NumParts(2)=1, Flags(1)=0, Priority(1)=150, Hash(16), TrailerSize(4)=40, Signature(4)='LSPK'
    trailer = struct.pack(
        '<IIIHBB16sI4s',
        13,
        file_list_offset,
        file_list_size,
        1,       # NumParts must be 1
        0,       # Flags
        priority, # 150 ensures overriding vanilla Sound.pak
        b'\x00' * 16,
        40,
        b'LSPK'
    )

    # 5. Write to destination
    os.makedirs(os.path.dirname(os.path.abspath(output_pak_path)), exist_ok=True)
    with open(output_pak_path, 'wb') as f:
        for block in file_data_blocks:
            f.write(block)
        f.write(file_list_block)
        f.write(trailer)

    total_size = os.path.getsize(output_pak_path)
    return len(file_entries), total_size
