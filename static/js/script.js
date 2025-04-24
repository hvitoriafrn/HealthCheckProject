// User Profile editing functionality
function toggleEdit(fieldId) {
    const inputField = document.getElementById(fieldId);
    const editButton = inputField.nextElementSibling;
    const cancelButton = editButton.nextElementSibling;

    if (editButton.innerText === "Edit") {
        // Enable editing
        inputField.removeAttribute("readonly");
        inputField.focus();
        editButton.innerText = "Double Click to Save";
        cancelButton.style.display = "inline-block";
    } else if (editButton.innerText === "Double Click to Save") {
        // Save changes
        saveField(fieldId);
        inputField.setAttribute("readonly", true);
        editButton.innerText = "Edit";
        cancelButton.style.display = "none";
    }
}

function cancelEdit(fieldId) {
    const inputField = document.getElementById(fieldId);
    const editButton = inputField.nextElementSibling;
    const cancelButton = editButton.nextElementSibling;

    // Revert changes
    inputField.value = inputField.getAttribute("placeholder");
    inputField.setAttribute("readonly", true);
    editButton.innerText = "Edit";
    cancelButton.style.display = "none";
}

function saveField(fieldId) {
    const inputField = document.getElementById(fieldId);
    const newValue = inputField.value;

    // Send the updated value to the backend
    fetch(`/update-profile/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
        },
        body: JSON.stringify({ field: fieldId, value: newValue }),
    })
        .then((response) => {
            if (response.ok) {
                inputField.setAttribute("placeholder", newValue);
                alert("Changes saved successfully!");
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while saving changes.");
        });
}

function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        if (cookie.startsWith("csrftoken=")) {
            return cookie.split("=")[1];
        }
    }
    return "";
}