class LoadingButton extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _text = this.getAttribute('text') || " ";

        this.innerHTML = `
            <button id="${_id}" name="${_name}" class="${_class}" disabled style="padding: 10px; margin: 0px; display: flex; align-items: center; gap: 10px; min-width: 100px; color: white; background-color: #8B8B8D; font-size: 12px; font-weight: bold; border: 0px; border-radius: 5px;">
                <div style="width: 7px;  height: 7px; border: 2px solid #f3f3f3; border-radius: 50%; border-top: 2px solid #8B8B8D; animation: c-loading-button-spin 2s linear infinite;"></div>
                <span class="button-text">${_text}</span>
            </button>
        `;
    }

}

window.customElements.define('c-loading-button', LoadingButton)

const style = document.createElement('style');
style.textContent = `
    @keyframes c-loading-button-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
