// Navigation Banner
var personal_details = document.getElementById('personalDetailsHeader')
var account_info = document.getElementById('accountInfoHeader')
var address = document.getElementById('addressHeader')
var submitHeader = document.getElementById('submitHeader')
// Button Sets
var goToAccountInfo = document.getElementById("goToAccountInfo")

var backToPersonalDetails = document.getElementById("backToPersonalDetails")
var goToAddress = document.getElementById("goToAddress")
var backToAccountInfo = document.getElementById("backToAccountInfo")
var goToSubmit = document.getElementById("goToSubmit")
var backToAddress = document.getElementById("backToAddress")
var submitBtn = document.getElementById("submit")

// HTMLs and Forms 
var personal_detailsPage = document.getElementById('personal_details')
var account_infoPage = document.getElementById('account_info')
var addressPage = document.getElementById('addressPage')
var submitPage = document.getElementById('submitPage')

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
    <div class="row">
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="username">Username<span
                    style="color: #B30000;">*</span></label><br>
            <input id="username" name="username" class="bodyFont formInput" type="text"
                placeholder="Username">
        </div>
        <div class="col-lg-6 spacer">
            
        </div>
        </div>
        <div class="row">
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="email">Email<span
                    style="color: #B30000;">*</span></label><br>
            <input id="email" name="email" class="bodyFont formInput" type="text"
                placeholder="Email">
        </div>
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="confirm_email">Confirm Email<span
                    style="color: #B30000;">*</span></label><br>
            <input id="confirm_email" name="confirm_email" class="bodyFont formInput" type="text"
                placeholder="Confirm Email">
        </div>
        </div>
        <div class="row">
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="contact_number">Contact Number<span
                    style="color: #B30000;">*</span></label><br>
            <input id="contact_number" name="contact_number" class="bodyFont formInput" type="text"
                placeholder="9XXXXXXXXX">
        </div>
        <div class="col-lg-6 spacer">
        </div>
        </div>
        <div class="row">
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="password">Password<span
                    style="color: #B30000;">*</span></label><br>
            <input id="password" name="password" class="bodyFont formInput" type="text"
                placeholder="Password">
        </div>
        <div class="col-lg-6 col-sm-12 mb-4">
            <label class="bodyFont formLabel globalSubHeader" for="confirm_password">Confirm Password<span
                    style="color: #B30000;">*</span></label><br>
            <input id="confirm_password" name="confirm_password" class="bodyFont formInput" type="text"
                placeholder="Confirm Password">
        </div>
    </div>
        `
var addressHTML = `
        WOAH WOAH WAOH
        
        `
var submitHTML = `
        FUCK 
        `

personal_detailsPage.innerHTML = personal_detailsHTML
account_infoPage.innerHTML = account_infoHTML
addressPage.innerHTML += addressHTML
submitPage.innerHTML += submitHTML

personal_detailsPage.style.display = "block"
account_infoPage.style.display = "none"
addressPage.style.display = "none"
submitPage.style.display = "none"

// BUTTON LOGIC
// Go to ACCOUNT INFO
goToAccountInfo.addEventListener("click", function () {
    personal_details.style.backgroundColor = "transparent"
    account_info.style.backgroundColor = "white"
    address.style.backgroundColor = "transparent"
    submitHeader.style.backgroundColor = "transparent"

    backToPersonalDetails.style.display = "block"
    goToAddress.style.display = "block"
    goToAccountInfo.style.display = "none"


    personal_detailsPage.style.display = "none"
    account_infoPage.style.display = "block"
    addressPage.style.display = "none"
    submitPage.style.display = "none"


    console.log("GO TO ACCOUNT INFO")
});

// Back to PERSONAL DETAILS
backToPersonalDetails.addEventListener("click", function () {
    personal_details.style.backgroundColor = "white"
    account_info.style.backgroundColor = "transparent"
    address.style.backgroundColor = "transparent"
    submitHeader.style.backgroundColor = "transparent"

    backToPersonalDetails.style.display = "none"
    goToAddress.style.display = "none"
    goToAccountInfo.style.display = "block"

    personal_detailsPage.style.display = "block"
    account_infoPage.style.display = "none"
    addressPage.style.display = "none"
    submitPage.style.display = "none"
});

// Go to ADDRESS
goToAddress.addEventListener("click", function () {
    personal_details.style.backgroundColor = "transparent"
    account_info.style.backgroundColor = "transparent"
    address.style.backgroundColor = "white"
    submitHeader.style.backgroundColor = "transparent"

    backToPersonalDetails.style.display = "none"
    goToAddress.style.display = "none"
    backToAccountInfo.style.display = "block"
    goToSubmit.style.display = "block"

    personal_detailsPage.style.display = "none"
    account_infoPage.style.display = "none"
    addressPage.style.display = "block"
    submitPage.style.display = "none"
});

// Back to ACCOUNT INFO
backToAccountInfo.addEventListener("click", function () {
    personal_details.style.backgroundColor = "transparent"
    account_info.style.backgroundColor = "white"
    address.style.backgroundColor = "transparent"
    submitHeader.style.backgroundColor = "transparent"

    backToPersonalDetails.style.display = "block"
    goToAddress.style.display = "block"
    backToAccountInfo.style.display = "none"
    goToSubmit.style.display = "none"

    personal_detailsPage.style.display = "none"
    account_infoPage.style.display = "block"
    addressPage.style.display = "none"
    submitPage.style.display = "none"
});

// Go to SUBMIT
goToSubmit.addEventListener("click", function () {
    personal_details.style.backgroundColor = "transparent"
    account_info.style.backgroundColor = "transparent"
    address.style.backgroundColor = "transparent"
    submitHeader.style.backgroundColor = "white"

    backToAddress.style.display = "block"
    submitBtn.style.display = "block"
    backToAccountInfo.style.display = "none"
    goToSubmit.style.display = "none"

    personal_detailsPage.style.display = "none"
    account_infoPage.style.display = "none"
    addressPage.style.display = "none"
    submitPage.style.display = "block"
});

// Back to ADDRESS
backToAddress.addEventListener("click", function () {
    personal_details.style.backgroundColor = "transparent"
    account_info.style.backgroundColor = "transparent"
    address.style.backgroundColor = "white"
    submitHeader.style.backgroundColor = "transparent"

    backToAddress.style.display = "none"
    submitBtn.style.display = "none"
    backToAccountInfo.style.display = "block"
    goToSubmit.style.display = "block"

    personal_detailsPage.style.display = "none"
    account_infoPage.style.display = "none"
    addressPage.style.display = "block"
    submitPage.style.display = "none"
});

// SUBMIT
submitBtn.addEventListener("click", function () {
    console.log("SUBMITTED SHEEESH")
});

