class PrimaryButton extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _text = this.getAttribute('text') || " ";
        const _onclick = this.getAttribute('onclick') || " ";

        this.innerHTML = `
            <button id="${_id}" name="${_name}" class="${_class}" onclick="window.event.stopPropagation(); ${_onclick}" style="padding: 10px; margin: 0px; min-width: 100px; color: white; background-color: #18181b; cursor: pointer; font-size: 12px; font-weight: bold; border: 0px; border-radius: 5px; ">${_text}</button>
        `;
    }

}

window.customElements.define('c-primary-button', PrimaryButton)
