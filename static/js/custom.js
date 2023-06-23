function loadAssignedUsers(projectId) {
    const assignedToContainer = document.querySelector("#assigned-to-container");
    const url = `/kanban/get_assigned_users/${projectId}/`;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            assignedToContainer.innerHTML = "";

            data.forEach((user) => {
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.name = "assigned_to";
                checkbox.value = user.id;
                checkbox.id = `user_${user.id}`;
                checkbox.style.transform = "scale(1.25)";

                const label = document.createElement("label");
                label.htmlFor = checkbox.id;
                label.textContent = user.username;
                label.style.fontSize = "1.25rem";
                label.style.paddingLeft = "0.25rem";

                const div = document.createElement("div");
                div.appendChild(checkbox);
                div.appendChild(label);
                div.style.paddingLeft = "0.75rem";

                assignedToContainer.appendChild(div);
            });
        });
}