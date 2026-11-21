# -*- coding: utf-8 -*-
import zipfile
from pathlib import Path

BASE = Path(r"C:\Users\aless\AppData\Local\Temp\opencode\apkbuild")
for name, out in [("jre17.zip", "jre"), ("build-tools.zip", "bt"), ("platform-34.zip", "plat")]:
    src = BASE / name
    with zipfile.ZipFile(src) as z:
        names = z.namelist()
        print(name, "OK, entries:", len(names), "first:", names[:3])
        z.extractall(BASE / out)
    print("  extracted ->", BASE / out)

print("\n--- android.jar ---")
found = list((BASE / "plat").rglob("android.jar"))
print(found)

print("\n--- build-tools binaries ---")
bt = BASE / "bt"
for p in sorted(bt.rglob("*")):
    if p.is_file() and (p.name in ("aapt2.exe", "zipalign.exe", "d8.jar", "apksigner.jar", "apksigner.bat", "d8.bat")):
        print(p.relative_to(bt), p.stat().st_size)

print("\n--- java.exe ---")
print(list((BASE / "jre").rglob("java.exe")))
