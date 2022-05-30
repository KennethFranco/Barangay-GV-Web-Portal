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
var submitBtn = document.getElementById("finalSubmitButton")

// HTMLs and Forms 
var personal_detailsPage = document.getElementById('personal_details')
var account_infoPage = document.getElementById('account_info')
var addressPage = document.getElementById('addressPage')
var submitPage = document.getElementById('submitPage')

// FORM ELEMENTS
var last_name = document.getElementById('last_name')
var first_name = document.getElementById('first_name')
var middle_name = document.getElementById('middle_name')
var nationality = document.getElementById('nationality')
var sex = document.getElementById('sex')
var civil_status = document.getElementById('civil_status')
var age = document.getElementById('age')
var birthday = document.getElementById('birthday')

var username = document.getElementById('username')
var contact_number = document.getElementById('contact_number')
var email = document.getElementById('email')
var confirm_email = document.getElementById('confirm_email')
var password = document.getElementById('password')
var confirm_password = document.getElementById('confirm_password')

var street = document.getElementById('street')
var province = document.getElementById('province')
var city = document.getElementById('city')
var barangay = document.getElementById('barangay')
var zip_code = document.getElementById('zip_code')

personal_detailsPage.style.display = "block"
account_infoPage.style.display = "none"
addressPage.style.display = "none"
submitPage.style.display = "none"

pd_isIncomplete = false;
ai_isIncomplete = false;
add_isIncomeplete = false;
var errorMessage = ""

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

email.addEventListener("keyup", function () {
    confirm_email.pattern = email.value
})

password.addEventListener("keyup", function () {
    confirm_password.pattern = password.value
})
