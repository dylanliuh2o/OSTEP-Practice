import json
import os
import shutil
import subprocess

INSTALL_DIR   = "install"
LAUNCH_FILE   = ".vscode/launch.json"
DEBUGGER_MODE = "gdb"  # 你可以换成 lldb

def clean_install_dir():
    if os.path.exists(INSTALL_DIR):
        print(f"Cleaning install directory: {INSTALL_DIR}")
        shutil.rmtree(INSTALL_DIR)

def run_cmake_install():
    print("Running: cmake --install build")
    subprocess.run(["cmake", "--install", "build" ], check=True)

def find_executables(root):
    result = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            path = os.path.join(dirpath, f)
            if os.access(path, os.X_OK) and not os.path.isdir(path):
                result.append(path)
    return result

def generate_launch_config(executables):
    configs = []
    for exe_path in executables:
        # 提取章节和程序名
        rel_path = os.path.relpath(exe_path, INSTALL_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) >= 3:
            chapter, prog, exe_name = parts[0], parts[1], parts[-1]
            name = f"Debug {chapter}/{prog} - {exe_name}"
        else:
            name = f"Debug {rel_path}"
        config = {
            "name": name,
            "type": "cppdbg",
            "request": "launch",
            "program": f"${{workspaceFolder}}/{exe_path}",
            "args": [],
            "stopAtEntry": True,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": False,
            "MIMode": DEBUGGER_MODE,
            "setupCommands": [
                {
                    "description": "Enable pretty-printing",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": True
                }
            ]
        }
        configs.append(config)
    return {
        "version": "0.2.0",
        "configurations": configs
    }

def main():
    clean_install_dir()
    run_cmake_install()
    executables = find_executables(INSTALL_DIR)
    launch_data = generate_launch_config(executables)

    os.makedirs(os.path.dirname(LAUNCH_FILE), exist_ok=True)
    with open(LAUNCH_FILE, "w") as f:
        json.dump(launch_data, f, indent=4)
    print(f"Generated {LAUNCH_FILE} with {len(executables)} configurations.")

if __name__ == "__main__":
    main()