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
// console.log(modalContent.textContent)

// FIELDS


form.addEventListener("submit", (e) => {
  var count = 0;
  var last_name = document.getElementById("last_name").value;
  var first_name = document.getElementById("first_name").value;
  var middle_name = document.getElementById("middle_name").value;
  var age = document.getElementById("age").value;
  var birthday = document.getElementById("birthday").value;
  var sex  = document.getElementById("sex").value;
  var nationality = document.getElementById("nationality").value;
  var civil_status = document.getElementById("civil_status").value;
  var email= document.getElementById("email").value;
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



  // checking for validity of email
  if (email != ""){
    var emailCheck = true;
    let emailAtCheck = email.includes("@");
  
    if (emailAtCheck === true){
      const emailSplit = email.split("@");
      let emailDotCheck = emailSplit[1].includes(".");
      if (emailDotCheck === true) {
        emailCheck = true;
      } else{
        emailCheck = false;
      }
    } else{
      emailCheck = false;
    }
  }

  // checking for validity of files
  var file1TypeCheck = true;
  if (first_file != ""){
    var first_file_choice = document.getElementById("first_file_choice").value;
    console.log(first_file_choice);
    file1TypeCheck = true;
  
    if (first_file_choice ===  "government_id"){
      var firstFileInput = document.getElementById('first_file');   
      var filename = firstFileInput.files[0].name;
      const fileSplit = filename.split(".");
      file1TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      console.log(file1TypeCheck);
    } else{
      var firstFileInput = document.getElementById('first_file');   
      var filename = firstFileInput.files[0].name;
      const fileSplit = filename.split(".");
      file1TypeCheck = fileSplit[1].includes("docx") || fileSplit[1].includes("pdf");
      console.log(file1TypeCheck);
    }
  }

  var file2TypeCheck = true;
  if (second_file != ""){
    file2TypeCheck = true;
    if (second_file != ""){
      var secondFileInput = document.getElementById('second_file');   
      var filename = secondFileInput.files[0].name;
      const fileSplit = filename.split(".");
      file2TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      console.log(file2TypeCheck);
    }
  }

  var file3TypeCheck =true;
  if (third_file != ""){
    file3TypeCheck = true;
    if (third_file != ""){
      var thirdFileInput = document.getElementById('third_file');   
      var filename = thirdFileInput.files[0].name;
      const fileSplit = filename.split(".");
      file3TypeCheck = fileSplit[1].includes("jpg") || fileSplit[1].includes("jpeg") || fileSplit[1].includes("png");
      console.log(file3TypeCheck);
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
    "Government ID",
    "Voter's ID",
    "1x1 Photo",
  ]


  for (const field of fields){
    if (field === "" || field === null){
      console.log(field);
    }
  }

  let x = 0;
  modalContent.innerHTML = "Missing fields:"
  for (const field of fields){
    if (field === "" || field === null){
      modalContent.innerHTML += "<br />" + staticFields[x]
    } else{
      count += 1;
    }
    x = x+1;
  }

  console.log(count)
  if (count == 21){
    error = false;
  }

  // email check
  if (emailCheck === false){
    modalContent.innerHTML += "<br />" + "<br />" + "Incorrect format fields:";
    modalContent.innerHTML += "<br />" + "Email field has incorrect format. Please follow example.";
    error = true;
  }

  // files check
  console.log(file1TypeCheck);
  console.log(file2TypeCheck);
  console.log(file3TypeCheck);
  if (file1TypeCheck === false || file2TypeCheck === false || file3TypeCheck === false){
    error = true;
    console.log(file1TypeCheck);
    console.log(file2TypeCheck);
    console.log(file3TypeCheck);
    modalContent.innerHTML += "<br />" + "<br />" + "Unaccepted file types:";
    
    if (file1TypeCheck === false){
      if (first_file_choice === "government_id"){
        modalContent.innerHTML += "<br />" + "Government ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
      } else{
        modalContent.innerHTML += "<br />" + "Letter of Acknowledgement field has an unaccepted file type. Please use .docx or .pdf.";
      }

    }

    if (file2TypeCheck === false) {
      modalContent.innerHTML += "<br />" + "Voter's ID field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
    }

    if (file3TypeCheck === false){
      modalContent.innerHTML += "<br />" + "1x1 photo field has an unaccepted file type. Please use .jpeg, .jpg, or .png.";
    }
    
    
  }

  if (error == true){
    console.log(emailCheck)
    e.preventDefault();
    $('#exampleModal').modal("show");
    // modalContent.innerHTML = "";
  } else{
    console.log("good");
  }

})