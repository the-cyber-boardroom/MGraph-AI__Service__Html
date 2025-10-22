/**
 * Sample Selector Component - v0.1.6
 * Dropdown for selecting HTML samples
 * 
 * Emits:
 *   sample-selected - { sampleName: string, sampleContent: string }
 */

import { Samples } from '../../../../v0.1.5/data/samples.js';

class SampleSelector extends HTMLElement {
    constructor() {
        super();
        console.log('📦 SampleSelector constructor');
    }

    connectedCallback() {
        this.render();
        this.attachListeners();
        this.loadStyles();
    }

    loadStyles() {
        if (!document.getElementById('sample-selector-styles')) {
            const link = document.createElement('link');
            link.id = 'sample-selector-styles';
            link.rel = 'stylesheet';
            link.href = '../v0.1.6/components/column-original/sample-selector/sample-selector.css';
            document.head.appendChild(link);
        }
    }

    render() {
        this.innerHTML = `
            <div class="sample-selector-container">
                <select id="sample-select" class="sample-select">
                    <option value="">-- Select a Sample --</option>
                    <option value="micro">Micro HTML (Minimal)</option>
                    <option value="simple">Simple HTML</option>
                    <option value="complex">Complex HTML (Deep Nesting)</option>
                    <option value="custom">Custom (Paste Your Own)</option>
                </select>
            </div>
        `;
    }

    attachListeners() {
        const select = this.querySelector('#sample-select');
        select?.addEventListener('change', (e) => {
            this.handleSampleChange(e.target.value);
        });
    }

    handleSampleChange(sampleName) {
        console.log(`📦 SampleSelector: Selected ${sampleName}`);
        
        if (!sampleName || sampleName === 'custom') {
            return;
        }

        const sampleContent = Samples[sampleName];
        if (sampleContent) {
            this.dispatchEvent(new CustomEvent('sample-selected', {
                detail: { 
                    sampleName,
                    sampleContent 
                },
                bubbles: true
            }));
        }
    }

    // Public API
    reset() {
        const select = this.querySelector('#sample-select');
        if (select) {
            select.value = 'custom';
        }
    }
}

customElements.define('sample-selector', SampleSelector);
console.log('✅ SampleSelector component registered');
