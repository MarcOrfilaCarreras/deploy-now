class TextInput extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _placeholder = this.getAttribute('placeholder') || " ";
        const _onkeyup = this.getAttribute('onkeyup') || " ";

        this.innerHTML = `
            <input type="text" id="${_id}" name="${_name}" class="${_class}" placeholder="${_placeholder}" onkeyup="window.event.stopPropagation(); ${_onkeyup}" style="padding: 10px; margin: 0px; background-color: white; width: 100%; box-sizing: border-box; border: 1px solid rgba(24, 24, 27, 0.1); border-radius: 5px;"></input>
        `;
    }
}

window.customElements.define('c-text-input', TextInput);
