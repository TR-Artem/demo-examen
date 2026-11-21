# -*- coding: utf-8 -*-
"""
Собирает офлайн-APK с мобильной версией тренажёра.

Требует: распакованный инструментарий в
  C:\\Users\\aless\\AppData\\Local\\Temp\\opencode\\apkbuild
(jre, bt, plat, ecj.jar, sql-wasm.js, sql-wasm.wasm) — см. apk_download.py / apk_unpack.py.

Используются только скачанные портативные утилиты, системная Java/Android SDK не нужны.
"""
from __future__ import annotations

import base64
import datetime
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Users\aless\demoexam-09-02-07")
MOBILE = ROOT / "mobile"
ASSETS = MOBILE / "assets"
TOOLS = Path(r"C:\Users\aless\AppData\Local\Temp\opencode\apkbuild")
WORK = TOOLS / "work"
APK_ASSETS = WORK / "apk_assets"
OUT_APK = ROOT / "DemoExam-09-02-07.apk"
STANDALONE = ROOT / "DemoExam-mobile.html"

JRE = next((TOOLS / "jre").glob("*/bin/java.exe"))
JAVA = str(JRE)
BT = TOOLS / "bt" / "android-14"
ANDROID_JAR = next((TOOLS / "plat").glob("*/android.jar"))
AAPT2 = str(BT / "aapt2.exe")
ZIPALIGN = str(BT / "zipalign.exe")
ECJ = str(TOOLS / "ecj.jar")
D8_JAR = str(BT / "lib" / "d8.jar")
APKSIGNER = str(BT / "lib" / "apksigner.jar")


def run(cmd, **kw):
    print("  >", " ".join(str(c) for c in cmd[:6]), "..." if len(cmd) > 6 else "", flush=True)
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        print("STDOUT:\n", r.stdout[-3000:], flush=True)
        print("STDERR:\n", r.stderr[-3000:], flush=True)
        raise RuntimeError(f"Команда завершилась с кодом {r.returncode}")
    return r


# ---------------------------------------------------------------- 1. данные
def gen_data():
    print("[1/9] Готовлю данные из trainer.py ...", flush=True)
    spec = importlib.util.spec_from_file_location("trainer_mod", ROOT / "trainer.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["trainer_mod"] = m
    spec.loader.exec_module(m)
    data = {
        "plan": m.PLAN,
        "lessons": [list(l) for l in m.LESSONS],
        "quiz": m.QUIZ,
        "sql": m.SQL_TASKS,
        "criteria": [[title, [[txt, w] for txt, w in items]] for title, items in m.CRITERIA],
        "snippets": [[t, c] for t, c in m.SNIPPETS],
        "schema": m.SCHEMA_SQL,
        "max_score": m.MAX_SCORE,
    }
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (ASSETS / "data.js").write_text("window.DEMO_DATA = " + js + ";\n", encoding="utf-8")
    print("      data.js:", len(js), "символов", flush=True)

    wasm = (TOOLS / "sql-wasm.wasm").read_bytes()
    b64 = base64.b64encode(wasm).decode("ascii")
    (ASSETS / "wasm_data.js").write_text(
        "window.SQL_WASM_B64 = \"" + b64 + "\";\n", encoding="ascii")
    print("      wasm:", len(wasm), "байт → base64", len(b64), "символов", flush=True)
    shutil.copy2(TOOLS / "sql-wasm.js", ASSETS / "sql-wasm.js")
    for f in ("index.html", "data.js", "wasm_data.js", "sql-wasm.js"):
        assert (ASSETS / f).exists(), f"Нет файла {f}"


def build_standalone():
    """Собирает ОДИН самодостаточный HTML: данные + sql.js + wasm внутри.

    Это важно для Android 11+: WebView может запрещать загрузку соседних
    file://-скриптов, а один файл грузится всегда. Он же отдаётся пользователю
    как «просто открыть в браузере телефона».
    """
    print("[1b/9] Собираю самодостаточный HTML (без внешних файлов) ...", flush=True)
    html = (ASSETS / "index.html").read_text(encoding="utf-8")
    parts = {
        "data.js": (ASSETS / "data.js").read_text(encoding="utf-8"),
        "wasm_data.js": (ASSETS / "wasm_data.js").read_text(encoding="utf-8"),
        "sql-wasm.js": (ASSETS / "sql-wasm.js").read_text(encoding="utf-8"),
    }
    assert "</script" not in parts["sql-wasm.js"].lower(), "в sql-wasm.js есть </script"
    for name, code in parts.items():
        # Экранируем последовательность, которая преждевременно закроет <script>
        code = code.replace("</script", "<\\/script")
        tag = f'<script src="{name}"></script>'
        assert tag in html, f"Не найден тег {tag}"
        html = html.replace(tag, "<script>\n" + code + "\n</script>")
    assert "<script src=" not in html
    STANDALONE.write_text(html, encoding="utf-8")
    APK_ASSETS.mkdir(parents=True, exist_ok=True)
    (APK_ASSETS / "index.html").write_text(html, encoding="utf-8")
    print("      standalone:", len(html), "символов, внешних скриптов: 0", flush=True)


# ---------------------------------------------------------------- 2. иконка
def write_png(path, w, h, rgba):
    raw = b"".join(b"\x00" + bytes(rgba[y * w * 4:(y + 1) * w * 4]) for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib_crc(t + d))
    def zlib_crc(b):
        import zlib
        return zlib.crc32(b) & 0xffffffff
    import zlib
    hdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", hdr)
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def gen_icon():
    print("[2/9] Рисую иконку ...", flush=True)
    W = H = 192
    px = bytearray(W * H * 4)
    def put(x, y, r, g, b, a=255):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 4
            px[i:i + 4] = bytes((r, g, b, a))
    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1):
            for x in range(x0, x1):
                put(x, y, *c)
    green, white = (46, 139, 87, 255), (255, 255, 255, 255)
    rad = 38
    for y in range(H):
        for x in range(W):
            cx = min(x, W - 1 - x); cy = min(y, H - 1 - y)
            inside = True
            if cx < rad and cy < rad:
                inside = (cx - rad) ** 2 + (cy - rad) ** 2 <= rad ** 2
            if inside:
                put(x, y, *green)
    # Скобки { } и слэш — значок «код»
    rect(52, 54, 59, 138, white)
    rect(52, 54, 76, 61, white)
    rect(52, 131, 76, 138, white)
    rect(133, 54, 140, 138, white)
    rect(116, 54, 140, 61, white)
    rect(116, 131, 140, 138, white)
    for k in range(40):
        x = 88 + k // 3
        y = 122 - k
        for dx in range(5):
            put(x + dx, y, *white)
    res = WORK / "res" / "mipmap-xxxhdpi"
    res.mkdir(parents=True, exist_ok=True)
    write_png(res / "ic_launcher.png", W, H, px)


# ---------------------------------------------------------------- 3. Java
JAVA_SRC = r"""package ru.demoexam.trainer;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient());
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
"""

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="ru.demoexam.trainer"
    android:versionCode="1"
    android:versionName="1.0">
    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="34" />
    <application
        android:label="ДЭ 09.02.07 — Тренажёр"
        android:icon="@mipmap/ic_launcher"
        android:theme="@android:style/Theme.Material.Light.NoActionBar"
        android:hardwareAccelerated="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""


def compile_java():
    print("[3/9] Компилирую MainActivity.java (ecj) ...", flush=True)
    src = WORK / "src" / "ru" / "demoexam" / "trainer"
    src.mkdir(parents=True, exist_ok=True)
    (src / "MainActivity.java").write_text(JAVA_SRC, encoding="utf-8")
    (WORK / "AndroidManifest.xml").write_text(MANIFEST, encoding="utf-8")
    classes = WORK / "classes"
    shutil.rmtree(classes, ignore_errors=True)
    classes.mkdir(parents=True)
    run([JAVA, "-jar", ECJ, "-source", "1.8", "-target", "1.8", "-nowarn",
         "-bootclasspath", ANDROID_JAR, "-classpath", ANDROID_JAR,
         "-d", classes, src / "MainActivity.java"])
    print("      class-файлы готовы", flush=True)

    print("[4/9] Собираю classes.dex (d8) ...", flush=True)
    dexdir = WORK / "dex"
    shutil.rmtree(dexdir, ignore_errors=True)
    dexdir.mkdir(parents=True)
    run([JAVA, "-cp", D8_JAR, "com.android.tools.r8.D8",
         "--lib", ANDROID_JAR, "--min-api", "21", "--output", dexdir,
         classes / "ru" / "demoexam" / "trainer" / "MainActivity.class"])
    assert (dexdir / "classes.dex").exists(), "d8 не создал classes.dex"


# ---------------------------------------------------------------- 4. aapt2
def link_apk():
    print("[5/9] Собираю ресурсы и манифест (aapt2) ...", flush=True)
    flats = WORK / "flats"
    shutil.rmtree(flats, ignore_errors=True)
    flats.mkdir(parents=True)
    run([AAPT2, "compile", WORK / "res" / "mipmap-xxxhdpi" / "ic_launcher.png", "-o", flats])
    flat_files = sorted(flats.rglob("*.flat"))
    assert flat_files, "aapt2 compile не создал .flat"
    base = WORK / "base.apk"
    if base.exists():
        base.unlink()
    cmd = [AAPT2, "link", "-o", base, "-I", ANDROID_JAR,
           "--manifest", WORK / "AndroidManifest.xml",
           "--min-sdk-version", "21", "--target-sdk-version", "34",
           "--auto-add-overlay"]
    for f in flat_files:
        cmd += ["-R", f]
    run(cmd)
    return base


# ---------------------------------------------------------------- 5. сборка ZIP
def build_apk(base):
    print("[6/9] Добавляю classes.dex и assets ...", flush=True)
    out = WORK / "unsigned.apk"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(base, "r") as zin, zipfile.ZipFile(out, "w") as zout:
        for info in zin.infolist():
            zout.writestr(info, zin.read(info.filename))
        zout.write(WORK / "dex" / "classes.dex", "classes.dex", zipfile.ZIP_DEFLATED)
        for f in sorted(APK_ASSETS.iterdir()):
            if f.is_file():
                zout.write(f, "assets/" + f.name, zipfile.ZIP_DEFLATED)
    print("      APK:", out.stat().st_size, "байт", flush=True)
    return out


def zipalign(unsigned):
    print("[7/9] Выравниваю (zipalign) ...", flush=True)
    aligned = WORK / "aligned.apk"
    if aligned.exists():
        aligned.unlink()
    run([ZIPALIGN, "-f", "-p", "4", unsigned, aligned])
    return aligned


# ---------------------------------------------------------------- 6. подпись
def make_key_cert():
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    print("[8/9] Генерирую ключ и подписываю APK (apksigner) ...", flush=True)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "DemoExam Trainer"),
                      x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Self-study")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=365 * 30))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(key, hashes.SHA256()))
    (WORK / "key.pk8").write_bytes(key.private_bytes(
        serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()))
    (WORK / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    return WORK / "key.pk8", WORK / "cert.pem"


def sign(aligned, key, cert):
    if OUT_APK.exists():
        OUT_APK.unlink()
    run([JAVA, "-jar", APKSIGNER, "sign",
         "--key", key, "--cert", cert,
         "--v1-signing-enabled", "true",
         "--v2-signing-enabled", "true",
         "--v3-signing-enabled", "false",
         "--v4-signing-enabled", "false",
         "--min-sdk-version", "21",
         "--out", OUT_APK, aligned])
    print("[9/9] Проверяю подпись ...", flush=True)
    r = run([JAVA, "-jar", APKSIGNER, "verify", "--verbose", "--print-certs", OUT_APK])
    print(r.stdout[-1800:], flush=True)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    gen_data()
    build_standalone()
    gen_icon()
    compile_java()
    base = link_apk()
    unsigned = build_apk(base)
    aligned = zipalign(unsigned)
    key, cert = make_key_cert()
    sign(aligned, key, cert)
    size = OUT_APK.stat().st_size
    print("\nГОТОВО:", OUT_APK, f"({size/1024/1024:.2f} МБ)", flush=True)
    # Копия исходников мобильной версии рядом, чтобы можно было открыть и в браузере
    print("Мобильная версия также лежит в:", MOBILE, flush=True)


if __name__ == "__main__":
    main()
