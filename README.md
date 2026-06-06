# Orbit

Personal hub for tools and digests.

**Live:** https://orben12-byte.github.io/Hub/

## Tools
- [Moon Phase](https://orben12-byte.github.io/moon-phase/)
- [Calculator](https://orben12-byte.github.io/calculator/)
- Free Tools Dashboard (coming soon)

## Digests
Stored under `digests/` with a `manifest.json` index per folder.

### Adding a new digest
1. Save the HTML file to the correct folder: `digests/weekly/`, `digests/monthly/`, or `digests/alt-hunter/`
2. Prepend an entry to that folder's `manifest.json`:
```json
[
  { "title": "Weekly Digest — 2026-06-06", "date": "6 ביוני 2026", "file": "2026-06-06.html" },
  ...
]
```
3. `git add . && git commit -m "digest: weekly 2026-06-06" && git push`
