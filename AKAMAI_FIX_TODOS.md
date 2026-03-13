# Akamai Bot Detection - Troubleshooting Todos

## Problem
First HTTP request to NSE is getting blocked/delayed by Akamai bot detection. Not detection from repeated calls, but from initial request headers/TLS mismatch.

## Root Causes
1. **Outdated User-Agent** (Chrome 80 from Feb 2020)
2. **Missing modern browser headers** (Sec-CH-UA-*)
3. **TLS fingerprint mismatch** (Python requests library vs claimed Chrome)
4. **Dead/suspicious headers** (old sec-fetch values)

---

## Todos (Easiest to Hardest)

### 1. Update User-Agent to Current Chrome
- [x] Update Chrome version to 2026 current (Chrome 134.0.6998.166)
- [x] Standardize all User-Agent strings across history.py, archives.py, live.py, bse/live.py
- [ ] Test: Run test_cookie and check if Akamai accepts it
- **Why this first**: Simplest change, highest ROI. Just string replacement.
- **Files updated**: All 7 locations updated to Chrome 134 from Chrome 80/84/120

### 2. Add Missing Sec-CH-UA Headers
- [x] Add `Sec-CH-UA: "Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"` to match updated User-Agent
- [x] Add `Sec-CH-UA-Mobile: ?0`
- [x] Add `Sec-CH-UA-Platform: "Windows"`
- [x] Add modern headers: `DNT: 1`, `Upgrade-Insecure-Requests: 1`
- [ ] Test: Run test_cookie again
- **Why**: Modern Akamai expects these. Real browsers always send them.
- **Files updated**: All modules (history.py, live.py, archives.py, bse/live.py)

### 3. Clean Up Suspicious Headers
- [ ] Remove or verify `pragma: no-cache` (uncommon in modern browsers)
- [ ] Remove or fix `Cache-Control` (should be "no-cache" or modern values)
- [ ] Verify Referer path is realistic for the request
- [ ] Test: Run test_cookie
- **Why**: Outdated header combinations scream "bot"

### 4. Add Common Modern Headers
- [ ] Add `DNT: 1`
- [ ] Add `Upgrade-Insecure-Requests: 1`
- [ ] Adjust Accept-Language to current standards
- [ ] Test: Run test_cookie

### 5. Use `httpx` with Custom Adapter (TLS Fingerprinting)
- [ ] Install `httpx` + `httpcore`
- [ ] Create custom adapter with Chrome-like TLS cipher suite
- [ ] Replace requests.Session with httpx.Client
- **Why**: Last resort. Fixes TLS mismatch but requires redesign.
- **Effort**: High

---

## Testing Strategy
After each todo, run:
```bash
pytest tests/test_nse.py::test_cookie -v -s
```

Track response status codes:
- 200 = Success
- 403/401 = Akamai rejected us
- Hanging/timeout = Still being throttled
