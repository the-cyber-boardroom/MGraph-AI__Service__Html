/**
 * Column Middle Component - v0.1.6
 * Layout & Content Objects (Dict + Hashes)
 * 
 * Emits:
 *   parse-requested - {}
 *   dict-changed - { dict: object }
 *   hashes-changed - { hashes: object }
 */

import { Syntax__Highlighter } from '../../../v0.1.4/js/utils/Syntax__Highlighter.js';

class ColumnMiddle extends HTMLElement {
    constructor() {
        super();
        console.log('🧩 ColumnMiddle constructor');
        this.mode = 'view'; // 'view' | 'edit'
        this.dict = null;
        this.hashes = null;
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
        link.href = '../v0.1.6/components/column-middle/column-middle.css';
        document.head.appendChild(link);
    }

    render() {
        this.innerHTML = `
            <div class="column middle-column" id="column-middle" data-mode="${this.mode}">
                <div class="column-header">
                    <h2>🧩 Layout & Content Objects</h2>

                    <mode-tabs 
                        modes="view,edit" 
                        active="${this.mode}"
                        column-id="middle"
                    ></mode-tabs>

                    <div class="column-actions">
                        <button class="btn-small btn-primary" id="btn-transform-parse">
                            ▶ Parse
                        </button>
                    </div>
                </div>

                <div class="column-content">
                    <!-- VIEW MODE (default - formatted display) -->
                    <div class="column-mode column-mode-view">
                        <!-- View 1: HTML Dict (Structure/Layout) -->
                        <div class="middle-view">
                            <div class="middle-view-header">
                                📐 HTML Dict (Structure/Layout)
                            </div>
                            <div class="middle-view-content" id="dict-output">
                                <div class="empty-state">
                                    <div class="empty-state-icon">📐</div>
                                    <div class="empty-state-text">HTML structure will appear here after parsing</div>
                                </div>
                            </div>
                        </div>

                        <!-- View 2: Text Nodes/Hashes (Content) -->
                        <div class="middle-view">
                            <div class="middle-view-header">
                                🔤 Text Nodes + Hashes (Content)
                            </div>
                            <div class="middle-view-content" id="hashes-output">
                                <div class="empty-state">
                                    <div class="empty-state-icon">🔤</div>
                                    <div class="empty-state-text">Text nodes will appear here after parsing</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- EDIT MODE (raw JSON editing) -->
                    <div class="column-mode column-mode-edit" style="display: none;">
                        <div class="edit-area">
                            <div class="edit-section">
                                <div class="edit-section-header">
                                    📐 HTML Dict JSON (Raw)
                                </div>
                                <textarea
                                    id="dict-edit"
                                    class="edit-textarea"
                                    placeholder='{"tag": "html", "attrs": {...}, "nodes": [...]}'
                                    spellcheck="false"
                                ></textarea>
                            </div>

                            <div class="edit-section">
                                <div class="edit-section-header">
                                    🔤 Text Hashes JSON (Raw)
                                </div>
                                <textarea
                                    id="hashes-edit"
                                    class="edit-textarea"
                                    placeholder='{"hash1": "text content", "hash2": "more text"}'
                                    spellcheck="false"
                                ></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    attachListeners() {
        // Parse button
        const parseBtn = this.querySelector('#btn-transform-parse');
        parseBtn?.addEventListener('click', () => {
            this.dispatchEvent(new CustomEvent('parse-requested', {
                bubbles: true
            }));
        });

        // Mode change listener
        this.addEventListener('mode-selected', (e) => {
            if (e.detail.columnId === 'middle') {
                this.switchMode(e.detail.mode);
            }
        });

        // Edit textarea changes
        const dictEdit = this.querySelector('#dict-edit');
        dictEdit?.addEventListener('blur', () => {
            this.syncFromEdit();
        });

        const hashesEdit = this.querySelector('#hashes-edit');
        hashesEdit?.addEventListener('blur', () => {
            this.syncFromEdit();
        });
    }

    switchMode(mode) {
        console.log(`🧩 ColumnMiddle: Switching to ${mode} mode`);
        this.mode = mode;
        
        const column = this.querySelector('#column-middle');
        column.setAttribute('data-mode', mode);

        if (mode === 'edit') {
            this.populateEditMode();
        } else if (mode === 'view') {
            this.syncFromEdit();
        }
    }

    populateEditMode() {
        console.log('🧩 ColumnMiddle: Populating edit mode');
        
        const dictEdit = this.querySelector('#dict-edit');
        const hashesEdit = this.querySelector('#hashes-edit');

        if (dictEdit && this.dict) {
            dictEdit.value = JSON.stringify(this.dict, null, 2);
        }

        if (hashesEdit && this.hashes) {
            hashesEdit.value = JSON.stringify(this.hashes, null, 2);
        }
    }

    syncFromEdit() {
        console.log('🧩 ColumnMiddle: Syncing from edit mode');
        
        const dictEdit = this.querySelector('#dict-edit');
        const hashesEdit = this.querySelector('#hashes-edit');

        try {
            if (dictEdit?.value.trim()) {
                this.dict = JSON.parse(dictEdit.value);
            }

            if (hashesEdit?.value.trim()) {
                this.hashes = JSON.parse(hashesEdit.value);
            }

            this.renderViewMode();
            
            // Emit changes
            this.dispatchEvent(new CustomEvent('dict-changed', {
                detail: { dict: this.dict },
                bubbles: true
            }));
            
            this.dispatchEvent(new CustomEvent('hashes-changed', {
                detail: { hashes: this.hashes },
                bubbles: true
            }));

        } catch (e) {
            console.error('🧩 ColumnMiddle: Invalid JSON', e);
            // Don't update if invalid JSON
        }
    }

    renderViewMode() {
        console.log('🧩 ColumnMiddle: Rendering view mode');
        
        const dictOutput = this.querySelector('#dict-output');
        const hashesOutput = this.querySelector('#hashes-output');

        if (dictOutput) {
            if (this.dict) {
                dictOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.dict, 'json')}</pre>`;
            } else {
                dictOutput.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📐</div>
                        <div class="empty-state-text">HTML structure will appear here after parsing</div>
                    </div>
                `;
            }
        }

        if (hashesOutput) {
            if (this.hashes) {
                hashesOutput.innerHTML = `<pre class="syntax-output">${Syntax__Highlighter.highlight(this.hashes, 'json')}</pre>`;
            } else {
                hashesOutput.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🔤</div>
                        <div class="empty-state-text">Text nodes will appear here after parsing</div>
                    </div>
                `;
            }
        }
    }

    // Public API
    setData(dict, hashes) {
        console.log('🧩 ColumnMiddle: Setting data', dict, hashes);
        this.dict = dict;
        this.hashes = hashes;
        
        if (this.mode === 'view') {
            this.renderViewMode();
        } else {
            this.populateEditMode();
        }
    }

    getData() {
        // If in edit mode, sync first
        if (this.mode === 'edit') {
            this.syncFromEdit();
        }
        return {
            dict: this.dict,
            hashes: this.hashes
        };
    }
}

customElements.define('column-middle', ColumnMiddle);
console.log('✅ ColumnMiddle component registered');
