import platform

platform_type = platform.system()
if platform_type == 'Windows':
    from .windows_memory import WindowsMemory as ExaMemory
elif platform_type == 'Linux':
    from .linux_memory import LinuxMemory as ExaMemory
