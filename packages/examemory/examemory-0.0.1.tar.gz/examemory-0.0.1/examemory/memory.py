import struct


class Memory:

    def __init__(self, process_name):
        raise NotImplementedError

    def get_process_id(self, process_name):
        raise NotImplementedError

    def get_module_base(self, module_name):
        raise NotImplementedError

    def get_module_size(self, module_name):
        raise NotImplementedError

    # ---Read---

    def read_ulong(self, address):
        return struct.unpack('L', self._read_bytes(address, 4))[0]

    def read_byte(self, address):
        return struct.unpack('b', self._read_bytes(address, 1))[0]

    def read_short(self, address):
        return struct.unpack('h', self._read_bytes(address, 2))[0]

    def read_int(self, address):
        return struct.unpack('i', self._read_bytes(address, 4))[0]

    def read_float(self, address):
        return struct.unpack('f', self._read_bytes(address, 4))[0]

    def read_double(self, address):
        return struct.unpack('d', self._read_bytes(address, 8))[0]

    def read_string(self, address, length):
        return self._read_bytes(address, length).decode()

    # ---Write---

    def write_byte(self, address, value):
        self._write_bytes(address, struct.pack('b', value))

    def write_short(self, address, value):
        self._write_bytes(address, struct.pack('h', value))

    def write_int(self, address, value):
        self._write_bytes(address, struct.pack('i', value))

    def write_float(self, address, value):
        self._write_bytes(address, struct.pack('f', value))

    def write_double(self, address, value):
        self._write_bytes(address, struct.pack('d', value))

    def write_string(self, address, value):
        self._write_bytes(address, value.encode())

    # ---SignatureScanning---

    def compare_data(self, module_data, current_offset, sig, mask):
        for x in range(len(sig)):
            if mask[x] and not sig[x] == module_data[current_offset+x]:
                return False
        return True

    def scan_signature(self, module_name, extra, offset, signature,
                       read=True, subtract=True):
        split_sig = signature.split(" ")
        signature_size = len(split_sig)

        sig = []
        mask = []

        for x in split_sig:
            sig.append(0 if x == '?' else int(x, 16))
            mask.append(0 if x == '?' else 1)

        module_base = self.get_module_base(module_name)
        max_scan_offset = self.get_module_size(module_name) - signature_size

        module_data = self._read_bytes(module_base,
                                       max_scan_offset + signature_size)

        for x in range(max_scan_offset):
            if self.compare_data(module_data, x, sig, mask):
                x += module_base + extra
                if read:
                    x = self.read_ulong(x)
                if subtract:
                    x -= module_base
                x += offset
                return x

        return -1
