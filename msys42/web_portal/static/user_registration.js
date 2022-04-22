// Navigation Banner
var personal_details = document.getElementsByClassName('personalDetailsHeader')
var account_info = document.getElementsByClassName('accountInfoHeader')
var address = document.getElementsByClassName('addressHeader')
var submitPage = document.getElementsByClassName('submitHeader')
// Button Sets
var goToAccountInfo = document.getElementById("goToAccountInfo")

var backToPersonalDetails = document.getElementById("backToPersonalDetails")
var goToAddress = document.getElementById("goToAddress")
var backToAccountInfo = document.getElementById("backToAccountInfo")
var goToSubmit = document.getElementById("goToSubmit")
var backToAdress = document.getElementById("backToAddress")
var submitBtn = document.getElementById("submit")

// HTMLs and Forms 
var mainForm = document.getElementById('mainForm')
var personal_detailsHTML = `
        <div class="row">
            <div class="col-lg-6 col-sm-12 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="last_name">Last Name<span
                        style="color: #B30000;">*</span></label><br>
                <input id="last_name" name="last_name" class="bodyFont formInput" type="text"
                    placeholder="Last Name">
            </div>
            <div class="col-lg-4 col-sm-6 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="nationality">Nationality<span
                        style="color: #B30000;">*</span></label><br>
                <input id="nationality" name="nationality" class="bodyFont formInput" type="text"
                    placeholder="Nationality">
            </div>
            <div class="col-lg-2 col-sm-6 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="sex">Sex<span
                        style="color: #B30000;">*</span></label><br>
                <select id="sex" name="sex" class="bodyFont formInput" type="text" placeholder="Sex">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-sm-12 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="first_name">First Name<span
                        style="color: #B30000;">*</span></label><br>
                <input id="first_name" name="first_name" class="bodyFont formInput" type="text"
                    placeholder="Last Name">
            </div>
            <div class="col-lg-3 col-sm-12 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="civil_status">Civil Status<span
                        style="color: #B30000;">*</span></label><br>
                <select id="civil_status" name="civil_status" class="bodyFont formInput" type="text"
                    placeholder="Civil Status">
                    <option value="Single">Single</option>
                    <option value="Married">Married</option>
                    <option value="Divorced">Divorced</option>
                    <option value="Widowed">Widowed</option>
                </select>
            </div>
            <div class="col-lg-3 col-sm-6 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="age">Age<span
                        style="color: #B30000;">*</span></label><br>
                <input id="age" name="age" class="bodyFont formInput" type="number" placeholder="Age">
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-sm-12 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="middle_name">Middle Name<span
                        style="color: #B30000;">*</span></label><br>
                <input id="middle_name" name="middle_name" class="bodyFont formInput" type="text"
                    placeholder="Middle Name">
            </div>
            <div class="col-lg-3 col-sm-12 mb-4">
                <label class="bodyFont formLabel globalSubHeader" for="birthday">Birthday<span
                        style="color: #B30000;">*</span></label><br>
                <input id="birthday" name="birthday" class="bodyFont formInput" type="date">
            </div>
            <div class="col-lg-3 mb-4">

            </div>
        </div>    
        `
var account_infoHTML = `
        GAY NIGGA
        `
var addressHTML = `
        
        `
var submitHTML = `
        
        `



mainForm.innerHTML += personal_detailsHTML

goToAccountInfo.addEventListener("click", function () {
    submitPage.className += "registrationHeaderPartial";
    address.style.backgroundColor = "white"
    account_info.style.backgroundColor = "white"
    personal_details.style.backgroundColor = "white"

    mainForm.innerHTML = account_infoHTML
});

