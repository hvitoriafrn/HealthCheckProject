
function exit(url){
    window.location.replace(url);
}
var questionsQty = document.getElementById("voting-card-body-2137").dataset.questionsQty;

function hideCard(ID){
    document.getElementById("voting-card-body-"+ID.toString()).setAttribute("style", "display:none");
}

function showCard(ID){
    document.getElementById("voting-card-body-"+ID.toString()).removeAttribute("style");
}

function navInit(){
    // this function is called as soon as the page loads and makes only the first voting card visible
    for (var question=2; question<=questionsQty; question++){
        hideCard(question);
    }
    // ID 2137 will be used for the summary card
    hideCard(2137);
}

function nextQuestion(activeQuestion){
    hideCard(activeQuestion);
    if (activeQuestion < questionsQty){
        showCard(activeQuestion+1);
    }
    else{
        showCard(2137);
    }
    
}

function previousQuestion(activeQuestion){
    hideCard(activeQuestion);
    if (activeQuestion!=2137){
        showCard(activeQuestion-1);
    }
    else{
        showCard(questionsQty);
    }

}
