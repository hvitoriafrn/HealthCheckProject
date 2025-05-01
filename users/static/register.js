// This was created by H Vitoria Almeida Franca, w1938811

// Javascript for the 'register' page


//waits until the document the document has been fully loaded
    document.addEventListener("DOMContentLoaded", function () {

        const form = document.querySelector("form");
        //selects all the inputs and the "select" (for role) on the page
        const fields = document.querySelectorAll("input, select");
        
        //get password 1 and 2 
        const password1 = document.getElementById("id_password1");
        const password2 = document.getElementById("id_password2");

        //
        const pw1Error = password1.parentElement.querySelector(".error-message");
        const pw2Error = password2.parentElement.querySelector(".error-message");

        //function to show the error 
        function showError(input, message) {
            const errorDiv= input.parentElement.querySelector(".error-message");
            input.classList.add("invalid");
            input.classList.remove("valid");

            if (errorDiv) {
                errorDiv.style.display = "block";
                errorDiv.textContent = message;
            }
        }

        //clears the error message
        function clearError(input) {
            const errorDiv = input.parentElement.querySelector(".error-message");
            input.classList.remove("invalid");
            input.classList.add("valid");
            if (errorDiv) {
                errorDiv.style.display = "none";
            }
        }

        //checks password 1 and that it is strong enough (length)
        function validatePassword1() {
            const value = password1.value;
            password1.classList.add("touched");

            //checks if the password has at least 8 characters and if not, shows the error
            if (value.length <8) {
                showError(password1, 
                    "Password must be at least 8 characters long")
            return;
            }

            //added this to also check for special characters and show the error accordingly
            const specialCharCheck = /[!@#$%^&*(),.?":{}|<>]/.test(value);
            if (!specialCharCheck) {
                showError(password1, "Password must include at least one special character")
            } else {
                clearError(password1);
            }
        }
        
        //check thas password2 matches password1!
        function validatePassword2(){
            const value1 =password1.value;
            const value2 =password2.value;

            // adds the 'touched' for styling
            password2.classList.add("touched");
            //ensure passwords match
            if (value1 && value2 && value1 !==value2) {
                showError(password2, "Passwords do not match")
            } else if (value2.length > 0) {
                clearError(password2);
            }
        }
        
        //do the validation in real time for better user experience 
        password1.addEventListener("input", () => {
            //call the functions
            validatePassword1();
            validatePassword2();
        });

        password2.addEventListener("input", validatePassword2);

        //loops through all the input fields
        fields.forEach(field => {
            //adds 'blur' event listener, to trigger when the user clicks anywhere that isnt a field
            field.addEventListener("blur", function () {
                //gets the parent element (<div>)
                const errorDiv = field.parentElement.querySelector(".error-message");
                
                // Skip password fields; handled by custom validation
                if (field.id === "id_password1" || field.id === "id_password2") return;
                // Mark as touched, makes it so it's easier to style, so if it's touched but nothing on it
                // then the red border and error message show up
                field.classList.add("touched");
    
                // Use HTML5 validation for the required fields and email format
                if (!field.checkValidity()) {
                    //checks if it's valid or not and if it isn't valid, removed the 'valid' (for styling too!)
                    field.classList.remove("valid");
                    field.classList.add("invalid");

                    //displays error message
                    if (errorDiv) {
                        errorDiv.style.display = "block";
                    }
                } else {
                    //if it's valid, it removes the 'invalid' (so it styles it as 'valid')
                    field.classList.remove("invalid");
                    field.classList.add("valid"); 

                    //and if it's valid, it hides the error message
                    if (errorDiv) {
                        errorDiv.style.display = "none";
                    }
                }
            });
        });

        // when submitting make everything show error if invalid
        form.addEventListener("submit", function (e) {
            fields.forEach(field => {
                field.classList.add("touched");

                if (!field.checkValidity()) {
                    showError(field, field.parentElement.querySelector(".error-message")?.textContent || "This field is required");
                }
            });

            validatePassword1();
            validatePassword2();
        });

    });


// creating a function to check if the passwords are matching or not 
//  while the user is inputting their password

//waits until the page is loaded
 document.addEventListener("DOMContentLoaded", function() {
    //gets the password fields
    const passw1 = document.getElementById("id_password1");
    const passw2 = document.getElementById("id_password2");
    
    //finds the error for password2
    const mistmatch= passw2.parentElement.querySelector(".error-message");
    
    //function to check if the passwords match
    function checkPasswords() {
        passw2.classList.add("touched"); //marks it as touched (styling)

        //if fields are empty, ignore and hide the styles and error
        if (!passw1.value || !passw2.value) {
            mistmatch.style.display="none";
            passw2.classList.remove("invalid","valid");
            return;
        }
        
        //checks if the passwords do not match 
        if (passw1.value !== passw2.value) {
            passw2.classList.add("touched"); //marks as touched for styling
            //if they don't match, it removes 'valid' and adds invalid (styling will show in red)
            if (passw1.value !== passw2.value) {
                passw2.classList.remove("valid");
                passw2.classList.add("invalid");
                mistmatch.style.display = "block"; //shows the error message
                mistmatch.textContent = "Passwords do not match"; //displays the message
            } else {
                //if they match, it removes the 'invalid' and marks it as valid (therefore making it green)
                passw2.classList.remove("invalid");
                passw2.classList.add("valid");
                mistmatch.style.display = "none";
            }
        }
    }
    
    //checks again everytime there's a change in any of the fields
    passw1.addEventListener("input", checkPasswords);
    passw2.addEventListener("input", checkPasswords);

});
              