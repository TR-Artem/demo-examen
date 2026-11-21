# -*- coding: utf-8 -*-
"""Скачивает портативный инструментарий для сборки APK."""
import sys
from pathlib import Path
import requests

BASE = Path(r"C:\Users\aless\AppData\Local\Temp\opencode\apkbuild")
BASE.mkdir(parents=True, exist_ok=True)

FILES = [
    ("jre17.zip", "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jre/hotspot/normal/eclipse"),
    ("ecj.jar", "https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.33.0/ecj-3.33.0.jar"),
    ("build-tools.zip", "https://dl.google.com/android/repository/build-tools_r34-windows.zip"),
    ("platform-34.zip", "https://dl.google.com/android/repository/platform-34-ext12_r01.zip"),
    ("sql-wasm.js", "https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/sql-wasm.js"),
    ("sql-wasm.wasm", "https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/sql-wasm.wasm"),
]

for name, url in FILES:
    dest = BASE / name
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"SKIP {name} ({dest.stat().st_size} bytes)", flush=True)
        continue
    print(f"GET  {name} ...", flush=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length") or 0)
        done = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
        print(f"     ok: {done} bytes (expected {total})", flush=True)
    if total and done != total:
        print("     WARNING: размер не совпал", flush=True)

print("DOWNLOAD DONE", flush=True)
for p in sorted(BASE.iterdir()):
    print(" ", p.name, p.stat().st_size, flush=True)
