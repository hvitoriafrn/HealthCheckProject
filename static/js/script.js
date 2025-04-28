
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

