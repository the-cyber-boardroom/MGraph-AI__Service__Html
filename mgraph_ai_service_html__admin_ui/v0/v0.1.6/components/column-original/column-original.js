/**
 * Column Original Component - v0.1.6 (Refactored)
 * Orchestrates: column-header, sample-selector, html-edit-mode, html-view-mode
 * 
 * Emits:
 *   html-changed - { html: string }
 *   clear-requested - {}
 */

class ColumnOriginal extends HTMLElement {
    constructor() {
        super();
        console.log('📝 ColumnOriginal constructor (refactored)');
        this.mode = 'edit'; // 'edit' | 'view'
    }

    connectedCallback() {
        this.render();
        this.attachListeners();
        this.loadStyles();
    }

    loadStyles() {
        if (!document.getElementById('column-original-styles')) {
            const link = document.createElement('link');
            link.id = 'column-original-styles';
            link.rel = 'stylesheet';
            link.href = '../v0.1.6/components/column-original/column-original.css';
            document.head.appendChild(link);
        }
    }

    render() {
        this.innerHTML = `
            <div class="column" data-mode="${this.mode}">
                <column-header 
                    title="Original HTML"
                    icon="📝"
                    modes="edit,view"
                    active-mode="${this.mode}"
                    column-id="original"
                >
                    <button slot="actions" class="btn-small btn-danger" id="btn-clear">Clear</button>
                </column-header>

                <div class="column-content">
                    <sample-selector></sample-selector>
                    
                    <!-- Edit Mode -->
                    <div class="mode-container mode-edit" ${this.mode !== 'edit' ? 'style="display: none;"' : ''}>
                        <html-edit-mode></html-edit-mode>
                    </div>

                    <!-- View Mode -->
                    <div class="mode-container mode-view" ${this.mode !== 'view' ? 'style="display: none;"' : ''}>
                        <html-view-mode></html-view-mode>
                    </div>
                </div>
            </div>
        `;
    }

    attachListeners() {
        // Listen to sample selection
        this.addEventListener('sample-selected', (e) => {
            const { sampleContent } = e.detail;
            this.setHtml(sampleContent);
        });

        // Listen to HTML changes from edit mode
        this.addEventListener('html-changed', (e) => {
            // Bubble up (already bubbling, but we could transform if needed)
            console.log('📝 ColumnOriginal: HTML changed');
        });

        // Listen to mode changes
        this.addEventListener('mode-selected', (e) => {
            if (e.detail.columnId === 'original') {
                this.switchMode(e.detail.mode);
            }
        });

        // Clear button
        const clearBtn = this.querySelector('#btn-clear');
        clearBtn?.addEventListener('click', () => {
            this.clear();
        });
    }

    switchMode(mode) {
        console.log(`📝 ColumnOriginal: Switching to ${mode} mode`);
        this.mode = mode;

        // Update column data-mode attribute
        const column = this.querySelector('.column');
        column.setAttribute('data-mode', mode);

        // Update header
        const header = this.querySelector('column-header');
        header?.setAttribute('active-mode', mode);

        // Show/hide mode containers
        const editContainer = this.querySelector('.mode-edit');
        const viewContainer = this.querySelector('.mode-view');

        if (mode === 'edit') {
            editContainer.style.display = '';
            viewContainer.style.display = 'none';
        } else {
            editContainer.style.display = 'none';
            viewContainer.style.display = '';
            
            // Sync content to view mode
            const editMode = this.querySelector('html-edit-mode');
            const viewMode = this.querySelector('html-view-mode');
            if (editMode && viewMode) {
                viewMode.setHtml(editMode.getHtml());
            }
        }
    }

    // Public API
    getHtml() {
        const editMode = this.querySelector('html-edit-mode');
        return editMode ? editMode.getHtml() : '';
    }

    setHtml(html) {
        const editMode = this.querySelector('html-edit-mode');
        const viewMode = this.querySelector('html-view-mode');
        
        if (editMode) {
            editMode.setHtml(html);
        }
        
        if (viewMode && this.mode === 'view') {
            viewMode.setHtml(html);
        }
    }

    clear() {
        console.log('📝 ColumnOriginal: Clearing');
        
        const editMode = this.querySelector('html-edit-mode');
        const viewMode = this.querySelector('html-view-mode');
        const sampleSelector = this.querySelector('sample-selector');
        
        if (editMode) editMode.clear();
        if (viewMode) viewMode.clear();
        if (sampleSelector) sampleSelector.reset();
        
        this.dispatchEvent(new CustomEvent('clear-requested', {
            bubbles: true
        }));
    }

    loadSample(sampleName) {
        const sampleSelector = this.querySelector('sample-selector');
        if (sampleSelector) {
            // Trigger the sample selector to load
            const select = sampleSelector.querySelector('#sample-select');
            if (select) {
                select.value = sampleName;
                select.dispatchEvent(new Event('change'));
            }
        }
    }
}

customElements.define('column-original', ColumnOriginal);
console.log('✅ ColumnOriginal component registered (refactored)');
