// This page created by Pawel Krezel (W1837610) 


function exit(url){
    window.location.replace(url);
}
var questionsQty = document.getElementById("voting-card-body-2137").dataset.questionsQty;

function hideCard(ID){
    ID = parseInt(ID)
    document.getElementById("voting-card-body-"+ID.toString()).setAttribute("style", "display:none");
}

function showCard(ID){
    ID = parseInt(ID)
    document.getElementById("voting-card-body-"+ID.toString()).removeAttribute("style");
}

function navInit(){
    // this function is called as soon as the page loads and makes only the first voting card visible
    for (var question=2; question<=questionsQty; question++){
        hideCard(question);
    }
    // ID '2137' will be used for the summary card
    hideCard(2137);
}

// populate the final voting card with user's answers 
function renderSummary(){
    var questionPK;
    var radioValue;
    var commentValue = "";
    var questionContent;
    var HTMLcontainer = document.getElementById("content-summary-container");
    HTMLcontainer.innerHTML = ""; //resets html content in case user makes changes to the cards before submitting
    for(question=1; question<=questionsQty; question++){
        questionPK = document.getElementById("voting-card-body-"+question.toString()).dataset.pk;
        if (document.getElementById(questionPK+"-green").checked){
            radioValue = 'green';
        }
        else if(document.getElementById(questionPK+"-amber").checked){
            radioValue = 'amber';
        }
        else if(document.getElementById(questionPK+"-red").checked){
            radioValue = 'red';
        }
        else{
            radioValue = 'pending';
        }
        commentValue = document.getElementById(questionPK+"-comment").value.toString();
        questionContent = document.getElementById("header-question-content-"+questionPK).innerHTML;
        if (radioValue != 'pending'){
            radioValue = "<div class='circle circle-"+radioValue+"' title='"+radioValue+"'></div>"
        }
        else{
            radioValue = "<div class=' pending-alert' title='"+radioValue+"'>"+radioValue+"</div>"
        }
        
        HTMLcontainer.innerHTML += '<div class="summary-box" onclick="jumpToCard('+question+')"><h4 class="summary-question-title">'+questionContent+'</h4><span class="summary-traffic-light">&nbsp;'+radioValue+'</span><br><span class="summary-comment">'+commentValue+'</span></div>';
    }
}
function jumpToCard(cardID){
    hideCard(2137);
    showCard(cardID);
}

function nextQuestion(activeQuestion){
    activeQuestion = parseInt(activeQuestion)
    hideCard(activeQuestion);
    if (activeQuestion < questionsQty){
        showCard(activeQuestion+1);
    }
    else{
        showCard(2137);
        renderSummary();
    }
    
}

function previousQuestion(activeQuestion){
    activeQuestion = parseInt(activeQuestion)
    hideCard(activeQuestion);
    if (activeQuestion!=2137){
        showCard(activeQuestion-1);
    }
    else{
        showCard(questionsQty);
    }

}

function saveProgress(){
    window.alert("Progress for this session has been saved! You can now click the exit button without loosing any data");
}

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
