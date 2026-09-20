import os
import sys
import struct
import math

class BitReader:
    def __init__(self, data, bit_pos=0):
        self.data = data
        self.bit_pos = bit_pos

    def read(self, n):
        res = 0
        for i in range(n):
            byte_idx = self.bit_pos // 8
            bit_idx = self.bit_pos % 8
            bit = (self.data[byte_idx] >> bit_idx) & 1
            res |= (bit << i)
            self.bit_pos += 1
        return res

    def bits_read(self):
        return self.bit_pos

    def get_bit(self):
        byte_idx = self.bit_pos // 8
        bit_idx = self.bit_pos % 8
        bit = (self.data[byte_idx] >> bit_idx) & 1
        self.bit_pos += 1
        return bit

class BitWriter:
    def __init__(self):
        self.buf = bytearray()
        self.cur_byte = 0
        self.bit_pos = 0

    def write(self, val, n):
        for i in range(n):
            bit = (val >> i) & 1
            self.put_bit(bit)

    def put_bit(self, bit):
        self.cur_byte |= (bit << self.bit_pos)
        self.bit_pos += 1
        if self.bit_pos == 8:
            self.buf.append(self.cur_byte)
            self.cur_byte = 0
            self.bit_pos = 0

    def flush_byte(self):
        if self.bit_pos > 0:
            self.buf.append(self.cur_byte)
            self.cur_byte = 0
            self.bit_pos = 0

    def bytes(self):
        return bytes(self.buf)

def ilog(v):
    ret = 0
    while v > 0:
        ret += 1
        v >>= 1
    return ret

def parse_full_codebook(r):
    ident = r.read(24)
    if ident != 0x564342:
        raise ValueError(f"bad ident {hex(ident)}")
    dims = r.read(16)
    entries = r.read(24)
    ordered = r.read(1)
    if ordered:
        init_len = r.read(5)
        numbers = []
        cur = 0
        while cur < entries:
            num = r.read(ilog(entries - cur))
            numbers.append(num)
            cur += num
        lens = None
    else:
        init_len = None
        numbers = None
        sparse = r.read(1)
        lens = []
        for _ in range(entries):
            if sparse:
                flag = r.read(1)
                l = r.read(5) if flag else -1
            else:
                l = r.read(5)
            lens.append(l)
    lookup_type = r.read(4)
    min_v = max_v = val_len = seq_flag = quantvals = None
    if lookup_type == 1:
        min_v = r.read(32)
        max_v = r.read(32)
        val_len = r.read(4)
        seq_flag = r.read(1)
        q = int(entries ** (1.0 / dims))
        while (q+1)**dims <= entries: q += 1
        while q**dims > entries: q -= 1
        quantvals = [r.read(val_len + 1) for _ in range(q)]
    
    key = [dims, entries, ordered, init_len, tuple(numbers or []), tuple(lens or []), lookup_type, min_v, max_v, val_len, seq_flag, tuple(quantvals or [])]
    return tuple(key)

def parse_compact_codebook(r):
    dims = r.read(4)
    entries = r.read(14)
    ordered = r.read(1)
    if ordered:
        init_len = r.read(5)
        numbers = []
        cur = 0
        while cur < entries:
            num = r.read(ilog(entries - cur))
            numbers.append(num)
            cur += num
        lens = None
    else:
        init_len = None
        numbers = None
        cll = r.read(3)
        sparse = r.read(1)
        lens = []
        for _ in range(entries):
            if sparse:
                flag = r.read(1)
                l = r.read(cll) if flag else -1
            else:
                l = r.read(cll)
            lens.append(l)
    lookup_type = r.read(1)
    min_v = max_v = val_len = seq_flag = quantvals = None
    if lookup_type == 1:
        min_v = r.read(32)
        max_v = r.read(32)
        val_len = r.read(4)
        seq_flag = r.read(1)
        q = int(entries ** (1.0 / dims))
        while (q+1)**dims <= entries: q += 1
        while q**dims > entries: q -= 1
        quantvals = [r.read(val_len + 1) for _ in range(q)]
    key = [dims, entries, ordered, init_len, tuple(numbers or []), tuple(lens or []), lookup_type, min_v, max_v, val_len, seq_flag, tuple(quantvals or [])]
    return tuple(key)

def load_codebook_library(pcb_path):
    with open(pcb_path, 'rb') as f:
        data = f.read()
    off_off = struct.unpack('<I', data[-4:])[0]
    count = (len(data) - off_off) // 4
    offsets = [struct.unpack('<I', data[off_off+4*i : off_off+4*i+4])[0] for i in range(count)]
    lib = {}
    for i in range(count - 1):
        cb_bytes = data[offsets[i] : offsets[i+1]]
        try:
            k = parse_compact_codebook(BitReader(cb_bytes))
            if k not in lib:
                lib[k] = i
        except Exception:
            pass
    return lib

def extract_ogg_packets(ogg_bytes):
    packets = []
    idx = 0
    cur_packet = bytearray()
    last_granule = -1
    granules = []
    while idx < len(ogg_bytes):
        if ogg_bytes[idx:idx+4] != b'OggS':
            break
        flags = ogg_bytes[idx+5]
        granule = struct.unpack('<q', ogg_bytes[idx+6:idx+14])[0]
        num_segs = ogg_bytes[idx+26]
        seg_lens = list(ogg_bytes[idx+27 : idx+27+num_segs])
        data_idx = idx + 27 + num_segs
        for s in seg_lens:
            cur_packet.extend(ogg_bytes[data_idx : data_idx + s])
            data_idx += s
            if s < 255:
                packets.append(bytes(cur_packet))
                granules.append(granule)
                cur_packet = bytearray()
        idx = data_idx
    if cur_packet:
        packets.append(bytes(cur_packet))
        granules.append(granule)
    return packets, granules

def strip_setup(packet, channels, lib):
    if len(packet) < 7 or packet[0] != 5 or packet[1:7] != b'vorbis':
        raise ValueError("Not a setup packet")
    r = BitReader(packet, 7 * 8)
    w = BitWriter()

    # Codebooks
    cb_count = r.read(8) + 1
    w.write(cb_count - 1, 8)
    for i in range(cb_count):
        k = parse_full_codebook(r)
        if k not in lib:
            raise ValueError(f"Codebook {i} not found in aoTuV library!")
        cb_id = lib[k]
        w.write(cb_id, 10)

    # Time domain placeholder
    time_count = r.read(6) + 1
    for _ in range(time_count):
        if r.read(16) != 0:
            raise ValueError("Nonzero time domain transform")

    # Floors
    floor_count = r.read(6) + 1
    w.write(floor_count - 1, 6)
    for _ in range(floor_count):
        if r.read(16) != 1:
            raise ValueError("Unexpected floor type")
        partitions = r.read(5)
        w.write(partitions, 5)
        partition_class = []
        max_class = 0
        for _ in range(partitions):
            pc = r.read(4)
            w.write(pc, 4)
            partition_class.append(pc)
            if pc > max_class:
                max_class = pc
        class_dims = [0] * (max_class + 1)
        for j in range(max_class + 1):
            dims_less1 = r.read(3)
            w.write(dims_less1, 3)
            class_dims[j] = dims_less1 + 1
            subclasses = r.read(2)
            w.write(subclasses, 2)
            if subclasses != 0:
                w.write(r.read(8), 8) # masterbook
            for _ in range(1 << subclasses):
                w.write(r.read(8), 8)
        w.write(r.read(2), 2) # multiplier
        rangebits = r.read(4)
        w.write(rangebits, 4)
        for j in range(partitions):
            for _ in range(class_dims[partition_class[j]]):
                w.write(r.read(rangebits), rangebits)

    # Residues
    residue_count = r.read(6) + 1
    w.write(residue_count - 1, 6)
    for _ in range(residue_count):
        residue_type = r.read(16)
        if residue_type > 2:
            raise ValueError("Invalid residue type")
        w.write(residue_type, 2) # Squeeze 16 -> 2 bits!
        w.write(r.read(24), 24)
        w.write(r.read(24), 24)
        w.write(r.read(24), 24)
        classifications = r.read(6) + 1
        w.write(classifications - 1, 6)
        w.write(r.read(8), 8)
        cascade = []
        for _ in range(classifications):
            low = r.read(3)
            w.write(low, 3)
            bitflag = r.read(1)
            w.write(bitflag, 1)
            high = r.read(5) if bitflag else 0
            if bitflag:
                w.write(high, 5)
            cascade.append(high * 8 + low)
        for j in range(classifications):
            for k in range(8):
                if cascade[j] & (1 << k):
                    w.write(r.read(8), 8)

    # Mappings
    mapping_count = r.read(6) + 1
    w.write(mapping_count - 1, 6)
    coupling_bits = ilog(channels - 1)
    for _ in range(mapping_count):
        if r.read(16) != 0:
            raise ValueError("Unexpected mapping type")
        submaps_flag = r.read(1)
        w.write(submaps_flag, 1)
        submaps = 1
        if submaps_flag:
            submaps_less1 = r.read(4)
            w.write(submaps_less1, 4)
            submaps = submaps_less1 + 1
        square_polar = r.read(1)
        w.write(square_polar, 1)
        if square_polar:
            coupling_steps = r.read(8) + 1
            w.write(coupling_steps - 1, 8)
            for _ in range(coupling_steps):
                w.write(r.read(coupling_bits), coupling_bits)
                w.write(r.read(coupling_bits), coupling_bits)
        mapping_reserved = r.read(2)
        w.write(mapping_reserved, 2)
        if mapping_reserved != 0:
            raise ValueError("Mapping reserved nonzero")
        if submaps > 1:
            for _ in range(channels):
                w.write(r.read(4), 4)
        for _ in range(submaps):
            w.write(r.read(8), 8)
            w.write(r.read(8), 8)
            w.write(r.read(8), 8)

    # Modes
    mode_count = r.read(6) + 1
    w.write(mode_count - 1, 6)
    mode_blockflag = []
    mode_bits = ilog(mode_count - 1)
    for _ in range(mode_count):
        blockflag = r.read(1)
        w.write(blockflag, 1)
        mode_blockflag.append(blockflag != 0)
        if r.read(16) != 0 or r.read(16) != 0:
            raise ValueError("Nonzero window/transform type")
        w.write(r.read(8), 8) # mapping

    if r.read(1) != 1:
        raise ValueError("Missing framing bit")

    w.flush_byte()
    return w.bytes(), mode_blockflag, mode_bits

def repack_audio_packet(ogg_pkt, mode_blockflag, mode_bits):
    r = BitReader(ogg_pkt)
    w = BitWriter()
    pkt_type = r.read(1)
    if pkt_type != 0:
        raise ValueError("Audio packet type != 0")
    mode = r.read(mode_bits) if mode_bits > 0 else 0
    w.write(mode, mode_bits)
    if mode_blockflag[mode]:
        r.read(1) # prev window
        r.read(1) # next window
    total_bits = len(ogg_pkt) * 8
    while r.bits_read() < total_bits:
        w.put_bit(r.get_bit())
    w.flush_byte()
    return w.bytes()

def build_wem(ogg_bytes, pcb_lib):
    packets, granules = extract_ogg_packets(ogg_bytes)
    if len(packets) < 4:
        raise ValueError("Too few packets in Ogg stream")

    # ID header
    id_pkt = packets[0]
    id_r = BitReader(id_pkt, 7 * 8)
    id_r.read(32) # version
    channels = id_r.read(8)
    sample_rate = id_r.read(32)
    id_r.read(32) # max
    bitrate_nominal = id_r.read(32)
    id_r.read(32) # min
    bs0 = id_r.read(4)
    bs1 = id_r.read(4)

    # Strip setup
    setup_bytes, mode_blockflag, mode_bits = strip_setup(packets[2], channels, pcb_lib)

    # Total sample count from granules
    sample_count = max(g for g in granules if g >= 0)

    short_bs = 1 << bs0
    long_bs = 1 << bs1
    setup_chunk = struct.pack('<H', len(setup_bytes)) + setup_bytes
    setup_chunk_len = len(setup_chunk)

    audio_blob = bytearray()
    seek_table = bytearray()
    max_packet = 0
    prev_bs = -1
    cum = 0
    last_sample = 0
    last_offset = 0

    seek_interval = 16384
    audio_packets = packets[3:]

    for p in audio_packets:
        payload = repack_audio_packet(p, mode_blockflag, mode_bits)
        mode = (p[0] >> 1) & ((1 << mode_bits) - 1) if mode_bits > 0 else 0
        cur_bs = long_bs if mode_blockflag[mode] else short_bs
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

    avg_bytes = bitrate_nominal // 8 if bitrate_nominal > 0 else 0
    scale = float(channels) * float(long_bs) / 1024.0
    decode_alloc = int(17692 * scale + 0.5)
    x64_alloc = int(18116 * scale + 0.5)

    subtype = 0x4101 if channels == 1 else 0
    # Use standard Wwise aoTuV 6.03 codebook UID
    uid = 0x20CEF588

    # fmt chunk (66 / 0x42 bytes)
    fmtc = struct.pack('<HHIIHH' 'H' 'H' 'I' 'I' 'I' 'I' 'H' 'H' 'I' 'I' 'H' 'H' 'I' 'I' 'I' 'BB',
        0xFFFF, channels, sample_rate, avg_bytes, 0, 0,
        0x30,               # extra size (48 bytes)
        0,                  # ext_unk
        subtype,            # subtype
        sample_count,       # dwTotalPCMFrames
        setup_chunk_len,    # dwLoopStartPacketOffset
        data_size - seek_size, # dwLoopEndPacketOffset
        0,                  # uLoopBeginExtra
        last_granule_extra, # uLoopEndExtra
        seek_size,          # dwSeekTableSize
        audio_offset,       # dwVorbisDataOffset
        max_packet,         # uMaxPacketSize
        last_granule_extra, # uLastGranuleExtra
        decode_alloc,       # dwDecodeAllocSize
        x64_alloc,          # dwDecodeX64AllocSize
        uid,                # uHashCodebook
        bs0, bs1            # block sizes
    )

    out = bytearray()
    out.extend(b'RIFF')
    # RIFF size placeholder
    riff_body = bytearray()
    riff_body.extend(b'WAVE')
    riff_body.extend(b'fmt ')
    riff_body.extend(struct.pack('<I', len(fmtc)))
    riff_body.extend(fmtc)
    riff_body.extend(b'data')
    riff_body.extend(struct.pack('<I', len(data_payload)))
    riff_body.extend(data_payload)
    if len(data_payload) % 2 != 0:
        riff_body.append(0)

    out.extend(struct.pack('<I', len(riff_body)))
    out.extend(riff_body)
    return bytes(out)

if __name__ == '__main__':
    pcb_lib = load_codebook_library('/tmp/wav2wem_repo/assets/packed_codebooks_aoTuV_603.bin')
    print(f"Loaded {len(pcb_lib)} codebooks.")
    with open('/tmp/aotuv_test.ogg', 'rb') as f:
        ogg_bytes = f.read()
    wem = build_wem(ogg_bytes, pcb_lib)
    with open('/tmp/converted_aotuv.wem', 'wb') as f:
        f.write(wem)
    print(f"Successfully converted /tmp/aotuv_test.ogg -> /tmp/converted_aotuv.wem ({len(wem)} bytes)")