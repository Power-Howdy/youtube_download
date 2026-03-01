#!/usr/bin/env python3
"""Minimal test script to download YouTube videos or full playlists."""

from typing import Optional

import yt_dlp
from pathlib import Path

DOWNLOAD_DIR = Path("downloads")


def _is_playlist(ydl, url: str) -> bool:
    """Check if the URL points to a playlist or multiple videos."""
    try:
        info = ydl.extract_info(url, download=False, process=False)
        return info is not None and "entries" in info
    except Exception:
        return False


def download(url: Optional[str] = None) -> bool:
    """
    Download all videos in a playlist, or a single video if not a playlist.
    Saves to downloads/ with correct names.
    """
    if url is None:
        url = "https://youtu.be/_G6jWN0PzDI?list=PL7VdqFXO0LzcO3VwfFCtZTFWC7kFUONcC"

    DOWNLOAD_DIR.mkdir(exist_ok=True)

    base_opts = {
        "format": "bestvideo+bestaudio/best",
        "ignoreerrors": True,
    }

    with yt_dlp.YoutubeDL(dict(base_opts, quiet=True)) as ydl:
        is_playlist = _is_playlist(ydl, url)

    if is_playlist:
        outtmpl = str(DOWNLOAD_DIR / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s")
        desc = "playlist"
    else:
        outtmpl = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
        desc = "single video"

    ydl_opts = {
        **base_opts,
        "outtmpl": outtmpl,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download ({desc})...")
            print(f"Output directory: {DOWNLOAD_DIR.resolve()}")
            ydl.download([url])
        print("SUCCESS")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else None
    download(url)