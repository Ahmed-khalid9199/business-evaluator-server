# ✅ SendGrid API Setup for Render (SMTP Blocked Solution)

## Problem
Render blocks **ALL outbound SMTP ports** (25, 587, 465) to prevent spam. You must use SendGrid's **HTTP API** instead.

## Solution Implemented
Your code now automatically uses:
- **SendGrid API** when `SENDGRID_API_KEY` is set (production on Render)
- **SMTP** when `SENDGRID_API_KEY` is not set (local development)

---

## Step-by-Step Setup

### 1. Create SendGrid Account (2 minutes)

1. Sign up: https://signup.sendgrid.com/
   - **Free tier**: 100 emails/day forever ✅
2. Verify your email address
3. Complete the onboarding (skip integrations for now)

### 2. Generate API Key (1 minute)

1. Go to: https://app.sendgrid.com/settings/api_keys
2. Click **"Create API Key"**
3. Name: `Render Production`
4. Select **"Restricted Access"**:
   - Expand **"Mail Send"**
   - Set to **"Full Access"** ✅
5. Click **"Create & View"**
6. **COPY THE API KEY** (starts with `SG.`)
   - ⚠️ You can only see it once! Save it securely.

### 3. Verify Sender Identity (2 minutes)

**Option A: Single Sender Verification** (Easiest for small projects)
1. Go to: https://app.sendgrid.com/settings/sender_auth/senders
2. Click **"Create New Sender"**
3. Fill in details:
   - **From Name**: Chelsea Corporate
   - **From Email**: noreply@chelseacorporate.com (or any email you own)
   - **Reply To**: info@chelseacorporate.com
   - **Company**: Chelsea Corporate
   - Fill in address (required by SendGrid)
4. Click **"Create"**
5. **Check your email** and click verification link

**Option B: Domain Authentication** (Best for production - prevents spam)
1. Go to: https://app.sendgrid.com/settings/sender_auth
2. Click **"Authenticate Your Domain"**
3. Follow instructions to add DNS records to your domain

### 4. Update Render Environment Variables

In your **Render Dashboard** → Your Service → **Environment**:

**Remove these** (SMTP no longer needed):
```
❌ EMAIL_HOST
❌ EMAIL_PORT
❌ EMAIL_HOST_USER
❌ EMAIL_HOST_PASSWORD
❌ EMAIL_USE_TLS
❌ EMAIL_USE_SSL
```

**Add/Update these**:
```env
# SendGrid API Key (REQUIRED)
SENDGRID_API_KEY=SG.your-actual-sendgrid-api-key-here

# From Email (must match verified sender)
DEFAULT_FROM_EMAIL=noreply@chelseacorporate.com

# Contact Info (shown in emails)
CONTACT_EMAIL=info@chelseacorporate.com
CONTACT_PHONE=(0) 20 3011 1373
SITE_URL=https://chelseacorporate.com
BACKEND_URL=https://your-backend.onrender.com

# Django Settings
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=your-app.onrender.com

# Database (if using PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Optional: Keep console backend for local dev fallback
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Deploy to Render

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn evaluator_server.wsgi:application --config gunicorn.conf.py
```

Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Testing

### Test 1: Check Logs
After deploying, submit a test form and check Render logs:

**Success messages to look for:**
```
INFO ... Email queued for user@example.com for lead ID abc123
INFO ... Business evaluation email sent to user@example.com for lead ID abc123 (SendGrid API, status: 202)
```

### Test 2: Check SendGrid Dashboard
1. Go to: https://app.sendgrid.com/email_activity
2. You should see your sent email
3. Status should be "Delivered" or "Processed"

### Test 3: Check Email Inbox
- Check recipient's inbox (might take 1-2 minutes)
- Check spam folder if not in inbox
- Verify email looks correct with logo and formatting

---

## Troubleshooting

### Error: "The from email does not match a verified Sender Identity"

**Solution**: Your `DEFAULT_FROM_EMAIL` must match a verified sender in SendGrid.

1. Check: https://app.sendgrid.com/settings/sender_auth/senders
2. Verify the email is listed and verified (green checkmark)
3. Update `DEFAULT_FROM_EMAIL` in Render to match exactly

### Error: "Forbidden: You do not have authorization"

**Solution**: Your API key doesn't have Mail Send permissions.

1. Go to: https://app.sendgrid.com/settings/api_keys
2. Delete the old key
3. Create a new key with **"Mail Send" → "Full Access"**
4. Update `SENDGRID_API_KEY` in Render

### Email goes to spam folder

**Solutions**:
1. ✅ Verify sender identity (see Step 3)
2. ✅ Set up domain authentication (prevents SPF/DKIM issues)
3. ✅ Use a professional from address (not gmail.com)
4. ✅ Ask recipients to mark as "Not Spam"

### Error: "No SendGrid API key configured"

**Solution**: Check Render environment variables.

1. Go to Render Dashboard → Environment
2. Verify `SENDGRID_API_KEY` is set (starts with `SG.`)
3. No spaces or quotes around the value
4. Click "Save Changes" and redeploy

### Email not sending at all

**Debug checklist**:
1. Check Render logs for error messages
2. Verify API key is correct (regenerate if needed)
3. Check SendGrid dashboard for blocked sends
4. Verify sender email is verified in SendGrid
5. Test API key with SendGrid's API Explorer: https://docs.sendgrid.com/api-reference/mail-send/mail-send

---

## Local Development

For local testing, your code will automatically use SMTP (console backend) if `SENDGRID_API_KEY` is not set.

**Option 1: Console Output (Default)**
```env
# In local .env file (no SendGrid key)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Emails print to terminal instead of sending.

**Option 2: Test with SendGrid Locally**
```env
# In local .env file
SENDGRID_API_KEY=SG.your-api-key-here
DEFAULT_FROM_EMAIL=noreply@chelseacorporate.com
```
Emails send via SendGrid API (counts toward your 100/day limit).

## Summary

✅ **What Changed:**
- Added `sendgrid==6.11.0` to requirements.txt
- Updated `api/signals.py` to use SendGrid HTTP API
- Updated `evaluator_server/settings.py` to support `SENDGRID_API_KEY`
- Emails send asynchronously (non-blocking)

✅ **What You Need to Do:**
1. Create SendGrid account
2. Generate API key with Mail Send permission
3. Verify sender email
4. Add `SENDGRID_API_KEY` to Render environment
5. Set `DEFAULT_FROM_EMAIL` to verified sender
6. Redeploy

✅ **Expected Result:**
- Emails send successfully via SendGrid API
- No SMTP/network errors
- Requests complete in < 3 seconds
- Emails deliver within 1-2 minutes

🎉 **You're all set!** Emails will now work reliably on Render.

