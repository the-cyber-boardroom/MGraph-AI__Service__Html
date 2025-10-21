/**
 * Playground Logic - v0.1.5
 * 3-Column Architecture: Original HTML | Layout & Content Objects | Created HTML
 */

// Import samples
import { Samples } from './samples.js';

// Import config from v0.1.3 (reuse)
import { Endpoints__Config } from '../../v0.1.3/js/config/Endpoints__Config.js';

// Import syntax highlighter from v0.1.4 (reuse)
import { Syntax__Highlighter } from '../../v0.1.4/js/utils/Syntax__Highlighter.js';

/**
 * Playground Controller
 */
class PlaygroundController {
    constructor() {
        // DOM Elements
        this.htmlInput = document.getElementById('html-input');
        this.sampleSelector = document.getElementById('sample-selector');
        this.charCount = document.getElementById('char-count');

        // Middle column outputs
        this.dictOutput = document.getElementById('dict-output');
        this.hashesOutput = document.getElementById('hashes-output');

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

        // State
        this.currentDict = null;
        this.currentHashes = null;
        this.currentCreatedHtml = null;

        // Load syntax highlighter styles
        Syntax__Highlighter.loadStyles();

        // Initialize
        this.init();
    }

    init() {
        console.log('🎮 Playground v0.1.5 initializing...');

        // Event Listeners
        this.htmlInput.addEventListener('input', () => this.updateCharCount());
        this.sampleSelector.addEventListener('change', (e) => this.loadSample(e.target.value));
        this.btnClearInput.addEventListener('click', () => this.clearInput());
        this.btnTransformParse.addEventListener('click', () => this.parseHtml());
        this.btnTransformRebuild.addEventListener('click', () => this.rebuildHtml());
        this.btnCopyOutput.addEventListener('click', () => this.copyOutput());
        this.btnDownloadOutput.addEventListener('click', () => this.downloadOutput());

        // Debug button listeners
        this.debugLoadMicro.addEventListener('click', () => this.loadSample('micro'));
        this.debugLoadSimple.addEventListener('click', () => this.loadSample('simple'));
        this.debugParse.addEventListener('click', () => this.parseHtml());
        this.debugRebuild.addEventListener('click', () => this.rebuildHtml());
        this.debugFullFlow.addEventListener('click', () => this.runFullFlow());

        console.log('✅ Event listeners attached');

        // Auto-run full flow on load
        console.log('🚀 Running auto-flow: Load Micro → Parse → Rebuild');
        setTimeout(() => {
            this.runFullFlow();
        }, 500);
    }

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
    }

    /**
     * Parse HTML → Dict + Hashes
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
            // Call both endpoints in parallel
            console.log('🌐 Calling API endpoints...');
            const [dictResult, hashesResult] = await Promise.all([
                this.callEndpoint('html_to_dict', html),
                this.callEndpoint('html_to_text_nodes', html)
            ]);

            console.log('📥 API responses received');
            console.log('Dict result:', dictResult);
            console.log('Hashes result:', hashesResult);

            // Store results
            this.currentDict = dictResult;
            this.currentHashes = hashesResult;

            // Display results with syntax highlighting
            this.dictOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(dictResult, 'json')}</pre>`;
            this.hashesOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(hashesResult, 'json')}</pre>`;

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

        if (!this.currentDict || !this.currentHashes) {
            this.showStatus('error', 'Please parse HTML first to generate Dict and Hashes');
            console.warn('⚠️ No Dict/Hashes available');
            return;
        }

        this.showStatus('loading', 'Rebuilding HTML...');
        console.log('📤 Sending Dict + Hashes to API...');

        try {
            // Call the reconstruction endpoint
            const payload = {
                html_dict: this.currentDict,
                text_nodes: this.currentHashes
            };

            console.log('🌐 Calling reconstruction endpoint...');
            const result = await this.callEndpoint('dict_and_nodes_to_html', payload);

            console.log('📥 Rebuild response received:', result);

            // Store result
            this.currentCreatedHtml = result.html || result;

            // Display result with syntax highlighting
            this.createdHtmlOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.currentCreatedHtml, 'html')}</pre>`;

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
        if (!this.currentCreatedHtml) {
            this.showStatus('error', 'No output to copy');
            return;
        }

        try {
            await navigator.clipboard.writeText(this.currentCreatedHtml);
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
        if (!this.currentCreatedHtml) {
            this.showStatus('error', 'No output to download');
            return;
        }

        const blob = new Blob([this.currentCreatedHtml], { type: 'text/html' });
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

    /**
     * Show status message
     */
    showStatus(type, message) {
        this.statusMessage.className = `status-message status-${type}`;
        this.statusMessage.textContent = message;
        this.statusMessage.style.display = 'block';

        // Auto-hide after 3 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                this.statusMessage.style.display = 'none';
            }, 3000);
        }
    }

    /**
     * Call API endpoint
     */
    async callEndpoint(endpointKey, payload) {
        console.log(`🌐 API Call: ${endpointKey}`);

        const endpoint = Endpoints__Config.endpoints[endpointKey];

        if (!endpoint) {
            console.error(`❌ Endpoint not found: ${endpointKey}`);
            throw new Error(`Endpoint "${endpointKey}" not found`);
        }

        const url = endpoint.url;
        const method = endpoint.method || 'POST';

        console.log(`   URL: ${url}`);
        console.log(`   Method: ${method}`);

        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (method === 'POST') {
            // Determine payload format based on endpoint
            if (endpointKey === 'dict_and_nodes_to_html') {
                options.body = JSON.stringify(payload);
            } else {
                options.body = JSON.stringify({ html: payload });
            }
            console.log(`   Payload size: ${options.body.length} bytes`);
        }

        console.log('   Sending request...');
        const response = await fetch(url, options);

        console.log(`   Response status: ${response.status}`);

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`   Error: ${errorText}`);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        const result = await response.json();
        console.log(`   ✅ Success!`);

        return result;
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new PlaygroundController();
});