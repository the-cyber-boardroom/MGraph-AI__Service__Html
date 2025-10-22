/**
 * Column Original Component - v0.1.6
 * Original HTML input with Edit/View modes
 * 
 * Emits:
 *   html-changed - { html: string }
 *   clear-requested - {}
 *   sample-selected - { sample: string }
 */

import { Syntax__Highlighter } from '../../../v0.1.4/js/utils/Syntax__Highlighter.js';
import { Samples } from '../../../v0.1.5/data/samples.js';

class ColumnOriginal extends HTMLElement {
    constructor() {
        super();
        console.log('📝 ColumnOriginal constructor');
        this.mode = 'edit'; // 'edit' | 'view'
        this.htmlContent = '';
    }

    connectedCallback() {
        this.render();
        this.attachListeners();
        
        // Load CSS
        this.loadStyles();
    }

    loadStyles() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '../v0.1.6/components/column-original/column-original.css';
        document.head.appendChild(link);
    }

    render() {
        this.innerHTML = `
            <div class="column" id="column-original" data-mode="${this.mode}">
                <div class="column-header">
                    <h2>📝 Original HTML</h2>
                    
                    <mode-tabs 
                        modes="edit,view" 
                        active="${this.mode}"
                        column-id="original"
                    ></mode-tabs>
                    
                    <div class="column-actions">
                        <button class="btn-small btn-danger" id="btn-clear-input">Clear</button>
                    </div>
                </div>

                <div class="column-content">
                    <!-- EDIT MODE -->
                    <div class="column-mode column-mode-edit">
                        <div class="input-area">
                            <div class="input-controls">
                                <select id="sample-selector">
                                    <option value="">-- Select a Sample --</option>
                                    <option value="micro">Micro HTML (Minimal)</option>
                                    <option value="simple">Simple HTML</option>
                                    <option value="complex">Complex HTML (Deep Nesting)</option>
                                    <option value="custom">Custom (Paste Your Own)</option>
                                </select>
                            </div>

                            <textarea
                                id="html-input"
                                class="input-textarea"
                                placeholder="Paste your HTML here or select a sample above..."
                                spellcheck="false"
                            >${this.htmlContent}</textarea>

                            <div class="character-count">
                                <span id="char-count">0</span> characters
                            </div>
                        </div>
                    </div>

                    <!-- VIEW MODE -->
                    <div class="column-mode column-mode-view" style="display: none;">
                        <div class="view-area">
                            <div class="syntax-highlighted" id="html-view">
                                <div class="empty-state">
                                    <div class="empty-state-icon">👁️</div>
                                    <div class="empty-state-text">Syntax-highlighted HTML will appear here</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    attachListeners() {
        // HTML input changes
        const htmlInput = this.querySelector('#html-input');
        htmlInput?.addEventListener('input', () => {
            this.htmlContent = htmlInput.value;
            this.updateCharCount();
            this.emitHtmlChanged();
        });

        // Sample selector
        const sampleSelector = this.querySelector('#sample-selector');
        sampleSelector?.addEventListener('change', (e) => {
            this.loadSample(e.target.value);
        });

        // Clear button
        const clearBtn = this.querySelector('#btn-clear-input');
        clearBtn?.addEventListener('click', () => {
            this.clearInput();
        });

        // Mode change listener
        this.addEventListener('mode-selected', (e) => {
            if (e.detail.columnId === 'original') {
                this.switchMode(e.detail.mode);
            }
        });

        // Initial char count
        this.updateCharCount();
    }

    switchMode(mode) {
        console.log(`📝 ColumnOriginal: Switching to ${mode} mode`);
        this.mode = mode;
        
        const column = this.querySelector('#column-original');
        column.setAttribute('data-mode', mode);

        if (mode === 'view') {
            this.updateSyntaxHighlighting();
        }
    }

    updateCharCount() {
        const charCount = this.querySelector('#char-count');
        if (charCount) {
            charCount.textContent = this.htmlContent.length.toLocaleString();
        }
    }

    updateSyntaxHighlighting() {
        const htmlView = this.querySelector('#html-view');
        
        if (!this.htmlContent.trim()) {
            htmlView.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">👁️</div>
                    <div class="empty-state-text">Syntax-highlighted HTML will appear here</div>
                </div>
            `;
            return;
        }

        const highlighted = Syntax__Highlighter.highlight(this.htmlContent, 'html');
        htmlView.innerHTML = `<pre class="syntax-output">${highlighted}</pre>`;
        console.log('📝 ColumnOriginal: Syntax highlighting applied');
    }

    loadSample(sampleName) {
        console.log(`📝 ColumnOriginal: Loading sample ${sampleName}`);
        
        if (!sampleName || sampleName === 'custom') {
            return;
        }

        const sample = Samples[sampleName];
        if (sample) {
            this.htmlContent = sample;
            const htmlInput = this.querySelector('#html-input');
            if (htmlInput) {
                htmlInput.value = sample;
            }
            this.updateCharCount();
            
            // Update view mode if active
            if (this.mode === 'view') {
                this.updateSyntaxHighlighting();
            }
            
            this.emitHtmlChanged();
            
            this.dispatchEvent(new CustomEvent('sample-selected', {
                detail: { sample: sampleName },
                bubbles: true
            }));
        }
    }

    clearInput() {
        console.log('📝 ColumnOriginal: Clearing input');
        this.htmlContent = '';
        const htmlInput = this.querySelector('#html-input');
        if (htmlInput) {
            htmlInput.value = '';
        }
        const sampleSelector = this.querySelector('#sample-selector');
        if (sampleSelector) {
            sampleSelector.value = 'custom';
        }
        this.updateCharCount();
        
        // Update view mode if active
        if (this.mode === 'view') {
            this.updateSyntaxHighlighting();
        }
        
        this.emitHtmlChanged();
        
        this.dispatchEvent(new CustomEvent('clear-requested', {
            bubbles: true
        }));
    }

    emitHtmlChanged() {
        this.dispatchEvent(new CustomEvent('html-changed', {
            detail: { html: this.htmlContent },
            bubbles: true
        }));
    }

    // Public API
    getHtml() {
        return this.htmlContent;
    }

    setHtml(html) {
        this.htmlContent = html;
        const htmlInput = this.querySelector('#html-input');
        if (htmlInput) {
            htmlInput.value = html;
        }
        this.updateCharCount();
        if (this.mode === 'view') {
            this.updateSyntaxHighlighting();
        }
    }
}

customElements.define('column-original', ColumnOriginal);
console.log('✅ ColumnOriginal component registered');
