/**
 * HTML Edit Mode Component - v0.1.6
 * Edit mode with textarea and character count
 * 
 * Emits:
 *   html-changed - { html: string }
 */

class HtmlEditMode extends HTMLElement {
    constructor() {
        super();
        console.log('✏️ HtmlEditMode constructor');
        this.htmlContent = '';
        this.templateLoaded = false;
    }

    async connectedCallback() {
        await this.loadTemplate();
        this.attachListeners();
        this.loadStyles();
        this.updateCharCount();
    }

    async loadTemplate() {
        try {
            const response = await fetch('../v0.1.6/components/column-original/html-edit-mode/html-edit-mode.html');
            const html = await response.text();
            this.innerHTML = html;
            this.templateLoaded = true;
            console.log('✏️ HtmlEditMode: Template loaded');
        } catch (error) {
            console.error('✏️ HtmlEditMode: Failed to load template', error);
            this.innerHTML = '<div class="error">Failed to load edit mode</div>';
        }
    }

    loadStyles() {
        if (!document.getElementById('html-edit-mode-styles')) {
            const link = document.createElement('link');
            link.id = 'html-edit-mode-styles';
            link.rel = 'stylesheet';
            link.href = '../v0.1.6/components/column-original/html-edit-mode/html-edit-mode.css';
            document.head.appendChild(link);
        }
    }

    attachListeners() {
        const textarea = this.querySelector('#html-textarea');
        textarea?.addEventListener('input', () => {
            this.htmlContent = textarea.value;
            this.updateCharCount();
            this.emitHtmlChanged();
        });
    }

    updateCharCount() {
        const charCount = this.querySelector('#char-count');
        if (charCount) {
            charCount.textContent = this.htmlContent.length.toLocaleString();
        }
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
        const textarea = this.querySelector('#html-textarea');
        if (textarea) {
            textarea.value = html;
        }
        this.updateCharCount();
    }

    clear() {
        this.setHtml('');
    }
}

customElements.define('html-edit-mode', HtmlEditMode);
console.log('✅ HtmlEditMode component registered');
