#!/usr/bin/env python3
"""Minimal test script to download YouTube videos or full playlists."""

from typing import Optional

import yt_dlp
from pathlib import Path
from alive_progress import alive_bar

DOWNLOAD_DIR = Path("downloads")

# Characters invalid in Windows paths (and common on Unix)
_INVALID_PATH_CHARS = '/\\:*?"<>|'


def _sanitize_path_component(name: str) -> str:
    """Make a string safe for use as a directory name."""
    for c in _INVALID_PATH_CHARS:
        name = name.replace(c, "_")
    return name.strip() or "Playlist"


def _get_playlist_info(ydl, url: str):
    """Extract playlist info and return (is_playlist, entry_count, playlist_title)."""
    try:
        info = ydl.extract_info(url, download=False)
        if info is None:
            return False, 0, None
        if "entries" not in info:
            return False, 1, None
        entries = [e for e in info.get("entries", []) or [] if e is not None]
        return True, len(entries), info.get("title")
    except Exception:
        return False, 0, None


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
        is_playlist, total, playlist_title = _get_playlist_info(ydl, url)

    playlist_dir = None
    if is_playlist:
        safe_title = _sanitize_path_component(playlist_title or "Playlist")
        playlist_dir = DOWNLOAD_DIR / safe_title
        playlist_dir.mkdir(parents=True, exist_ok=True)
        outtmpl = str(playlist_dir / "%(playlist_index)03d - %(title)s.%(ext)s")
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
            out_dir = (playlist_dir or DOWNLOAD_DIR).resolve()
            print(f"Starting download ({desc})...")
            print(f"Output directory: {out_dir}")

            if is_playlist and total > 0:
                with alive_bar(total, title="Videos", enrich_print=False) as bar:
                    def progress_hook(d):
                        if d.get("status") == "finished":
                            bar.text = d.get("info_dict", {}).get("title", "")
                            bar()

                    ydl.add_progress_hook(progress_hook)
                    ydl.download([url])
            else:
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