# Web Deployment - Rogue Tower Defense

## Status: ✅ DEPLOYED

The game is now available as a web application!

## Access URLs

**Local Network:**
- http://192.168.0.89:8080
- http://localhost:8080 (from this machine)

**Public Access:**
To make this accessible from the internet, you'll need to:
1. Configure port forwarding on your router (port 8080 → 192.168.0.89:8080)
2. OR use a reverse proxy/tunnel service like ngrok, Cloudflare Tunnel, or similar

## Server Management

### Check Status
```bash
ss -tuln | grep 8080
# or
ps aux | grep "http.server 8080"
```

### Stop Server
```bash
pkill -f "http.server 8080"
```

### Start Server
```bash
cd ~/projects/rogue-tower-defense/build/web
python3 -m http.server 8080 > /tmp/game-server.log 2>&1 &
```

### View Logs
```bash
tail -f /tmp/game-server.log
```

## Rebuild Web Version

If you make changes to the game code:

```bash
cd ~/projects/rogue-tower-defense
python3 -m pygbag --build main_web.py
```

Then restart the server.

## Technical Details

- **Build Tool:** pygbag (Pygame → WebAssembly)
- **Web Server:** Python http.server (port 8080)
- **Build Output:** ~/projects/rogue-tower-defense/build/web/
- **Entry Point:** main_web.py (async version for web)

## Architecture

```
rogue-tower-defense/
├── main.py              # Desktop version
├── main_web.py          # Web version (async)
├── build/
│   └── web/            # Built web assets
│       ├── index.html
│       ├── *.wasm
│       └── *.data
└── serve_web.sh        # Server startup script
```

## Controls (Web)

Same as desktop version:
- **1/2/3/4:** Select tower type
- **Left Click:** Place tower
- **Space:** Start wave
- **R:** Restart (when game over)
- **U:** Upgrades menu (when game over)
- **ESC:** Cancel tower selection / Close upgrades

## Performance Notes

Web version runs via WebAssembly - performance is slightly lower than native desktop but still smooth for this type of game.

## Future: Public Deployment Options

For true remote access without port forwarding:

1. **Cloudflare Tunnel** (free)
   - cloudflared tunnel for secure public URL
   
2. **ngrok** (free tier available)
   - `ngrok http 8080`
   - Provides temporary public URL
   
3. **Deploy to hosting**
   - GitHub Pages (static hosting)
   - Netlify / Vercel (free tiers)
   - Any static site host

4. **VPS with domain**
   - nginx reverse proxy
   - SSL certificate (Let's Encrypt)
   - Custom domain

---

**Current Status:** Running on local network at http://192.168.0.89:8080
