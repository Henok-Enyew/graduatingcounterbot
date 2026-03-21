# UptimeRobot Setup Guide

## Problem
Render's free tier services sleep after 15 minutes of inactivity. The bot needs to stay awake to send daily messages.

## Solution
Use UptimeRobot to ping your bot every 5 minutes, keeping it alive 24/7.

---

## Step 1: Fix the 502 Bad Gateway Error

The 502 error happens because:
1. The bot might not be fully started when Render checks it
2. The Flask server needs time to initialize

**Solution:** We've added:
- Multiple health check endpoints (`/`, `/health`, `/ping`)
- 2-second startup delay for Flask
- Threaded Flask server for better concurrency

---

## Step 2: Deploy the Fixed Version

```bash
git add keep_alive_server.py main.py test_health_check.py UPTIMEROBOT_SETUP.md
git commit -m "Fix: Improve keep-alive server for UptimeRobot compatibility"
git push origin main
```

Wait 2-3 minutes for Render to deploy.

---

## Step 3: Verify the Bot is Working

### Option A: Test Locally
```bash
python test_health_check.py https://graduatingcounterbot.onrender.com
```

### Option B: Test in Browser
Open these URLs in your browser:
- https://graduatingcounterbot.onrender.com/
- https://graduatingcounterbot.onrender.com/health
- https://graduatingcounterbot.onrender.com/ping

All should return `200 OK` with text response.

---

## Step 4: Set Up UptimeRobot

### 4.1 Create Account
1. Go to https://uptimerobot.com
2. Sign up for free account
3. Verify your email

### 4.2 Add New Monitor
1. Click **"+ Add New Monitor"**
2. Fill in the details:

**Monitor Type:** HTTP(s)

**Friendly Name:** BiT Graduation Bot

**URL (or IP):** `https://graduatingcounterbot.onrender.com/health`

**Monitoring Interval:** 5 minutes (free tier)

**Monitor Timeout:** 30 seconds

**HTTP Method:** GET (HEAD might not work with Flask)

**Alert Contacts:** Your email (to get notified if bot goes down)

3. Click **"Create Monitor"**

---

## Step 5: Verify UptimeRobot is Working

### Check Monitor Status
1. Go to UptimeRobot dashboard
2. You should see your monitor with status: **Up**
3. Response time should be < 1000ms

### Check Render Logs
1. Go to Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. You should see requests coming in every 5 minutes:
   ```
   GET /health HTTP/1.1" 200
   ```

---

## Troubleshooting

### Issue: Still Getting 502 Bad Gateway

**Solution 1: Check Render Logs**
```
1. Go to Render dashboard
2. Click your service
3. Check logs for errors
4. Look for "Keep-alive server started on port 10000"
```

**Solution 2: Try Different Endpoint**
Change UptimeRobot URL to:
- `https://graduatingcounterbot.onrender.com/ping`
- Or `https://graduatingcounterbot.onrender.com/`

**Solution 3: Increase Timeout**
In UptimeRobot settings:
- Change timeout from 30s to 60s

### Issue: Bot Still Sleeps

**Check:**
1. UptimeRobot monitor is active (green)
2. Monitoring interval is 5 minutes
3. Render logs show regular requests

**Solution:**
- Make sure HTTP method is GET (not HEAD)
- Verify URL is correct (no typos)
- Check Alert Contacts are set up

### Issue: UptimeRobot Shows "Down"

**Possible Causes:**
1. Bot crashed - check Render logs
2. Render is redeploying - wait 2-3 minutes
3. Network issue - temporary, will resolve

**Solution:**
- Check Render dashboard for service status
- Review logs for errors
- Wait a few minutes and check again

---

## Alternative: Cron-job.org

If UptimeRobot doesn't work, try Cron-job.org:

1. Go to https://cron-job.org
2. Sign up for free
3. Create new cron job:
   - **Title:** BiT Graduation Bot Keep-Alive
   - **Address:** `https://graduatingcounterbot.onrender.com/health`
   - **Schedule:** Every 10 minutes
   - **Request method:** GET
4. Save and enable

---

## Expected Behavior

### When Working Correctly:
- ✅ UptimeRobot shows "Up" status
- ✅ Response time < 1000ms
- ✅ Render logs show requests every 5 minutes
- ✅ Bot sends daily messages at 00:01 AM EAT
- ✅ `/start` and `/test` commands work

### Render Logs Should Show:
```
Keep-alive server started on port 10000
Bot is fully operational!
127.0.0.1 - - [21/Mar/2026 09:33:24] "GET /health HTTP/1.1" 200 -
127.0.0.1 - - [21/Mar/2026 09:38:24] "GET /health HTTP/1.1" 200 -
```

---

## Cost

**UptimeRobot Free Tier:**
- ✅ 50 monitors
- ✅ 5-minute intervals
- ✅ Email alerts
- ✅ Unlimited checks
- ✅ No credit card required

**Render Free Tier:**
- ✅ 750 hours/month (enough for 24/7 with keep-alive)
- ✅ Automatic deploys from GitHub
- ✅ HTTPS included

**Total Cost:** $0/month 🎉

---

## Summary

1. Deploy the fixed code
2. Verify health endpoints work
3. Set up UptimeRobot with `/health` endpoint
4. Monitor should show "Up" status
5. Bot will stay alive 24/7

Your bot will now:
- ✅ Never sleep
- ✅ Send daily messages reliably
- ✅ Respond to commands instantly
- ✅ Cost $0/month
