function cSearchInput (containerId, tag){
    let searchInput;

    if (window.event.target.tagName.toLowerCase() === 'input') {
        searchInput = window.event.target.value.toLowerCase();
    } else {
        const inputElement = window.event.currentTarget.parentElement.parentElement.querySelector('c-text-input').querySelector('input');
        searchInput = inputElement.value.toLowerCase();
    }

    const searchContainer = document.getElementById(containerId);
    const searchTags = searchContainer.querySelectorAll(tag || 'p, span, div');

    searchTags.forEach(tag => {
        const text = tag.textContent.toLowerCase();

        if (text.includes(searchInput)) {
            tag.style.display = "block";
        } else {
            tag.style.display = "none";
        }
    });
}

class SearchInput extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const _id = this.getAttribute('id') || " ";
        const _name = this.getAttribute('name') || " ";
        const _class = this.getAttribute('class') || " ";
        const _style = this.getAttribute('style') || " ";
        const _container_id = this.getAttribute('container-id') || " ";
        const _tag = this.getAttribute('tag') || " ";

        if (!customElements.get('c-text-input')) {
            import('/static/_/js/components/inputs/text.js');
        }

        if (!customElements.get("c-primary-button")) {
            import("/static/_/js/components/buttons/primary.js");
        }

        this.innerHTML = `
            <div id="${_id}" name="${_name}" class="${_class}" style="padding: 0px; margin: 0px; display: flex; flex-direction: row; gap: 10px; ${_style} ">
                <c-text-input style="flex: 1;" placeholder="Start typing ..." onkeyup="cSearchInput('${_container_id}', '${_tag}')"></c-text-input>
                <c-primary-button text="Search" onclick="cSearchInput('${_container_id}', '${_tag}')" />
            </div>
        `;
    }
}

window.customElements.define('c-search-input', SearchInput);
