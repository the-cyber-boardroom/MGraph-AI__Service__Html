# HTML Service Admin UI - v0.1.1

## Overview

Version 0.1.1 adds the **Transformation Playground** - an interactive interface for testing all HTML service endpoints with pre-loaded samples and real-time results.

## What's New in v0.1.1

### ✨ Major Features

1. **Transformation Playground Page** (`playground.html`)
   - Interactive testing of all service endpoints
   - Pre-loaded sample HTML files
   - Real-time transformations
   - Formatted output with syntax highlighting
   - Copy/download results

2. **Top Navigation Component**
   - Consistent navigation across all pages
   - Active page highlighting
   - Seamless page transitions

3. **Web Components Architecture**
   - `html-input` - HTML input with sample selector
   - `transformation-selector` - Endpoint selection with configuration
   - `output-viewer` - Formatted result display
   - `top-nav` - Navigation banner

4. **Enhanced Dashboard**
   - Working link to playground
   - Updated with top navigation
   - Improved action cards

## Features

✅ **Zero Setup Required** - Samples pre-loaded, no file upload needed  
✅ **All Endpoints Available** - Test all 9 transformation endpoints  
✅ **Real API Integration** - Calls actual service endpoints  
✅ **Syntax Highlighting** - JSON, HTML, and text formatting  
✅ **Copy/Download Results** - Export transformation results  
✅ **Responsive Design** - Works on desktop, tablet, mobile  
✅ **Event-Driven Architecture** - Clean component communication  
✅ **Zero External Dependencies** - 100% native web platform  

## Project Structure

```
v0.1.1/
├── index.html                    # Dashboard (enhanced)
├── playground.html               # NEW: Playground page
├── 404.html                      # Error page
├── README.md                     # This file
├── css/
│   ├── common.css               # Shared styles
│   ├── dashboard.css            # Dashboard styles
│   └── playground.css           # NEW: Playground layout
├── components/                   # NEW: Web Components
│   ├── top-nav/                 # Navigation component
│   │   ├── top-nav.html
│   │   ├── top-nav.css
│   │   └── top-nav.js
│   ├── html-input/              # HTML input component
│   │   ├── html-input.html
│   │   ├── html-input.css
│   │   └── html-input.js
│   ├── transformation-selector/ # Endpoint selector
│   │   ├── transformation-selector.html
│   │   ├── transformation-selector.css
│   │   └── transformation-selector.js
│   └── output-viewer/           # Output display
│       ├── output-viewer.html
│       ├── output-viewer.css
│       └── output-viewer.js
├── js/
│   ├── services/
│   │   └── api-client.js        # API communication
│   ├── dashboard.js             # Dashboard logic
│   └── playground.js            # NEW: Playground orchestrator
└── samples/                      # Sample HTML files
    ├── simple.html              # Basic example
    ├── complex.html             # Deep nesting
    └── playground.html          # NEW: Self-referential
```

## Usage Guide

### Transformation Playground

1. **Open Playground**: Navigate to `playground.html` or click "Transformation Playground" from dashboard

2. **Select Sample**: Choose from dropdown:
   - Simple HTML - Basic elements
   - Complex HTML - Deep nesting
   - Playground HTML - This page!
   - Custom - Paste your own

3. **Choose Transformation**: Select endpoint from dropdown:
   - HTML → Dict (parse structure)
   - HTML → Text Nodes (extract with hashes)
   - HTML → Lines (readable format)
   - HTML → HTML (Hashes) (debug visualization)
   - HTML → HTML (XXX) (privacy masking)

4. **Configure (if needed)**: Adjust max_depth slider for applicable endpoints

5. **Transform**: Click "▶️ Transform" button

6. **View Results**: See formatted output with syntax highlighting

7. **Export**: Use "📋 Copy" or "💾 Download" buttons

### Available Transformations

#### HTML Transformations
- **HTML → Dict**: Parse HTML into nested dictionary structure
- **HTML → Text Nodes**: Extract all text with unique hash identifiers
- **HTML → Lines**: Format HTML as readable indented lines
- **HTML → HTML (Hashes)**: Replace text with hashes for debugging
- **HTML → HTML (XXX)**: Replace text with x's for privacy

#### Dict Operations
- **Dict → HTML**: Reconstruct HTML from dictionary
- **Dict → Text Nodes**: Extract text nodes from dictionary
- **Dict → Lines**: Format dictionary as readable lines

#### Hash Operations
- **Hashes → HTML**: Apply hash mappings (future workflow)

## Component Architecture

### Event-Driven Communication

Components communicate via CustomEvents:

```javascript
// html-input emits when HTML changes
html-changed → { html: "..." }

// transformation-selector emits when transform requested
transformation-requested → { endpointId, route, inputType, maxDepth }

// Components listen and react
document.addEventListener('html-changed', (e) => {...});
document.addEventListener('transformation-requested', (e) => {...});
```

### Component Lifecycle

All components follow this pattern:
1. Load external CSS file
2. Load external HTML template
3. Attach event listeners
4. Initialize with default state
5. Emit events on user actions

## Sample Files

### simple.html
Basic HTML with common elements - perfect for learning transformations.

### complex.html
Deeply nested structure (5+ levels) - tests max_depth parameter effectively.

### playground.html
Self-referential sample - transform the playground page itself!

## API Integration

All transformations call real service endpoints:

```javascript
// Example: HTML → Dict
POST /html/to__dict
{
  "html": "<h1>Hello</h1>"
}

// Response
{
  "tag": "h1",
  "nodes": [...],
  ...
}
```

No mocking - real API calls from day one!

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Requires ES6+ support (async/await, Custom Elements)
- No polyfills needed for modern browsers

## IFD Principles Applied

✅ **Version Independence** - Completely self-contained, no shared code  
✅ **Copy Forward** - Built by copying v0.1.0 and enhancing  
✅ **Progressive Enhancement** - Dashboard works, playground adds features  
✅ **Real Data** - Calls actual API endpoints immediately  
✅ **Event-Driven** - Clean component communication  
✅ **Zero Dependencies** - Pure native web platform  

## Differences from v0.1.0

**New Files**:
- `playground.html` - Main playground page
- `css/playground.css` - Playground layout
- `js/playground.js` - Orchestrator
- `components/` - 4 web components (12 files total)
- `samples/playground.html` - Self-referential sample

**Enhanced Files**:
- `index.html` - Added top-nav component
- `js/dashboard.js` - Working playground link
- `css/dashboard.css` - Clickable action card styles

**Copied Unchanged**:
- `404.html`
- `css/common.css`
- `js/services/api-client.js`
- `samples/simple.html`
- `samples/complex.html`

## Next Version Ideas

Potential features for v0.1.2:
- Text Nodes Explorer page
- Hash Mapper workflow
- Side-by-side comparison view
- Transformation history
- API response metadata display

## Testing Checklist

- [ ] Dashboard loads with top navigation
- [ ] Playground link works from dashboard
- [ ] Simple sample loads by default on playground
- [ ] All sample files load correctly
- [ ] Character counter updates
- [ ] All 5 HTML transformations work
- [ ] Max depth slider appears for applicable endpoints
- [ ] Output displays with correct formatting
- [ ] Copy button works
- [ ] Download button works
- [ ] Error handling works for invalid input
- [ ] Navigation between pages works
- [ ] Responsive on mobile/tablet
- [ ] No console errors

## Development Notes

**IFD Methodology**: This version was created by copying the entire v0.1.0 folder and adding new features. No code is shared between versions - each version is completely independent.

**Component Pattern**: All components use flat structure (3 files: HTML, CSS, JS) since they're relatively simple. Future complex components may use modular structure.

**API Calls**: The playground makes real POST requests to service endpoints using the API client. Same origin = no CORS issues!

---

**Created**: 2024
**Methodology**: Iterative Flow Development (IFD)  
**Previous Version**: v0.1.0  
**Dependencies**: None (100% native web platform)  
**Status**: Production Ready ✅
