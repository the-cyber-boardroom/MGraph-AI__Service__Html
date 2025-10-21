/**
 * Playground Controller - v0.1.6
 * Web Component for managing the transformation playground
 *
 * NEW in v0.1.6:
 * - Edit/View mode switching for all columns
 * - Status messages in header
 * - Middle column editing support
 * - Syntax highlighting in view mode
 *
 * Base functionality from v0.1.5
 */

import { Syntax__Highlighter } from '../../../v0.1.4/js/utils/Syntax__Highlighter.js';
import { Samples } from '../../../v0.1.5/data/samples.js';

class PlaygroundController extends HTMLElement {
    constructor() {
        super();
        console.log('🎮 PlaygroundController constructor called (v0.1.6)');

        // State
        this.state = {
            // NEW v0.1.6: Mode state for each column
            column1Mode: 'edit',  // 'edit' | 'view'
            column2Mode: 'view',  // 'view' | 'edit'
            column3Mode: 'view',  // 'view' only for now

            // Existing state (from v0.1.5)
            originalHtml: '',
            currentDict: null,
            currentHashes: null,
            currentCreatedHtml: null,
        };

        // Load syntax highlighter styles
        Syntax__Highlighter.loadStyles();
    }

    connectedCallback() {
        console.log('🎮 PlaygroundController connectedCallback - component mounted!');

        // Get DOM references
        this.getDOMReferences();

        // Attach event listeners
        this.attachEventListeners();

        // NEW v0.1.6: Setup mode tab listeners
        this.setupModeTabListeners();

        console.log('✅ Event listeners attached');

        // Auto-run full flow on load
        console.log('🚀 Running auto-flow: Load Micro → Parse → Rebuild');
        setTimeout(() => {
            this.runFullFlow();
        }, 500);
    }

    disconnectedCallback() {
        console.log('🎮 PlaygroundController disconnected');
        // Cleanup if needed
    }

    /**
     * Get all DOM element references
     */
    getDOMReferences() {
        // Input elements
        this.htmlInput = document.getElementById('html-input');
        this.sampleSelector = document.getElementById('sample-selector');
        this.charCount = document.getElementById('char-count');

        // Middle column outputs
        this.dictOutput = document.getElementById('dict-output');
        this.hashesOutput = document.getElementById('hashes-output');

        // NEW v0.1.6: Middle column edit textareas
        this.dictEdit = document.getElementById('dict-edit');
        this.hashesEdit = document.getElementById('hashes-edit');

        // NEW v0.1.6: Original HTML view
        this.htmlView = document.getElementById('html-view');

        // Right column output
        this.createdHtmlOutput = document.getElementById('created-html-output');
        this.statusMessage = document.getElementById('status-message');

        // Buttons
        this.btnClearInput = document.getElementById('btn-clear-input');
        this.btnTransformParse = document.getElementById('btn-transform-parse');
        this.btnTransformRebuild = document.getElementById('btn-transform-rebuild');
        this.btnCopyOutput = document.getElementById('btn-copy-output');
        this.btnDownloadOutput = document.getElementById('btn-download-output');

        // Debug buttons
        this.debugLoadMicro = document.getElementById('debug-load-micro');
        this.debugLoadSimple = document.getElementById('debug-load-simple');
        this.debugParse = document.getElementById('debug-parse');
        this.debugRebuild = document.getElementById('debug-rebuild');
        this.debugFullFlow = document.getElementById('debug-full-flow');

        console.log('✅ DOM references obtained');
    }

    /**
     * Attach all event listeners
     */
    attachEventListeners() {
        // Input events
        this.htmlInput?.addEventListener('input', () => this.updateCharCount());
        this.sampleSelector?.addEventListener('change', (e) => this.loadSample(e.target.value));

        // Button events
        this.btnClearInput?.addEventListener('click', () => this.clearInput());
        this.btnTransformParse?.addEventListener('click', () => this.parseHtml());
        this.btnTransformRebuild?.addEventListener('click', () => this.rebuildHtml());
        this.btnCopyOutput?.addEventListener('click', () => this.copyOutput());
        this.btnDownloadOutput?.addEventListener('click', () => this.downloadOutput());

        // Debug button listeners
        this.debugLoadMicro?.addEventListener('click', () => this.loadSample('micro'));
        this.debugLoadSimple?.addEventListener('click', () => this.loadSample('simple'));
        this.debugParse?.addEventListener('click', () => this.parseHtml());
        this.debugRebuild?.addEventListener('click', () => this.rebuildHtml());
        this.debugFullFlow?.addEventListener('click', () => this.runFullFlow());
    }

    // ========================================
    // NEW v0.1.6: Mode Switching
    // ========================================

    /**
     * Setup mode tab listeners
     */
    setupModeTabListeners() {
        document.querySelectorAll('.mode-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                const column = e.target.dataset.column;
                this.switchMode(column, mode);
            });
        });
        console.log('✅ Mode tab listeners attached');
    }

    /**
     * Switch column mode
     */
    switchMode(column, mode) {
        console.log(`🔄 Switching ${column} to ${mode} mode`);

        // Map column names to numbers
        const columnMap = {
            'original': 1,
            'middle': 2,
            'created': 3
        };

        const columnNum = columnMap[column];

        // Update state
        this.state[`column${columnNum}Mode`] = mode;

        // Update DOM attribute
        const columnElement = document.getElementById(`column-${column}`);
        columnElement.setAttribute('data-mode', mode);

        // Update active tab
        this.updateActiveTab(column, mode);

        // Sync content between modes
        this.syncModeContent(column, mode);
    }

    /**
     * Update active tab styling
     */
    updateActiveTab(column, mode) {
        const columnElement = document.getElementById(`column-${column}`);
        const tabs = columnElement.querySelectorAll('.mode-tab');

        tabs.forEach(tab => {
            if (tab.dataset.mode === mode) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });
    }

    /**
     * Sync content when switching modes
     */
    syncModeContent(column, mode) {
        if (column === 'original') {
            if (mode === 'view') {
                // Switching to view mode - update syntax highlighting
                this.updateSyntaxHighlighting();
            } else {
                // Switching to edit mode - sync textarea with current value
                // (already in sync, no action needed)
            }
        }

        if (column === 'middle') {
            if (mode === 'edit') {
                // Switching to edit mode - populate textareas with current JSON
                this.populateMiddleEdit();
            } else {
                // Switching to view mode - parse JSON from textareas and update view
                this.parseMiddleEdit();
            }
        }
    }

    /**
     * Update syntax highlighting for original HTML view
     */
    updateSyntaxHighlighting() {
        const htmlContent = this.htmlInput.value;

        if (!htmlContent.trim()) {
            this.htmlView.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">👁️</div>
                    <div class="empty-state-text">Syntax-highlighted HTML will appear here</div>
                </div>
            `;
            return;
        }

        // Use syntax highlighter
        const highlighted = Syntax__Highlighter.highlight(htmlContent, 'html');
        this.htmlView.innerHTML = `<pre class="syntax-output">${highlighted}</pre>`;
    }

    /**
     * Populate middle column edit mode with current JSON
     */
    populateMiddleEdit() {
        if (this.state.currentDict) {
            this.dictEdit.value = JSON.stringify(this.state.currentDict, null, 2);
        } else {
            this.dictEdit.value = '';
        }

        if (this.state.currentHashes) {
            this.hashesEdit.value = JSON.stringify(this.state.currentHashes, null, 2);
        } else {
            this.hashesEdit.value = '';
        }
    }

    /**
     * Parse middle column edit mode and update view
     */
    parseMiddleEdit() {
        try {
            // Parse Dict
            if (this.dictEdit.value.trim()) {
                this.state.currentDict = JSON.parse(this.dictEdit.value);
            }

            // Parse Hashes
            if (this.hashesEdit.value.trim()) {
                this.state.currentHashes = JSON.parse(this.hashesEdit.value);
            }

            // Update view mode display
            this.renderMiddleView();

            return true;
        } catch (e) {
            this.showStatus('error', 'Invalid JSON in edit mode: ' + e.message);
            console.error('❌ JSON parse error:', e);
            return false;
        }
    }

    /**
     * Render middle column view mode
     */
    renderMiddleView() {
        if (this.state.currentDict) {
            this.dictOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.state.currentDict, 'json')}</pre>`;
        } else {
            this.dictOutput.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📐</div>
                    <div class="empty-state-text">HTML structure will appear here after parsing</div>
                </div>
            `;
        }

        if (this.state.currentHashes) {
            this.hashesOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.state.currentHashes, 'json')}</pre>`;
        } else {
            this.hashesOutput.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🔤</div>
                    <div class="empty-state-text">Text nodes will appear here after parsing</div>
                </div>
            `;
        }
    }

    /**
     * Show status message in header (NEW v0.1.6 location)
     */
    showStatus(type, message) {
        this.statusMessage.className = `status-message status-${type}`;
        this.statusMessage.textContent = message;
        this.statusMessage.style.display = 'block';

        // Auto-hide after 4 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                this.statusMessage.style.display = 'none';
            }, 4000);
        }
    }

    // ========================================
    // Existing Functionality (from v0.1.5)
    // ========================================

    /**
     * Run full flow: Load → Parse → Rebuild
     */
    async runFullFlow() {
        console.log('⚡ Starting full flow...');

        // Step 1: Load micro sample
        this.loadSample('micro');
        await this.delay(300);

        // Step 2: Parse
        await this.parseHtml();
        await this.delay(300);

        // Step 3: Rebuild
        await this.rebuildHtml();

        console.log('✅ Full flow complete!');
    }

    /**
     * Helper: delay function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Update character count
     */
    updateCharCount() {
        const count = this.htmlInput.value.length;
        this.charCount.textContent = count.toLocaleString();

        // NEW v0.1.6: If in view mode, update syntax highlighting
        if (this.state.column1Mode === 'view') {
            this.updateSyntaxHighlighting();
        }
    }

    /**
     * Load sample HTML
     */
    loadSample(sampleName) {
        console.log(`📄 Loading sample: ${sampleName}`);

        if (!sampleName || sampleName === 'custom') {
            return;
        }

        const sample = Samples[sampleName];
        if (sample) {
            this.htmlInput.value = sample;
            this.sampleSelector.value = sampleName;
            this.updateCharCount();
            console.log(`✅ Sample loaded: ${sample.length} characters`);

            // NEW v0.1.6: If in view mode, update syntax highlighting
            if (this.state.column1Mode === 'view') {
                this.updateSyntaxHighlighting();
            }
        } else {
            console.error(`❌ Sample not found: ${sampleName}`);
        }
    }

    /**
     * Clear input
     */
    clearInput() {
        this.htmlInput.value = '';
        this.updateCharCount();
        this.sampleSelector.value = 'custom';

        // NEW v0.1.6: If in view mode, update syntax highlighting
        if (this.state.column1Mode === 'view') {
            this.updateSyntaxHighlighting();
        }
    }

    /**
     * Parse HTML → Dict + Hashes
     * Using the combined endpoint that returns both in the correct format
     */
    async parseHtml() {
        const html = this.htmlInput.value.trim();

        console.log('🔍 Parse requested...');

        if (!html) {
            this.showStatus('error', 'Please enter some HTML to parse');
            console.warn('⚠️ No HTML to parse');
            return;
        }

        this.showStatus('loading', 'Parsing HTML...');
        console.log(`📤 Sending ${html.length} characters to API...`);

        try {
            // Use the combined endpoint that returns dict with hashes + hash_mapping
            console.log('🌐 Calling combined dict/hashes endpoint...');

            const url = '/html/to/dict/hashes';
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    html: html,
                    max_depth: 256
                })
            });

            console.log(`   Response status: ${response.status}`);

            if (!response.ok) {
                const errorText = await response.text();
                console.error(`   Error: ${errorText}`);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const result = await response.json();
            console.log('📥 API response received:', result);

            // Extract the data
            this.state.currentDict = result.html_dict;
            this.state.currentHashes = result.hash_mapping;

            console.log('Extracted dict:', this.state.currentDict);
            console.log('Extracted hash_mapping:', this.state.currentHashes);

            // NEW v0.1.6: Check if in edit mode and populate textareas
            if (this.state.column2Mode === 'edit') {
                this.populateMiddleEdit();
            } else {
                // Display results with syntax highlighting in view mode
                this.renderMiddleView();
            }

            this.showStatus('success', 'HTML parsed successfully!');
            console.log('✅ Parse complete!');

        } catch (error) {
            this.showStatus('error', `Parse failed: ${error.message}`);
            console.error('❌ Parse error:', error);
        }
    }

    /**
     * Rebuild HTML from Dict + Hashes
     */
    async rebuildHtml() {
        console.log('🔧 Rebuild requested...');

        // NEW v0.1.6: If in edit mode, parse JSON first
        if (this.state.column2Mode === 'edit') {
            if (!this.parseMiddleEdit()) {
                console.warn('⚠️ Invalid JSON, aborting rebuild');
                return; // Invalid JSON, don't proceed
            }
        }

        if (!this.state.currentDict || !this.state.currentHashes) {
            this.showStatus('error', 'Please parse HTML first to generate Dict and Hashes');
            console.warn('⚠️ No Dict/Hashes available');
            return;
        }

        this.showStatus('loading', 'Rebuilding HTML...');
        console.log('📤 Sending Dict + Hashes to API...');

        try {
            // Call the reconstruction endpoint
            const payload = {
                html_dict: this.state.currentDict,
                hash_mapping: this.state.currentHashes
            };

            console.log('🌐 Calling reconstruction endpoint...');
            console.log('   Payload:', payload);

            const url = '/hashes/to/html';
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            console.log(`   Response status: ${response.status}`);

            if (!response.ok) {
                const errorText = await response.text();
                console.error(`   Error: ${errorText}`);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            // The response is HTML text, not JSON!
            const htmlResult = await response.text();
            console.log('📥 Rebuild response received (HTML):', htmlResult.substring(0, 100) + '...');

            // Store result
            this.state.currentCreatedHtml = htmlResult;

            // Display result with syntax highlighting
            this.createdHtmlOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(htmlResult, 'html')}</pre>`;

            this.showStatus('success', 'HTML rebuilt successfully!');
            console.log('✅ Rebuild complete!');

        } catch (error) {
            this.showStatus('error', `Rebuild failed: ${error.message}`);
            console.error('❌ Rebuild error:', error);
        }
    }

    /**
     * Copy output to clipboard
     */
    async copyOutput() {
        if (!this.state.currentCreatedHtml) {
            this.showStatus('error', 'No output to copy');
            return;
        }

        try {
            await navigator.clipboard.writeText(this.state.currentCreatedHtml);
            this.showStatus('success', 'Copied to clipboard!');
        } catch (error) {
            this.showStatus('error', 'Failed to copy to clipboard');
            console.error('Copy error:', error);
        }
    }

    /**
     * Download output as HTML file
     */
    downloadOutput() {
        if (!this.state.currentCreatedHtml) {
            this.showStatus('error', 'No output to download');
            return;
        }

        const blob = new Blob([this.state.currentCreatedHtml], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reconstructed.html';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showStatus('success', 'Download started!');
    }
}

// Register the Web Component
customElements.define('playground-controller', PlaygroundController);

console.log('✅ PlaygroundController component registered (v0.1.6)');