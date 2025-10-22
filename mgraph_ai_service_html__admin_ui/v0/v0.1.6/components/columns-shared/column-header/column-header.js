/**
 * Column Header Component - v0.1.6 (Fixed with ComponentUtils)
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

import { ComponentUtils } from '../../../utils/ComponentUtils.js';

class ColumnHeader extends HTMLElement {
    // Static configuration
    static STYLE_ID = 'column-header-styles';
    static STYLE_PATH = '../v0.1.6/components/column-original/column-header/column-header.css';

    constructor() {
        super();
        console.log('📋 ColumnHeader constructor');
    }

    connectedCallback() {
        ComponentUtils.loadStyles(ColumnHeader.STYLE_ID, ColumnHeader.STYLE_PATH);
        this.render();
    }

    render() {
        const title = this.getAttribute('title') || 'Column';
        const icon = this.getAttribute('icon') || '📋';
        const modes = this.getAttribute('modes') || '';
        const activeMode = this.getAttribute('active-mode') || 'edit';
        const columnId = this.getAttribute('column-id') || '';

        // Check if we already have the structure (to preserve slots)
        let headerDiv = ComponentUtils.$(this, '.column-header');

        if (!headerDiv) {
            // First render - create structure
            headerDiv = document.createElement('div');
            headerDiv.className = 'column-header';

            // Create title
            const h2 = document.createElement('h2');
            h2.innerHTML = `${icon} ${title}`;
            headerDiv.appendChild(h2);

            // Create mode tabs if modes specified
            if (modes) {
                const modeTabs = document.createElement('mode-tabs');
                ComponentUtils.setAttributes(modeTabs, {
                    'modes': modes,
                    'active': activeMode,
                    'column-id': columnId
                });
                headerDiv.appendChild(modeTabs);
            }

            // Create actions container with slot
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'column-actions';
            const slot = document.createElement('slot');
            slot.setAttribute('name', 'actions');
            actionsDiv.appendChild(slot);
            headerDiv.appendChild(actionsDiv);

            this.appendChild(headerDiv);
        } else {
            // Update existing structure
            const h2 = ComponentUtils.$(headerDiv, 'h2');
            if (h2) {
                h2.innerHTML = `${icon} ${title}`;
            }

            const modeTabs = ComponentUtils.$(headerDiv, 'mode-tabs');
            if (modeTabs && modes) {
                ComponentUtils.setAttributes(modeTabs, {
                    'modes': modes,
                    'active': activeMode,
                    'column-id': columnId
                });
            }
        }
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
console.log('✅ ColumnHeader component registered (fixed slot preservation + ComponentUtils)');