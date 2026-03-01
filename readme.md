# YouTube Download

Download YouTube videos or full playlists with automatic format selection (best video + best audio).

## Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation

```bash
pip install yt-dlp
```

## Usage

```bash
# Download default playlist (uses built-in test URL)
python main.py

# Download a specific URL (playlist or single video)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
python main.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
python main.py "https://youtu.be/VIDEO_ID?list=PLAYLIST_ID"
```

### Behavior

- **Playlist URL** → Downloads all videos in the playlist
- **Single video URL** → Downloads that one video only

## Output

All downloads are saved to the `downloads/` directory:

| Input           | Output path                                      |
|-----------------|--------------------------------------------------|
| Single video    | `downloads/<title>.<ext>`                        |
| Playlist        | `downloads/<playlist_title>/001 - <title>.<ext>` |

Format: best video + best audio merged (or best combined format).

## Troubleshooting

If downloads fail:

1. **Update yt-dlp** — YouTube changes often; keep the tool current:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Use cookies for age-restricted or private content** — Export `cookies.txt` from your browser (e.g. via a cookies extension) and place it in the project folder. yt-dlp will use it if present when you add `--cookies cookies.txt` (requires updating the script) or use yt-dlp directly with cookie support.

3. **Check the URL** — Ensure the video or playlist is public and accessible.

## License

MIT
