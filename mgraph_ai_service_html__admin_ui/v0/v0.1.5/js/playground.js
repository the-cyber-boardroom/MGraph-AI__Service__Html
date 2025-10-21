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
        // Event Listeners
        this.htmlInput.addEventListener('input', () => this.updateCharCount());
        this.sampleSelector.addEventListener('change', (e) => this.loadSample(e.target.value));
        this.btnClearInput.addEventListener('click', () => this.clearInput());
        this.btnTransformParse.addEventListener('click', () => this.parseHtml());
        this.btnTransformRebuild.addEventListener('click', () => this.rebuildHtml());
        this.btnCopyOutput.addEventListener('click', () => this.copyOutput());
        this.btnDownloadOutput.addEventListener('click', () => this.downloadOutput());

        // Load micro sample by default
        this.loadSample('micro');
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
        if (!sampleName || sampleName === 'custom') {
            return;
        }

        const sample = Samples[sampleName];
        if (sample) {
            this.htmlInput.value = sample;
            this.updateCharCount();
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

        if (!html) {
            this.showStatus('error', 'Please enter some HTML to parse');
            return;
        }

        this.showStatus('loading', 'Parsing HTML...');

        try {
            // Call both endpoints in parallel
            const [dictResult, hashesResult] = await Promise.all([
                this.callEndpoint('html_to_dict', html),
                this.callEndpoint('html_to_text_nodes', html)
            ]);

            // Store results
            this.currentDict = dictResult;
            this.currentHashes = hashesResult;

            // Display results with syntax highlighting
            this.dictOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(dictResult, 'json')}</pre>`;
            this.hashesOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(hashesResult, 'json')}</pre>`;

            this.showStatus('success', 'HTML parsed successfully!');

        } catch (error) {
            this.showStatus('error', `Parse failed: ${error.message}`);
            console.error('Parse error:', error);
        }
    }

    /**
     * Rebuild HTML from Dict + Hashes
     */
    async rebuildHtml() {
        if (!this.currentDict || !this.currentHashes) {
            this.showStatus('error', 'Please parse HTML first to generate Dict and Hashes');
            return;
        }

        this.showStatus('loading', 'Rebuilding HTML...');

        try {
            // Call the reconstruction endpoint
            const payload = {
                html_dict: this.currentDict,
                text_nodes: this.currentHashes
            };

            const result = await this.callEndpoint('dict_and_nodes_to_html', payload);

            // Store result
            this.currentCreatedHtml = result.html || result;

            // Display result with syntax highlighting
            this.createdHtmlOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.currentCreatedHtml, 'html')}</pre>`;

            this.showStatus('success', 'HTML rebuilt successfully!');

        } catch (error) {
            this.showStatus('error', `Rebuild failed: ${error.message}`);
            console.error('Rebuild error:', error);
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
        const endpoint = Endpoints__Config.endpoints[endpointKey];

        if (!endpoint) {
            throw new Error(`Endpoint "${endpointKey}" not found`);
        }

        const url = endpoint.url;
        const method = endpoint.method || 'POST';

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
        }

        const response = await fetch(url, options);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        return await response.json();
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new PlaygroundController();
});