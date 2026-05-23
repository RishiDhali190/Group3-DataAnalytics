# How to Deploy Consumer360 Online

## Option 1: GitHub Pages (Free & Easy)

1. Create a GitHub account at https://github.com (if you don't have one)

2. Create a new repository:
   - Go to https://github.com/new
   - Name it: `consumer360-analytics`
   - Make it Public
   - Click "Create repository"

3. Upload your file:
   - Click "uploading an existing file"
   - Drag and drop `index.html`
   - Click "Commit changes"

4. Enable GitHub Pages:
   - Go to Settings → Pages
   - Under "Source", select "main" branch
   - Click Save

5. Your link will be:
   ```
   https://YOUR-USERNAME.github.io/consumer360-analytics/index.html
   ```

**Time:** 5 minutes | **Cost:** Free

---

## Option 2: Netlify Drop (Fastest)

1. Go to https://app.netlify.com/drop

2. Drag and drop your `index.html` file

3. Get instant link like:
   ```
   https://random-name-12345.netlify.app
   ```

**Time:** 30 seconds | **Cost:** Free

---

## Option 3: Vercel (Professional)

1. Go to https://vercel.com/new

2. Sign in with GitHub

3. Drag and drop your file or connect your GitHub repo

4. Get link like:
   ```
   https://consumer360-analytics.vercel.app
   ```

**Time:** 2 minutes | **Cost:** Free

---

## Option 4: Local Network Access (No Internet Needed)

If you just want to share with people on the same WiFi:

1. Open Command Prompt in the folder with index.html

2. Run:
   ```
   python -m http.server 8000
   ```
   (If you have Python installed)

3. Share this link with others on your network:
   ```
   http://YOUR-LOCAL-IP:8000/index.html
   ```

To find your local IP:
```
ipconfig
```
Look for "IPv4 Address" (usually starts with 192.168.x.x)

---

## Recommended: Netlify Drop

**Easiest and fastest** — just drag and drop, get instant link, no account needed!

Visit: https://app.netlify.com/drop
