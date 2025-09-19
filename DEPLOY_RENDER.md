Render deployment instructions

Overview
--------
This guide shows how to deploy the `USAFhelper` Discord bot to Render using the Dockerfile already included in the repository.

What I added
------------
- `render.yaml` — Render service definition configured to use the Dockerfile and auto-deploy from the `main` branch.
- `Dockerfile`, `.dockerignore`, and `docker-compose.yml` (already present).

Required secrets / environment variables
--------------------------------------
- DISCORD_TOKEN: Your Discord bot token (required). Add this to Render's Environment in the service settings.
- RUN_FLASK (optional): Set to `true` if you want the included Flask endpoint to run. Default is `false` in `render.yaml`.

Steps to finish deployment
--------------------------
1. Push this repo to GitHub, if it's not already there.
2. Create a Render account and connect your GitHub repo (Render will read `render.yaml`).
3. In Render's dashboard, go to the `usafhelper-bot` service that gets created and open the Environment tab.
4. Add an Environment Variable named `DISCORD_TOKEN` and paste your bot token as the value. Mark it **private**.
5. (Optional) Set `RUN_FLASK` to `true` if you want the Flask keep-alive endpoint.
6. Trigger a deploy (Render will auto-deploy on pushes to `main` if you accept the default auto-deploy).

Notes
-----
- Render's free/starter plans may sleep after long idle periods. For guaranteed always-on, pick a paid plan.
- Do NOT commit your `DISCORD_TOKEN` to the repo. If it was ever committed, rotate the token immediately.

Troubleshooting
---------------
- If the container fails to start, check Render's logs for the service. Typical issues:
  - Missing `DISCORD_TOKEN` environment variable.
  - Dependencies missing from `requirements.txt`.
  - Incorrect working directory assumptions (the Dockerfile sets `/app`)

If you want, I can attempt to trigger the deploy for you — I will need a Render API key. Otherwise, follow these steps and paste any error logs here and I'll debug them.
