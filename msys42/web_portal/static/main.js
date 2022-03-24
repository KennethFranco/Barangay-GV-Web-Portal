// ADMIN
$('[data-toggle=offcanvas]').click(function(e) {
  e.preventDefault()
  $('.row-offcanvas').toggleClass('active');
  $('.collapse').toggleClass('in').toggleClass('hidden-xs').toggleClass('visible-xs');
});

function confirmationFunction(){
  document.getElementById("mainFormContent").style.display = "none";
  document.getElementById("confirmationPage").style.display = "block";
  document.getElementById("nextButton").style.display = "none";
}

function backFunction(){
  document.getElementById("mainFormContent").style.display = "block";
  document.getElementById("confirmationPage").style.display = "none";
  document.getElementById("nextButton").style.display = "block";
}
// CURRENT FORM 
var currentForm = localStorage.getItem("currentForm");

// BARANGAY ID CHOICE
if (currentForm === "id") {
  var choice1 = localStorage.getItem("barangay_id_choice");
  console.log(choice1);

  if (choice1 === "Constituent") {
    console.log(currentForm);
    document.getElementById("landlordDiv").style.display = "none";
    console.log("here");
    document.getElementById("maintitle").textContent = "Barangay ID (Constituent)";
    document.getElementById("checkerTitle").textContent = "Barangay ID (Constituent)";
  } else if (choice1 === "Transient") {
    if (document.getElementById("landlordDiv") != null) {
      document.getElementById("landlordDiv").style.display = "block";
    }
    document.getElementById("landlordDiv").style.display = "block";
    document.getElementById("maintitle").textContent = "Barangay ID (Transient)";
    document.getElementById("checkerTitle").textContent = "Barangay ID (Transient)";
  }
}
// BARANGAY CLEARANCE CHOICE
else if (currentForm === "clearance") {
  var choice2 = localStorage.getItem("barangay_clearance_choice");
  console.log(choice2);

  if (choice2 === "Bonafide") {
    console.log("here");
    document.getElementById("maintitle").textContent = "Barangay Clearance (Bonafide)";
    document.getElementById("checkerTitle").textContent = "Barangay Clearance (Bonafide)";
  } else if (choice2 === "Transient") {
    document.getElementById("maintitle").textContent = "Barangay Clearance (Transient)";
    document.getElementById("checkerTitle").textContent = "Barangay Clearance (Transient)";
  }
}

// CERTIFICATE OF INDIGENCY CHOICE
else if (currentForm === "certificate_of_indigency") {
  document.getElementById("maintitle").textContent = "Certificate of Indigency";
  document.getElementById("checkerTitle").textContent = "Certificate of Indigency";
}

// BARANGAY CERTIFICATE CHOICE
else if (currentForm === "barangay_certificate") {
  var choice3 = localStorage.getItem("barangay_certificate_choice");
  console.log("we are here" + choice3);

  if (choice3 === "Bonafide") {
    document.getElementById("maintitle").textContent = "Barangay Certificate (Bonafide)";
    document.getElementById("checkerTitle").textContent = "Barangay Certificate (Bonafide)";
  } else if (choice3 === "Transient") {
    document.getElementById("maintitle").textContent = "Barangay Certificate (Transient)";
    document.getElementById("checkerTitle").textContent = "Barangay Certificate (Transient)";
  }
}


var checkerTitle = document.getElementById("maintitle").textContent.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim();
console.log(checkerTitle)

// BARANGAY ID CONSTITUENT
if (checkerTitle === "Barangay ID (Constituent)") {
  document.getElementById("barangay_id_type").value = "Constituent";
  document.getElementById("votersDiv").style.display = "block";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var emergency_name = document.getElementById("emergency_name").value;
    var emergency_contact_number = document.getElementById("emergency_contact_number").value;
    var emergency_address = document.getElementById("emergency_address").value;
    var first_file = document.getElementById("first_file").value;
    var second_file = document.getElementById("second_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var emergencyContactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }

    if (emergency_contact_number) {
      if (phonenum.test(emergency_contact_number) == false) {
        emergencyContactCheck = false;
      }
      else {
        emergencyContactCheck = true;
      }
    }






    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }

    var file2TypeCheck = true;
    if (second_file != "") {
      file2TypeCheck = true;
      if (second_file != "") {
        var secondFileInput = document.getElementById('second_file');
        var filename = secondFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file2TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }

    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      emergency_name,
      emergency_contact_number,
      emergency_address,
      first_file,
      second_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Emergency Name",
      "Emergency Contact Number",
      "Emergency Address",
      "Government ID/Letter of Acknowledgement",
      "Voter's ID",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 21) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false || emergencyContactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    if (emergencyContactCheck === false) {
      modalContent.innerHTML += "<br />" + "Emergency Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 2: " + file2TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file2TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file2TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }

      if (file2TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "Voter's ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }

      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}

else if (checkerTitle === "Barangay ID (Transient)") {
  document.getElementById("landlordDiv").style.display = "block";
  document.getElementById("barangay_id_type").value = "Transient";
  document.getElementById("votersDiv").style.display = "none";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var emergency_name = document.getElementById("emergency_name").value;
    var emergency_contact_number = document.getElementById("emergency_contact_number").value;
    var emergency_address = document.getElementById("emergency_address").value;
    var landlord_name = document.getElementById("landlord_name").value;
    var landlord_address = document.getElementById("landlord_address").value;
    var landlord_contact_number = document.getElementById("landlord_contact_number").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var emergencyContactCheck = true;
    var landlordContactCheck = true;

    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }

    if (emergency_contact_number) {
      if (phonenum.test(emergency_contact_number) == false) {
        emergencyContactCheck = false;
      }
      else {
        emergencyContactCheck = true;
      }
    }

    if (landlord_contact_number) {
      if (phonenum.test(landlord_contact_number) == false) {
        landlordContactCheck = false;
      }
      else {
        landlordContactCheck = true;
      }
    }





    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }

    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      emergency_name,
      emergency_contact_number,
      emergency_address,
      first_file,
      third_file,
      landlord_name,
      landlord_address,
      landlord_contact_number,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Emergency Name",
      "Emergency Contact Number",
      "Emergency Address",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
      "Landlord/landlady Name",
      "Landlord/landlady Address",
      "Landlord/landlady Contact Number",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 23) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false || emergencyContactCheck === false || landlordContactCheck) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    if (emergencyContactCheck === false) {
      modalContent.innerHTML += "<br />" + "Emergency Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    if (landlordContactCheck === false) {
      modalContent.innerHTML += "<br />" + "Landlord/landlady Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }


      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}

// BARANGAY CLEARANCE BONAFIDE
else if (checkerTitle === "Barangay Clearance (Bonafide)") {
  document.getElementById("barangay_clearance_type").value = "Bonafide";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }







    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }

    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      first_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 17) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }

      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}

// BARANGAY CLEARANCE TRANSIENNT
else if (checkerTitle === "Barangay Clearance (Transient)") {
  document.getElementById("barangay_clearance_type").value = "Transient";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }







    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }


    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      first_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 17) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }


      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}




// -------------------
// CERT OF INDI
else if (checkerTitle === "Certificate of Indigency") {
  console.log("made it");

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  var modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }






    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }



    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      first_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 17) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    if (file1TypeCheck === false || file3TypeCheck === false) {
      error = true;
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }

      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 Photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }
    }


    if (error == true) {
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
      for (const field of fields) {
        console.log(field);
      }
    }

  })
}

// BARANGAY CERTIFICATE BONAFIDE
else if (checkerTitle === "Barangay Certificate (Bonafide)") {
  document.getElementById("barangay_certificate_type").value = "Bonafide";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }







    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }



    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      first_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 17) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file2TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }


      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}

// BARANGAY CERTIFICATE TRANSIENT
else if (checkerTitle === "Barangay Certificate (Transient)") {
  document.getElementById("barangay_certificate_type").value = "Transient";

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();

      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */
  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }


  // data validation

  const form = document.getElementById("mainForm");
  const modal = document.getElementById("exampleModal");
  var error = true;
  const modalContent = document.getElementById("modalText");
  var list = document.getElementById('trial').childNodes;
  var theArray = [];
  for (var i = 0; i < list.length; i++) {
    var arrValue = list[i].innerHTML;
    // alert(arrValue);
    theArray.push(arrValue);
  }

  // FIELDS

  // lisstener for select
  var selectElement = document.querySelector('#first_file_choice');



  selectElement.addEventListener('change', (event) => {
    console.log(selectText);
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice)
    if (first_file_choice === "government_id") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .jpeg, .jpg, .png</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    } else if (first_file_choice === "letter_of_acknowledgement") {
      document.getElementById("selectText").innerHTML = "<p>Accepted files: .docx, .pdf</p>";
      document.getElementById("selectText").classList.add("bodyFont");
      document.getElementById("selectText").classList.add("globalBody");
    }

  });

  form.addEventListener("submit", (e) => {

    var count = 0;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var middle_name = document.getElementById("middle_name").value;
    var age = document.getElementById("age").value;
    var birthday = document.getElementById("birthday").value;
    var sex = document.getElementById("sex").value;
    var nationality = document.getElementById("nationality").value;
    var civil_status = document.getElementById("civil_status").value;
    var email = document.getElementById("email").value;
    var contact_number = document.getElementById("contact_number").value;
    var address_first_line = document.getElementById("address_first_line").value;
    var address_city = document.getElementById("address_city").value;
    var address_barangay = document.getElementById("address_barangay").value;
    var address_zip_code = document.getElementById("address_zip_code").value;
    var address_province = document.getElementById("address_province").value;
    var first_file = document.getElementById("first_file").value;
    var third_file = document.getElementById("third_file").value;

    var existCheck = true;
    if (contact_number != "") {
      console.log("Contact Number: " + contact_number)
      for (const value of theArray) {
        if (value != null) {
          split = value.split(":");
          if (contact_number === split[0]) {
            console.log("same")
            console.log(split[1])
            if (split[1] === "Submitted") {
              existCheck = false;
              error = true;
            }
          }

        }
      }
    }

    
    var emailCheck = true;
    // checking for validity of email
    console.log(emailCheck)
    if (email) {
      console.log("not null");
      console.log(email);
      let emailAtCheck = email.includes("@");

      if (emailAtCheck === true) {
        const emailSplit = email.split("@");
        let emailDotCheck = emailSplit[1].includes(".");
        if (emailDotCheck === true) {
          emailCheck = true;
        } else {
          emailCheck = false;
        }
      } else {
        emailCheck = false;
      }
    }
    else {
      emailCheck = true;
    }


    //checking for validity of phone numbers 
    var contactCheck = true;
    var phonenum = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (contact_number) {
      if (phonenum.test(contact_number) == false) {
        contactCheck = false;
      }
      else {
        contactCheck = true;
      }
    }







    // checking for validity of files
    var file1TypeCheck = true;
    if (first_file != "") {
      console.log('not null file 1')
      var first_file_choice = document.getElementById("first_file_choice").value;
      file1TypeCheck = true;

      if (first_file_choice === "government_id") {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      } else {
        var firstFileInput = document.getElementById('first_file');
        var filename = firstFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      }
    }


    var file3TypeCheck = true;
    if (third_file != "") {
      file3TypeCheck = true;
      if (third_file != "") {
        var thirdFileInput = document.getElementById('third_file');
        var filename = thirdFileInput.files[0].name;
        const fileSplit = filename.split(".");
        file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      }
    }



    var fields = [
      last_name,
      first_name,
      middle_name,
      age,
      birthday,
      sex,
      nationality,
      civil_status,
      email,
      contact_number,
      address_first_line,
      address_city,
      address_barangay,
      address_zip_code,
      address_province,
      first_file,
      third_file,
    ]

    const staticFields = [
      "Last Name",
      "First Name",
      "Middle Name",
      "Age",
      "Birthday",
      "Sex",
      "Nationality",
      "Civil Status",
      "Email",
      "Contact Number",
      "Address First Line",
      "Address City",
      "Address Barangay",
      "Address Zip Code",
      "Address Province",
      "Government ID/Letter of Acknowledgement",
      "1x1 Photo",
    ]


    for (const field of fields) {
      if (field === "" || field === null) {
        console.log(field);
      }
    }

    let x = 0;
    modalContent.innerHTML = "Missing fields:"
    for (const field of fields) {
      if (field === "" || field === null) {
        modalContent.innerHTML += "<br />" + staticFields[x]
      } else {
        count += 1;
      }
      x = x + 1;
    }

    console.log(count)
    if (count == 17) {
      error = false;
    }

    if (emailCheck === false || contactCheck === false) {
      modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    }
    // email check
    if (emailCheck === false) {
      console.log(emailCheck)
      console.log("This is email:" + email);
      if (email != null || email != "") {
        modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow the format: username@email.com";
        error = true;
      }

    }

    if (contactCheck === false) {
      modalContent.innerHTML += "<br />" + "Contact Number Field has incorrect format. Please follow the format: 9171234567";
      error = true;
    }

    // files check
    console.log("File Check 1: " + file1TypeCheck);
    console.log("File Check 3: " + file3TypeCheck);
    if (file1TypeCheck === false || file2TypeCheck === false || file3TypeCheck === false) {
      error = true;
      console.log(file1TypeCheck);
      console.log(file3TypeCheck);
      modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";

      if (file1TypeCheck === false) {
        if (first_file_choice === "government_id") {
          modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
        } else {
          modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
        }

      }

      if (file3TypeCheck === false) {
        modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      }


    }


    if (error == true) {
      console.log(checkerTitle);
      if (checkerTitle === "Barangay ID (Constituent)") {
        console.log("yep")
      }
      e.preventDefault();
      if (existCheck == false) {
        modalContent.innerHTML = "";
        modalContent.innerHTML += "<br />" + "You currently have an onging request with this phone number. Please wait for it to be resolved/finished before submitting a new one.";
      }
      $('#exampleModal').modal("show");
    } else {
      console.log("good");
    }

  })
}


