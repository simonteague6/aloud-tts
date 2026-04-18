from setuptools import setup

APP = ["src/tts_app/menubar/app.py"]
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleIdentifier": "com.simonteague.aloud-tts",
        "CFBundleName": "TTS",
        "CFBundleShortVersionString": "0.1.0",
        "LSUIElement": True,
        "NSAppleEventsUsageDescription": "TTS needs Accessibility to read selected text.",
        "NSMicrophoneUsageDescription": "Not used, but required by pynput manifest scan.",
    },
    "packages": ["tts_app", "mlx_audio", "misaki", "rumps", "pynput"],
    "includes": ["pkg_resources"],
    # "iconfile": "assets/icon.icns",  # add when icon exists
}

setup(app=APP, options={"py2app": OPTIONS}, setup_requires=["py2app"])
