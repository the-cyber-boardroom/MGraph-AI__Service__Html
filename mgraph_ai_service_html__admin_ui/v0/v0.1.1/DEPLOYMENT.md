# v0.1.1 Deployment Guide

## Overview

This guide explains how to deploy v0.1.1 of the HTML Service Admin UI.

## Files Created

### Total Files: 27

**Pages (3)**:
- `index.html` - Enhanced dashboard
- `playground.html` - NEW playground page
- `404.html` - Error page

**CSS (3)**:
- `css/common.css` - Shared styles
- `css/dashboard.css` - Dashboard styles
- `css/playground.css` - NEW playground layout

**JavaScript (3)**:
- `js/services/api-client.js` - API client
- `js/dashboard.js` - Dashboard logic
- `js/playground.js` - NEW playground orchestrator

**Components (12 files across 4 components)**:
- `components/top-nav/` - 3 files (HTML, CSS, JS)
- `components/html-input/` - 3 files (HTML, CSS, JS)
- `components/transformation-selector/` - 3 files (HTML, CSS, JS)
- `components/output-viewer/` - 3 files (HTML, CSS, JS)

**Samples (3)**:
- `samples/simple.html`
- `samples/complex.html`
- `samples/playground.html` - NEW self-referential

**Documentation (2)**:
- `README.md`
- `DEPLOYMENT.md` (this file)

## Deployment Steps

### Step 1: Copy Files

Copy all files from the generated v0.1.1 folder to your project:

```bash
# From your project root
cp -r /path/to/generated/v0.1.1/* mgraph_ai_service_html__admin_ui/v0/v0.1.1/
```

### Step 2: Verify Structure

Your structure should look like:

```
mgraph_ai_service_html__admin_ui/
├── __init__.py
└── v0/
    ├── v0.1.0/
    │   └── ... (existing files)
    └── v0.1.1/
        ├── index.html
        ├── playground.html
        ├── 404.html
        ├── README.md
        ├── DEPLOYMENT.md
        ├── css/
        ├── components/
        ├── js/
        └── samples/
```

### Step 3: Update Backend Service

If using `Html__Admin__Service.py`, update the version:

```python
class Html__Admin__Service(Type_Safe):
    current_version: Safe_Str__Version = Safe_Str__Version("v0.1.1")  # Changed from v0.1.0
    # ... rest of the class
```

### Step 4: Test Locally

1. Start your FastAPI server
2. Navigate to: `http://localhost:8000/html-service/`
3. Should redirect to: `http://localhost:8000/html-service/v0/v0.1.1/index.html`
4. Click "Transformation Playground" card
5. Should load: `http://localhost:8000/html-service/v0/v0.1.1/playground.html`

### Step 5: Test Playground

1. On playground page, verify:
   - Simple sample loads automatically
   - Sample selector works
   - Choose "HTML → Dict" transformation
   - Click "Transform" button
   - Verify JSON output displays
   - Test "Copy" button
   - Test "Download" button

2. Test all transformations:
   - HTML → Dict ✓
   - HTML → Text Nodes ✓
   - HTML → Lines ✓
   - HTML → HTML (Hashes) ✓
   - HTML → HTML (XXX) ✓

### Step 6: Verify Backend Integration

Ensure these endpoints are working:
- `POST /html/to__dict`
- `POST /html/to__text__nodes`
- `POST /html/to__lines`
- `POST /html/to__html__hashes`
- `POST /html/to__html__xxx`

All should return proper responses when called from playground.

## Troubleshooting

### Issue: Components not loading

**Symptom**: Blank sections on playground page

**Solution**: Check browser console for fetch errors. Verify file paths are correct relative to playground.html:
- `./components/top-nav/top-nav.html`
- `./components/html-input/html-input.html`
- etc.

### Issue: Transformations not working

**Symptom**: Error displayed in output viewer

**Possible causes**:
1. Service not running
2. Wrong endpoint URLs
3. CORS issues (shouldn't happen if served from same origin)
4. Invalid HTML input

**Check**:
- Browser console for errors
- Network tab for failed requests
- Service logs for backend errors

### Issue: Samples not loading

**Symptom**: "Failed to load sample file" alert

**Solution**: Verify sample files exist at `./samples/` relative to playground.html

### Issue: 404 on navigation

**Symptom**: Custom 404 page not showing

**Solution**: Verify `404.html` exists in v0.1.1 root directory

## IFD Compliance Check

✅ Version Independence
- v0.1.1 is completely self-contained
- No imports from v0.1.0
- Can delete v0.1.0 without breaking v0.1.1

✅ Copy Forward
- v0.1.1 was created by copying v0.1.0 and enhancing
- Shared code was copied, not imported

✅ Real Data
- Playground calls actual API endpoints
- No mocked responses

✅ Zero Dependencies
- Pure HTML/CSS/JavaScript
- No external libraries

## Performance Notes

**Component Loading**: Components load templates asynchronously. First page load may show brief flash as components initialize.

**Sample Loading**: Default sample (simple.html) loads on component mount, may take 50-100ms.

**API Calls**: Transformation speed depends on HTML size and endpoint complexity. Most complete in < 500ms.

## Security Notes

**Path Traversal**: Backend service should validate paths to prevent directory traversal attacks.

**Input Validation**: Frontend accepts any HTML, backend should validate and sanitize.

**File Size**: HTML input limited to 1MB (browser-side warning at 900KB).

## Next Steps

After successful deployment:

1. Monitor for errors in production
2. Gather user feedback
3. Plan v0.1.2 features based on usage
4. Consider adding:
   - Request/response logging
   - Performance metrics
   - User preferences (theme, default sample)

---

**Version**: 0.1.1  
**Status**: Ready for Deployment  
**Methodology**: IFD  
**Date**: 2024
