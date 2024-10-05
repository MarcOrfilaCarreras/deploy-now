class Title extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _text = this.getAttribute('text') || " ";
        const _type = this.getAttribute('type') || "h1";
        const _image = this.getAttribute('image') || null;

        const imgHtml = _image ? `<img src="${_image}" alt="${_text} image" style="margin-right: 10px; display: none;"/>` : "";

        this.innerHTML = `
            <div style="display: flex; align-items: center; margin: 0px;">
                ${imgHtml}
                <${_type} id="${_id}" name="${_name}" class="${_class}" style="margin: 0px; color: #18181b; font-weight: bold; text-align: center;">
                    ${_text}
                </${_type}>
            </div>
        `;

        if (! _image) {
            return
        }

        const img = this.querySelector('img');
        const textElement = this.querySelector(_type);

        img.onload = () => {
            const textHeight = textElement.offsetHeight;
            img.style.height = `${textHeight}px`;
            img.style.removeProperty("display");
        };
    }
}

window.customElements.define('c-title', Title);
