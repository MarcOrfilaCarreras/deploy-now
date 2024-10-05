class Card extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _title = this.getAttribute('title') || " ";
        const _description = this.getAttribute('description') || " ";
        const _action = this.getAttribute('action') || " ";
        const _onclick = this.getAttribute('onclick') || " ";

        if (!customElements.get('c-title')) {
            import('/static/_/js/components/title.js');
        }

        if (!customElements.get("c-primary-button")) {
            import("/static/_/js/components/buttons/primary.js");
        }

        this.innerHTML = `
            <div id="${_id}" name="${_name}" class="${_class}" style="padding: 10px; margin: 0px; max-width: 1500px; background-color: white; border: 1px solid rgba(24, 24, 27, 0.1); border-radius: 5px;">
                <c-title type="h3" text="${_title}"></c-title>
                <p>${_description}</p>
                <c-primary-button text="${_action}" onclick="${_onclick}"/>
            </div>
        `;
    }
}

window.customElements.define('c-card', Card);
