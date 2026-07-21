/* ==========================================
   RainSense AI
   Final Script.js
========================================== */

/* ==========================================
   DOM Elements
========================================== */

const form = document.getElementById("predictionForm");

const steps = document.querySelectorAll(".form-step");

const indicators = document.querySelectorAll(".step");

const progressBar = document.getElementById("progressBar");

const predictionDate = document.getElementById("predictionDate");

const yearInput = document.getElementById("year");
const monthInput = document.getElementById("month");
const dayInput = document.getElementById("day");
const seasonInput = document.getElementById("season");

/* ==========================================
   Buttons
========================================== */

const nextButtons = document.querySelectorAll("[id^='next']");

const previousButtons = document.querySelectorAll("[id^='prev']");

/* ==========================================
   State
========================================== */

let currentStep = 0;

const totalSteps = steps.length;

/* ==========================================
   Show Step
========================================== */

function showStep(index){

    steps.forEach(step=>{

        step.classList.remove("active");

    });

    steps[index].classList.add("active");

    updateProgress(index);

    updateIndicators(index);

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}

/* ==========================================
   Progress Bar
========================================== */

function updateProgress(index){

    const percentage=((index+1)/totalSteps)*100;

    progressBar.style.width=percentage+"%";

}

/* ==========================================
   Step Indicator
========================================== */

function updateIndicators(index){

    indicators.forEach((indicator,i)=>{

        indicator.classList.remove("active");

        indicator.classList.remove("completed");

        if(i<index){

            indicator.classList.add("completed");

        }

        if(i===index){

            indicator.classList.add("active");

        }

    });

}

/* ==========================================
   Next
========================================== */

function nextStep(){

    if(currentStep>=totalSteps-1){

        return;

    }

    currentStep++;

    showStep(currentStep);

}

/* ==========================================
   Previous
========================================== */

function previousStep(){

    if(currentStep<=0){

        return;

    }

    currentStep--;

    showStep(currentStep);

}
/* ==========================================
   Season Calculation
========================================== */

function getSeason(month){

    switch(month){

        case 12:
        case 1:
        case 2:
            return "Summer";

        case 3:
        case 4:
        case 5:
            return "Autumn";

        case 6:
        case 7:
        case 8:
            return "Winter";

        default:
            return "Spring";

    }

}

/* ==========================================
   Date Processing
========================================== */

if(predictionDate){

    predictionDate.addEventListener("change",function(){

        if(!this.value){

            return;

        }

        const date=new Date(this.value);

        const year=date.getFullYear();

        const month=date.getMonth()+1;

        const day=date.getDate();

        yearInput.value=year;

        monthInput.value=month;

        dayInput.value=day;

        seasonInput.value=getSeason(month);

    });

}

/* ==========================================
   Validation Helpers
========================================== */

function markValid(element){

    element.classList.remove("is-invalid");

    element.classList.add("is-valid");

}

function markInvalid(element){

    element.classList.remove("is-valid");

    element.classList.add("is-invalid");

}

function clearValidation(element){

    element.classList.remove("is-valid");

    element.classList.remove("is-invalid");

}

/* ==========================================
   Validate Required Fields
========================================== */

function validateRequiredFields(step){

    let isValid=true;

    const inputs=step.querySelectorAll("input,select");

    inputs.forEach(input=>{

        if(input.type==="hidden"){

            return;

        }

        if(input.disabled){

            return;

        }

        if(input.value.trim()===""){

            markInvalid(input);

            isValid=false;

        }

        else{

            markValid(input);

        }

    });

    return isValid;

}

/* ==========================================
   Validate Numeric Values
========================================== */

function validateNumericRanges(step){

    let valid=true;

    const numbers=step.querySelectorAll("input[type='number']");

    numbers.forEach(input=>{

        if(input.value===""){

            return;

        }

        const value=parseFloat(input.value);

        switch(input.name){

            case "Humidity9am":
            case "Humidity3pm":

                if(value<0 || value>100){

                    markInvalid(input);

                    valid=false;

                }

                break;

            case "Cloud9am":
            case "Cloud3pm":

                if(value<0 || value>8){

                    markInvalid(input);

                    valid=false;

                }

                break;

            case "Rainfall":
            case "Evaporation":
            case "Sunshine":
            case "WindGustSpeed":
            case "WindSpeed9am":
            case "WindSpeed3pm":

                if(value<0){

                    markInvalid(input);

                    valid=false;

                }

                break;

        }

    });

    return valid;

}

/* ==========================================
   Validate Current Step
========================================== */

function validateCurrentStep(){

    const currentSection=steps[currentStep];

    const requiredOk=validateRequiredFields(currentSection);

    const numericOk=validateNumericRanges(currentSection);

    if(!requiredOk){

        alert("Please fill all required fields.");

        return false;

    }

    if(!numericOk){

        alert("Please enter valid values.");

        return false;

    }

    return true;

}
/* ==========================================
   Navigation Events
========================================== */

nextButtons.forEach(button=>{

    button.addEventListener("click",function(e){

        e.preventDefault();

        if(validateCurrentStep()){

            nextStep();

        }

    });

});

previousButtons.forEach(button=>{

    button.addEventListener("click",function(e){

        e.preventDefault();

        previousStep();

    });

});

/* ==========================================
   Loading Animation
========================================== */

function startLoading(){

    const submitButton=form.querySelector("button[type='submit']");

    if(!submitButton){

        return;

    }

    submitButton.disabled=true;

    submitButton.classList.add("btn-loading");

    submitButton.innerHTML=`
        <span class="spinner-border spinner-border-sm"></span>
        Predicting...
    `;

}

/* ==========================================
   Restore Button
========================================== */

function stopLoading(){

    const submitButton=form.querySelector("button[type='submit']");

    if(!submitButton){

        return;

    }

    submitButton.disabled=false;

    submitButton.classList.remove("btn-loading");

    submitButton.innerHTML=`
        <i class="bi bi-magic me-2"></i>
        Predict Rainfall
    `;

}

/* ==========================================
   Form Submission
========================================== */

form.addEventListener("submit",function(e){

    if(!validateCurrentStep()){

        e.preventDefault();

        return;

    }

    startLoading();

});

/* ==========================================
   Live Validation
========================================== */

const allInputs=document.querySelectorAll("input,select");

allInputs.forEach(input=>{

    input.addEventListener("input",function(){

        if(this.type==="hidden"){

            return;

        }

        if(this.value.trim()===""){

            clearValidation(this);

            return;

        }

        markValid(this);

    });

});

/* ==========================================
   Enter Key Support
========================================== */

document.addEventListener("keydown",function(e){

    if(e.key==="Enter"){

        const activeElement=document.activeElement;

        if(activeElement.tagName==="TEXTAREA"){

            return;

        }

        if(currentStep<totalSteps-1){

            e.preventDefault();

            if(validateCurrentStep()){

                nextStep();

            }

        }

    }

});

/* ==========================================
   Initialize Application
========================================== */

document.addEventListener("DOMContentLoaded",function(){

    showStep(currentStep);

    updateProgress(currentStep);

    updateIndicators(currentStep);

    stopLoading();

    console.log("RainSense AI Loaded Successfully");

});