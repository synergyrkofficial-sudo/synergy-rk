# Domain setup (Render or Railway)

This repo has a frontend (static) and a Flask backend API. The frontend now calls:
- https://api.synergyrkofficial.com

That means:
- Your root domain should serve the frontend
- Your API should live at the api subdomain

## Render (recommended for backend)
1) In Render, open your backend service.
2) Add a custom domain: api.synergyrkofficial.com
3) Render will show the DNS records you must add at your DNS provider.
4) Add those exact records (no https://). Wait for verification.

## Railway (alternative for backend)
1) In Railway, open your service.
2) Add a custom domain: api.synergyrkofficial.com
3) Railway will show the DNS records. Add them at your DNS provider.

## Frontend domain
Host the frontend on any static host (Render Static Site, Vercel, Netlify, GitHub Pages).
Then:
- Add synergyrkofficial.com and www.synergyrkofficial.com in that host
- Use the DNS records that host provides for the apex (@) and www

## Quick DNS tips
- Use only hostnames in DNS values (no https://)
- Wait for propagation after changes