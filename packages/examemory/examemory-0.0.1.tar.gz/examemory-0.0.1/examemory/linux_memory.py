import ctypes
import subprocess

from .memory import *


class IOVEC(ctypes.Structure):
        _fields_ = [("iov_base", ctypes.c_void_p),
                    ("iov_len", ctypes.c_size_t)]


libc = ctypes.CDLL("libc.so.6")
process_vm_readv = libc.process_vm_readv
process_vm_writev = libc.process_vm_writev


class LinuxMemory(Memory):

    def __init__(self, process_name):
        self.process_id = self.get_process_id(process_name)

    def get_process_id(self, process_name):
        return int(subprocess.check_output(["pidof", "-s", process_name]))

    def get_module_base(self, module_name):
        content = open('/proc/'+str(self.process_id)+'/maps').read()
        for entry in content.split('\n')[:-1]:
            entry_data = entry.split(' ')
            if entry_data[-1].split('/')[-1] == module_name:
                return int(entry_data[0].split('-')[0], 16)

    def get_module_size(self, module_name):
        content = open('/proc/'+str(self.process_id)+'/maps').read()
        for entry in content.split('\n')[:-1]:
            entry_data = entry.split(' ')
            if entry_data[-1].split('/')[-1] == module_name:
                return int(entry_data[0].split('-')[1], 16)

    def _read_bytes(self, address, size):
        buffer = ctypes.create_string_buffer(size)
        local = IOVEC(ctypes.addressof(buffer), size)
        remote = IOVEC(address, size)
        process_vm_readv(self.process_id, ctypes.byref(local), 1,
                         ctypes.byref(remote), 1, 0)
        return buffer.raw

    def _write_bytes(self, address, data):
        size = len(data)
        buffer = ctypes.create_string_buffer(data)
        local = IOVEC(ctypes.addressof(buffer), size)
        remote = IOVEC(address, size)
        process_vm_writev(self.process_id, ctypes.byref(local), 1,
                          ctypes.byref(remote), 1, 0)
