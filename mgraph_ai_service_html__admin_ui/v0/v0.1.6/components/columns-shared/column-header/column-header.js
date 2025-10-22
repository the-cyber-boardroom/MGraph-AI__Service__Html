/**
 * Column Header Component - v0.1.6 (Shadow DOM + Smart Rendering)
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

import { ComponentUtils } from '../../../../v0.1.6/utils/ComponentUtils.js';

class ColumnHeader extends HTMLElement {
    // Static configuration
    static STYLE_ID = 'column-header-styles';
    static STYLE_PATH = '../v0.1.6/components/columns-shared/column-header/column-header.css';

    constructor() {
        super();
        console.log('📋 ColumnHeader constructor');

        // Create Shadow DOM
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        //ComponentUtils.loadStyles(ColumnHeader.STYLE_ID, ColumnHeader.STYLE_PATH);
        this.render();
    }

    render() {
        const title = this.getAttribute('title') || 'Column';
        const icon = this.getAttribute('icon') || '📋';
        const modes = this.getAttribute('modes') || '';
        const activeMode = this.getAttribute('active-mode') || 'edit';
        const columnId = this.getAttribute('column-id') || '';

        // Check if we already have the structure (to avoid re-creating everything)
        let headerDiv = this.shadowRoot.querySelector('.column-header');

        if (!headerDiv) {
            // First render - create structure

            // Add external CSS link
            const linkElem = document.createElement('link');
            linkElem.setAttribute('rel', 'stylesheet');
            linkElem.setAttribute('href', ColumnHeader.STYLE_PATH);
            this.shadowRoot.appendChild(linkElem);

            // Create header container
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

            this.shadowRoot.appendChild(headerDiv);

            console.log(`📋 ColumnHeader: First render complete for "${title}"`);
        } else {
            // Update existing structure (only what changed)
            const h2 = headerDiv.querySelector('h2');
            if (h2) {
                h2.innerHTML = `${icon} ${title}`;
            }

            const modeTabs = headerDiv.querySelector('mode-tabs');
            if (modeTabs && modes) {
                ComponentUtils.setAttributes(modeTabs, {
                    'modes': modes,
                    'active': activeMode,
                    'column-id': columnId
                });
            }

            console.log(`📋 ColumnHeader: Updated "${title}"`);
        }
    }

    static get observedAttributes() {
        return ['active-mode', 'title', 'icon'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this.render();
        }
    }
}

customElements.define('column-header', ColumnHeader);
console.log('✅ ColumnHeader component registered (Shadow DOM + External CSS + Smart Rendering)');