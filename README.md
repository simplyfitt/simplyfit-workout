# SimplyFit Workout MVP (v1)
Zero-dependency Node server + static pages. Data lives in `data/db.json` (seeded from `data/seed.json` on first run).

## Run
    npm start          # http://localhost:3000  (PORT=xxxx to change)
- Home: `/`  · Coach: `/coach`  · Demo client: `/c/demo-7f3k`
- For phones on the same network, open `http://<your-LAN-IP>:3000/c/<token>`.
- Reset data: delete `data/db.json` and restart.

## v1 does
- Mobile-first client view: Day 1–5 tabs, exercises with sets × reps, notes, form-video link; tick sets done (localStorage, per device).
- Coach view: pick/add client, edit week as JSON, save, copy shareable link (`/c/<token>`).
- Brand palette: #1B4332, #52796F, #F5F0E8, #C9A84C.

## v1 does NOT include
Weight/rep logger, journal, WhatsApp delivery, real auth (share link token is the only access control — coach page is open), multi-week history, form-based plan builder, hosting/HTTPS.
