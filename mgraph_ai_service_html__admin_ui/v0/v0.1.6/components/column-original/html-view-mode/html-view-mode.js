/**
 * HTML View Mode Component - v0.1.6
 * View mode with syntax highlighting
 */

import { Syntax__Highlighter } from '../../../../v0.1.4/js/utils/Syntax__Highlighter.js';

class HtmlViewMode extends HTMLElement {
    constructor() {
        super();
        console.log('👁️ HtmlViewMode constructor');
        this.htmlContent = '';
        this.templateLoaded = false;
    }

    async connectedCallback() {
        await this.loadTemplate();
        this.loadStyles();
        this.render();
    }

    async loadTemplate() {
        try {
            const response = await fetch('../v0.1.6/components/column-original/html-view-mode/html-view-mode.html');
            const html = await response.text();
            this.innerHTML = html;
            this.templateLoaded = true;
            console.log('👁️ HtmlViewMode: Template loaded');
        } catch (error) {
            console.error('👁️ HtmlViewMode: Failed to load template', error);
            this.innerHTML = '<div class="error">Failed to load view mode</div>';
        }
    }

    loadStyles() {
        if (!document.getElementById('html-view-mode-styles')) {
            const link = document.createElement('link');
            link.id = 'html-view-mode-styles';
            link.rel = 'stylesheet';
            link.href = '../v0.1.6/components/column-original/html-view-mode/html-view-mode.css';
            document.head.appendChild(link);
        }
    }

    render() {
        const output = this.querySelector('#syntax-output');
        if (!output) return;

        if (!this.htmlContent.trim()) {
            output.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">👁️</div>
                    <div class="empty-state-text">Syntax-highlighted HTML will appear here</div>
                </div>
            `;
            return;
        }

        const highlighted = Syntax__Highlighter.highlight(this.htmlContent, 'html');
        output.innerHTML = `<pre class="syntax-output">${highlighted}</pre>`;
        console.log('👁️ HtmlViewMode: Syntax highlighting applied');
    }

    // Public API
    setHtml(html) {
        this.htmlContent = html;
        if (this.templateLoaded) {
            this.render();
        }
    }

    getHtml() {
        return this.htmlContent;
    }

    clear() {
        this.htmlContent = '';
        this.render();
    }
}

customElements.define('html-view-mode', HtmlViewMode);
console.log('✅ HtmlViewMode component registered');
