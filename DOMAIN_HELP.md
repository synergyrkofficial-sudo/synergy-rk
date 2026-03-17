# Domain setup help (Vercel + GoDaddy)

This project is deployed with the Vercel CLI (no GitHub). If the CLI domain linking fails, follow the steps below to manually connect your custom domain **`synergyrkofficial.com`** in the Vercel Dashboard.

## 1) Add the domain in Vercel Dashboard

1. Open the **Vercel Dashboard**.
2. Select your **project** (the one deployed from the `frontend/` folder).
3. Go to **Settings → Domains**.
4. Click **Add** and enter:
   - `synergyrkofficial.com`
5. Click **Add** / **Save**.

Vercel will show you the DNS records required. For GoDaddy, you’ll typically add a CNAME record for the subdomain.

## 2) GoDaddy DNS record (CNAME)

Add this record in **GoDaddy → DNS Management** for your domain:

- **Type**: CNAME  
- **Name**: synergyrk  
- **Value**: cname.vercel-dns.com

## 3) Verify

- Wait for DNS propagation (can take minutes to hours).
- In Vercel **Settings → Domains**, the domain should move to **Verified** once DNS is correct.

## 4) If you used a Vercel URL first (alias)

If Vercel gave you a deployment URL like `https://xxxxx.vercel.app`, you can point your domain to it with:

```bash
vercel alias set [YOUR_VERCEL_URL] synergyrkofficial.com
```

