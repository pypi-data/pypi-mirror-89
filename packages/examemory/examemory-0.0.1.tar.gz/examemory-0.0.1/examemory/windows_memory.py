import ctypes
import ctypes.wintypes

from .memory import *

PROCESS_ALL_ACCESS = 0x1F0FFF

TH32CS_SNAPPROCESS = 0x2
TH32CS_SNAPMODULE = 0x8
TH32CS_SNAPMODULE32 = 0x10

MEM_RESERVE = 0x2000
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x4


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_ulong),
                ("cntUsage", ctypes.c_ulong),
                ("th32ProcessID", ctypes.c_ulong),
                ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                ("th32ModuleID", ctypes.c_ulong),
                ("cntThreads", ctypes.c_ulong),
                ("th32ParentProcessID", ctypes.c_ulong),
                ("pcPriClassBase", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("szExeFile", ctypes.c_char * ctypes.wintypes.MAX_PATH)]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_ulong),
                ("th32ModuleID", ctypes.c_ulong),
                ("th32ProcessID", ctypes.c_ulong),
                ("GlblcntUsage", ctypes.c_ulong),
                ("ProccntUsage", ctypes.c_ulong),
                ("modBaseAddr", ctypes.c_ulonglong),
                ("modBaseSize", ctypes.c_ulong),
                ("hModule", ctypes.wintypes.HANDLE),
                ("szModule", ctypes.c_char * 256),
                ("szExePath", ctypes.c_char * ctypes.wintypes.MAX_PATH)]


CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
CloseHandle = ctypes.windll.kernel32.CloseHandle
OpenProcess = ctypes.windll.kernel32.OpenProcess

Process32First = ctypes.windll.kernel32.Process32First
Process32Next = ctypes.windll.kernel32.Process32Next

Module32First = ctypes.windll.kernel32.Module32First
Module32Next = ctypes.windll.kernel32.Module32Next

ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory

GetProcAddress = ctypes.windll.kernel32.GetProcAddress
GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA

VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject


class WindowsMemory(Memory):

    def __init__(self, process_name):
        self.process_id = self.get_process_id(process_name)
        self.process_handle = OpenProcess(PROCESS_ALL_ACCESS, 0,
                                          self.process_id)

    def get_process_id(self, process_name):
        handle_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if handle_snapshot:
            process_info = PROCESSENTRY32()
            process_info.dwSize = ctypes.sizeof(PROCESSENTRY32)
            Process32First(handle_snapshot, ctypes.byref(process_info))
            if process_info.szExeFile.decode() == process_name:
                return process_info.th32ProcessID
            while Process32Next(handle_snapshot, ctypes.byref(process_info)):
                if process_info.szExeFile.decode() == process_name:
                    return process_info.th32ProcessID
        CloseHandle(handle_snapshot)
        return -1

    def get_module_base(self, module_name):
        handle_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE |
                                                   TH32CS_SNAPMODULE32,
                                                   self.process_id)
        if handle_snapshot:
            module_info = MODULEENTRY32()
            module_info.dwSize = ctypes.sizeof(MODULEENTRY32)
            Module32First(handle_snapshot, ctypes.byref(module_info))
            if module_info.szModule.decode() == module_name:
                return module_info.modBaseAddr
            while Module32Next(handle_snapshot, ctypes.byref(module_info)):
                if module_info.szModule.decode() == module_name:
                    return module_info.modBaseAddr
        CloseHandle(handle_snapshot)
        return -1

    def get_module_size(self, module_name):
        handle_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE |
                                                   TH32CS_SNAPMODULE32,
                                                   self.process_id)
        if handle_snapshot:
            module_info = MODULEENTRY32()
            module_info.dwSize = ctypes.sizeof(MODULEENTRY32)
            Module32First(handle_snapshot, ctypes.byref(module_info))
            if module_info.szModule.decode() == module_name:
                return module_info.modBaseSize
            while Module32Next(handle_snapshot, ctypes.byref(module_info)):
                if module_info.szModule.decode() == module_name:
                    return module_info.modBaseSize
        CloseHandle(handle_snapshot)
        return -1

    # ---Read---

    def _read_bytes(self, address, size):
        buffer = ctypes.create_string_buffer(size)
        ReadProcessMemory(self.process_handle, ctypes.c_void_p(address),
                          ctypes.byref(buffer), size, 0)
        return buffer.raw

    # ---Write---

    def _write_bytes(self, address, data):
        WriteProcessMemory(self.process_handle, ctypes.c_char_p(address),
                           data, len(data), 0)

    # ---DLL-Injection---

    def inject_dll(self, dll_path):
        path_length = len(dll_path)+1
        load_library_address = GetProcAddress(GetModuleHandleA(
                               'kernel32.dll'.encode('ascii')),
                               'LoadLibraryA'.encode())
        parameter_address = VirtualAllocEx(self.process_handle, 0,
                                           path_length,
                                           MEM_RESERVE | MEM_COMMIT,
                                           PAGE_READWRITE)
        self._write_bytes(parameter_address, dll_path.encode('ascii'))
        thread_handle = CreateRemoteThread(self.process_handle, 0, 0,
                                           load_library_address,
                                           parameter_address, 0, 0)
        WaitForSingleObject(thread_handle, -1)
        CloseHandle(thread_handle)

    # ---Shellcode-Injection---

    def inject_shellcode(self, shellcode):
        shellcode_length = len(shellcode)
        shellcode_address = VirtualAllocEx(self.process_handle, 0,
                                           shellcode_length,
                                           MEM_RESERVE | MEM_COMMIT,
                                           PAGE_READWRITE)
        self._write_bytes(shellcode_address, shellcode)
        CreateRemoteThread(self.process_handle, 0, 0, shellcode_address,
                           0, 0, 0)
