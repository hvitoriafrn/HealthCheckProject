// User Profile editing functionality
function toggleEdit(fieldId) {
    const inputField = document.getElementById(fieldId);
    const buttonContainer = inputField.closest('.field-item').querySelector('.button-container');
    const editButton = buttonContainer.querySelector('.edit-btn');
    const saveButton = buttonContainer.querySelector('.save-btn');
    const cancelButton = buttonContainer.querySelector('.cancel-btn');


    // Enable editing
    if (fieldId === "team") {
        inputField.removeAttribute("disabled");
        inputField.style.borderColor = "blue";
    } else {
        inputField.removeAttribute("readonly");
        inputField.style.borderColor = "blue";
    }
    inputField.focus();
    editButton.style.display = "none";
    saveButton.style.display = "inline-block";
    cancelButton.style.display = "inline-block";
}

function saveField(fieldId) {
    const inputField = document.getElementById(fieldId);
    const buttonContainer = inputField.closest('.field-item').querySelector('.button-container');
    const editButton = buttonContainer.querySelector('.edit-btn');
    const saveButton = buttonContainer.querySelector('.save-btn');
    const cancelButton = buttonContainer.querySelector('.cancel-btn');
    // Save changes to the database
    const newValue = inputField.value;

    fetch(`/update-profile/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ field: fieldId, value: newValue }),
    })
        .then((response) => {
            if (response.ok) {
                // Update the placeholder and reset the field
                inputField.setAttribute("placeholder", newValue);
                if (fieldId === "team") {
                    inputField.setAttribute("disabled", true); // Disable dropdown
                } else {
                    inputField.setAttribute("readonly", true); // Make the field readonly again
                }
                inputField.style.borderColor = "black"; // Reset border color

                // Restore button visibility
                editButton.style.display = "inline-block"; // Show the Edit button
                saveButton.style.display = "none"; // Hide the Save button
                cancelButton.style.display = "none"; // Hide the Cancel button
            } else {
                alert("Failed to update. Please try again.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
}

function cancelEdit(fieldId) {
    const inputField = document.getElementById(fieldId);
    const buttonContainer = inputField.closest('.field-item').querySelector('.button-container');
    const editButton = buttonContainer.querySelector('.edit-btn');
    const saveButton = buttonContainer.querySelector('.save-btn');
    const cancelButton = buttonContainer.querySelector('.cancel-btn');
    
    // Revert changes
    inputField.value = inputField.getAttribute("placeholder");
    inputField.setAttribute("readonly", true);
    inputField.style.borderColor = "blue"; 
    editButton.style.display = "inline-block"; // Show the "Edit" button
    saveButton.style.display = "none"; // Hide the "Save" button
    cancelButton.style.display = "none"; // Hide the "Cancel" button
}

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

function toggleTrends(display) {
    const trendColumns = document.querySelectorAll('.trend-column');

    trendColumns.forEach(column => {
        column.style.display = display ? 'table-cell' : 'none';
    });
}

function changeSession() {
    const selectedSession = document.getElementById('session-dropdown').value;

    
    fetch(`/team-summary/?session=${selectedSession}`)
        .then(response => response.json())
        .then(data => {
            // Update the circles dynamically
            const circlesRow = document.querySelector('.circles-row');
            circlesRow.innerHTML = ''; // Clear existing circles

            data.voting_data.forEach(vote => {
                const circle = `
                    <div class="circle-container">
                        <div class="circle ${vote.current_vote} ${vote.trend}"></div>
                    </div>
                `;
                circlesRow.innerHTML += circle;
            });
        })
        .catch(error => console.error('Error fetching session data:', error));
}