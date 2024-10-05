const API_VERSION = "v1";
const BASE_API_URL = `/api/${API_VERSION}`;

function capitalizeFirstLetter(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

function launchContainer(id) {
    const containerEndpoint = `/app/${id}`;

    if (window.event.target.nodeName === "DIV" || window.event.target.nodeName === "P") {
        return
    }

    window.open(containerEndpoint);
}

function startContainer(id) {
    const containerEndpoint = `${BASE_API_URL}/containers/${id}`;

    if (window.event.target.nodeName === "DIV" || window.event.target.nodeName === "P") {
        return
    }

    if (!customElements.get("c-loading-button")) {
        import("/static/_/js/components/buttons/loading.js");
    }

    if (!customElements.get("c-loading-button")) {
        import("/static/_/js/components/buttons/loading.js");
    }

    const loadingButton = document.createElement('c-loading-button');
    loadingButton.setAttribute('text', "Please wait")

    window.event.target.parentElement.replaceWith(loadingButton);

    window.fetch(containerEndpoint, {
        method: 'PATCH',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            state: "running"
        })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to update container ${id}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.status != "success") {
                throw new Error(`Failed to fetch containers data`);
            }

            const launchButton = document.createElement('c-primary-button');
            launchButton.setAttribute('text', 'Launch');
            launchButton.setAttribute('onclick', `launchContainer('${id}')`);

            loadingButton.replaceWith(launchButton);
        })
        .catch((error) => {
            console.error('Error updating the container:', error);
        });
}

function loadContainers() {
    const containersEndpoint = `${BASE_API_URL}/containers`;
    const containersDivId = "containers";

    if (!customElements.get("c-card")) {
        import("/static/_/js/components/card.js");
    }

    window.fetch(containersEndpoint)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch containers data`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.status != "success") {
                throw new Error(`Failed to fetch containers data`);
            }

            const containersDiv = document.getElementById(containersDivId);

            if (!containersDiv) {
                console.error(`Element with id "${containersDivId}" not found.`);
                return;
            }

            containersDiv.innerHTML = '';

            const containers = Array.isArray(data) ? data : data.containers;

            containers.forEach(container => {
                const containerCard = document.createElement("c-card");
                containerCard.setAttribute('title', capitalizeFirstLetter(container.name));
                containerCard.setAttribute('description', container.description);

                if (container.state === "running") {
                    containerCard.setAttribute('action', 'Launch');
                    containerCard.setAttribute('onclick', `launchContainer('${container.id}')`);
                } else {
                    containerCard.setAttribute('action', 'Start');
                    containerCard.setAttribute('onclick', `startContainer('${container.id}')`);
                }

                containersDiv.appendChild(containerCard);
            });
        })
        .catch((error) => {
            console.error('Error fetching and rendering containers:', error);
        });
}
