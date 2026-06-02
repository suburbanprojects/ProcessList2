import psutil


def get_all_processes():
    """Return list of all running processes with details."""
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes


def terminate_by_pid(pid):
    """Terminate a process by PID. Returns (success, message)."""
    try:
        psutil.Process(pid).terminate()
        return True, f'Process {pid} terminated.'
    except ValueError:
        return False, 'PID must be an integer.'
    except psutil.NoSuchProcess:
        return False, f'Process {pid} does not exist.'
    except psutil.AccessDenied:
        return False, f'Permission denied terminating PID {pid}.'


def terminate_by_name(name):
    """Terminate a process by name. Returns (success, message)."""
    target_name = name.lower()
    for process in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = (process.info.get('name') or '').lower()
            if target_name == proc_name or target_name in proc_name:
                process.terminate()
                return True, f'Process {process.pid} ("{process.name()}") terminated.'
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, f'No process matching "{name}" found.'


def terminate_by_target(target_text):
    """Terminate a process by either PID or name. Returns (success, message)."""
    target_text = target_text.strip()
    if not target_text:
        return False, 'Enter a PID or process name first.'

    # Try as PID first
    try:
        pid = int(target_text)
        return terminate_by_pid(pid)
    except ValueError:
        pass

    # Try as process name
    return terminate_by_name(target_text)
