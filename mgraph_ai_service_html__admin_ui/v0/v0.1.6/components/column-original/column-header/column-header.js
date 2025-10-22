/**
 * Column Header Component - v0.1.6
 * Reusable header for all columns
 * 
 * Attributes:
 *   title - Column title
 *   icon - Emoji icon
 *   modes - Comma-separated modes (e.g., "edit,view")
 *   active-mode - Currently active mode
 *   column-id - Identifier for events
 * 
 * Slots:
 *   actions - Buttons/actions on the right
 */

class ColumnHeader extends HTMLElement {
    constructor() {
        super();
        console.log('📋 ColumnHeader constructor');
    }

    connectedCallback() {
        this.render();
        this.loadStyles();
    }

    loadStyles() {
        if (!document.getElementById('column-header-styles')) {
            const link = document.createElement('link');
            link.id = 'column-header-styles';
            link.rel = 'stylesheet';
            link.href = '../v0.1.6/components/column-original/column-header/column-header.css';
            document.head.appendChild(link);
        }
    }

    render() {
        const title = this.getAttribute('title') || 'Column';
        const icon = this.getAttribute('icon') || '📋';
        const modes = this.getAttribute('modes') || '';
        const activeMode = this.getAttribute('active-mode') || 'edit';
        const columnId = this.getAttribute('column-id') || '';

        this.innerHTML = `
            <div class="column-header">
                <h2>${icon} ${title}</h2>
                
                ${modes ? `
                    <mode-tabs 
                        modes="${modes}" 
                        active="${activeMode}"
                        column-id="${columnId}"
                    ></mode-tabs>
                ` : ''}
                
                <div class="column-actions">
                    <slot name="actions"></slot>
                </div>
            </div>
        `;
    }

    static get observedAttributes() {
        return ['active-mode'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'active-mode' && oldValue !== newValue) {
            this.render();
        }
    }
}

customElements.define('column-header', ColumnHeader);
console.log('✅ ColumnHeader component registered');
