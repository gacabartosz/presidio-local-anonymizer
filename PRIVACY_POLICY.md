# Privacy Policy - Presidio Browser Anonymizer

**Last updated:** November 15, 2025

## Overview

Presidio Browser Anonymizer is committed to protecting your privacy. This extension processes all data **locally on your computer** and does NOT send any information to external servers.

---

## Data Collection

**WE DO NOT COLLECT ANY PERSONAL DATA.**

This extension does NOT:
- ❌ Collect user data
- ❌ Send data to external servers
- ❌ Track user behavior
- ❌ Use analytics or telemetry
- ❌ Display advertisements
- ❌ Share data with third parties

---

## What Data is Processed

The extension processes the following data **locally on your computer only**:

### 1. Text Processing
- **What:** Text you paste (Ctrl+V) into web forms
- **Where:** Processed by local backend at `http://localhost:4222`
- **Why:** To detect and anonymize personally identifiable information (PII)
- **Retention:** Temporary - processed in memory, not stored permanently

### 2. Extension Configuration
- **What:** Extension settings (backend URL, toggle state)
- **Where:** Stored locally in your browser using Chrome Storage API
- **Why:** To remember your preferences
- **Retention:** Until you uninstall the extension

### 3. Anonymization Logs
- **What:** History of anonymization operations (max 100 recent entries)
- **Where:** Stored temporarily in browser memory
- **Why:** To show you what was anonymized in the dashboard
- **Retention:** Cleared when you close the dashboard or manually clear logs
- **Access:** Only you can see these logs - they never leave your computer

---

## How Data is Processed

### Local Processing Only

```
Your Computer Only - No External Servers!

1. You paste text →
2. Extension reads pasted text →
3. Sends to YOUR local backend (localhost:4222) →
4. Microsoft Presidio library (running on YOUR computer) detects PII →
5. Anonymized text returned →
6. Extension pastes anonymized text

ALL PROCESSING HAPPENS ON YOUR MACHINE!
```

### No External Communication

- ✅ Backend runs at `http://localhost:4222` (your computer)
- ✅ All processing is local
- ✅ No data sent to our servers (we don't even have servers!)
- ✅ No cloud services used
- ✅ No internet connection required (except for install)

---

## Permissions Used

The extension requests the following permissions:

### `storage`
**Why:** Save extension settings locally (backend URL, toggle state)
**Data stored:** Configuration only, no personal data
**Location:** Chrome local storage (your browser)

### `clipboardRead`
**Why:** Read pasted text when you press Ctrl+V to anonymize it
**When:** Only when you actively paste text
**Data sent:** Only to YOUR local backend (localhost:4222)

### `activeTab`
**Why:** Access current webpage to paste anonymized text
**Scope:** Only active tab, only when you paste
**Data accessed:** Text in input fields you paste into

### `contextMenus`
**Why:** Add "Anonymize selected text" option to right-click menu
**Data accessed:** Only text you manually select and right-click

### `host_permissions` (localhost:*, 127.0.0.1:*)
**Why:** Communicate with local backend running on your computer
**Servers:** Only YOUR computer - no external servers!

---

## Third-Party Libraries

### Microsoft Presidio
- **What:** Open-source PII detection library
- **Where:** Runs on YOUR computer (local backend)
- **Privacy:** No data sent to Microsoft or anyone else
- **Source code:** https://github.com/microsoft/presidio

### No Analytics or Tracking
- We do NOT use Google Analytics
- We do NOT use any crash reporting
- We do NOT use any telemetry
- We do NOT track you in any way

---

## Data Retention

| Data Type | Retention | Location |
|-----------|-----------|----------|
| Extension settings | Until uninstall | Browser local storage |
| Pasted text | Processed in memory, not stored | - |
| Anonymization logs | Max 100 entries, in memory | Browser |
| Backend data | Temporary, cleared on restart | Your computer (localhost) |

### How to Delete Data

1. **Clear logs:** Dashboard → "Wyczyść Logi" button
2. **Clear settings:** Uninstall extension
3. **Clear backend data:** Restart backend service

---

## Your Rights

### Access to Data
You have full access to all data - it's all on YOUR computer!

### Data Portability
Not applicable - no data is stored externally.

### Right to Deletion
Uninstall the extension or clear logs in dashboard.

### Right to Audit
Full source code available on GitHub:
https://github.com/gacabartosz/presidio-local-anonymizer

You can inspect every line of code to verify our privacy claims.

---

## Security

### Local Processing
- All PII detection happens on YOUR computer
- No data ever leaves your machine
- Even we (developers) cannot access your data!

### Open Source
- Full source code available
- Community can audit for security issues
- Transparent development process

### No Authentication Required
- No accounts needed
- No passwords stored
- No login required

---

## Children's Privacy

This extension does not knowingly collect data from anyone, including children under 13. Since we don't collect ANY data, we comply with COPPA (Children's Online Privacy Protection Act).

---

## Changes to This Policy

We may update this Privacy Policy from time to time. We will notify users of any changes by:
- Updating the "Last updated" date
- Publishing changes on GitHub
- Notifying via Chrome Web Store update notes

---

## Contact Us

If you have questions about this Privacy Policy:

- **GitHub Issues:** https://github.com/gacabartosz/presidio-local-anonymizer/issues
- **GitHub Discussions:** https://github.com/gacabartosz/presidio-local-anonymizer/discussions
- **Email:** (available on GitHub profile)

---

## Compliance

### GDPR (Europe)
- ✅ No personal data collected
- ✅ No data processing outside user's computer
- ✅ Full transparency (open source)
- ✅ User control (ON/OFF toggle, delete logs)

### CCPA (California)
- ✅ No personal information sold
- ✅ No personal information shared
- ✅ No personal information collected for commercial purposes

### LGPD (Brazil)
- ✅ Data processed only locally
- ✅ User consent via extension install
- ✅ Transparent processing

---

## Summary

**In Plain English:**

1. **We don't collect your data** - Period.
2. **Everything happens on your computer** - No external servers.
3. **You have full control** - ON/OFF toggle, delete logs anytime.
4. **Open source** - Audit the code yourself.
5. **No tracking** - No analytics, no ads, no telemetry.

Your privacy is our priority. That's why we built this extension to work 100% locally.

---

**Last updated:** November 15, 2025
**Version:** 1.3.0
**GitHub:** https://github.com/gacabartosz/presidio-local-anonymizer
