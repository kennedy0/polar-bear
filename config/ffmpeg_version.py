import shutil

from pyffmpeg import FFmpeg


FFMPEG_SYSTEM = "system"
FFMPEG_BUNDLED = "bundled"


def get_system_ffmpeg() -> str or None:
    return shutil.which("ffmpeg")


def get_ffmpeg_binary(version: str) -> str:
    if version == FFMPEG_SYSTEM:
        ffmpeg_binary = get_system_ffmpeg()
        if ffmpeg_binary is not None:
            return ffmpeg_binary

    return FFmpeg().get_ffmpeg_bin()
