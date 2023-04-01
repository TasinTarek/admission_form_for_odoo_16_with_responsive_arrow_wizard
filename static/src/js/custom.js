// Next
function nextSection() {
  var currentSection = document.querySelector(
    'section[style*="display: block"]'
  );

  if (currentSection.getAttribute("id") === "section1") {
    // document.getElementById('section2').scrollIntoView({behavior: 'smooth'});
    document.getElementById("section2").style.display = "block";
    document.querySelector(".color2").style.backgroundColor = "lightblue";
  } else if (currentSection.getAttribute("id") === "section2") {
    document.getElementById("section3").style.display = "block";
    document.querySelector(".color3").style.backgroundColor = "lightblue";
  }else if (currentSection.getAttribute("id") === "section3") {
    document.getElementById("section4").style.display = "block";
    document.querySelector(".color4").style.backgroundColor = "lightblue";
  }else if (currentSection.getAttribute("id") === "section4") {
    document.getElementById("section4").style.display = "none";
    document.getElementById("section5").style.display = "block";
    document.querySelector("button:last-child").style.display = "none";
    document.querySelector(".color5").style.backgroundColor = "lightblue"; // hide "next" button on last section
    
    }

  currentSection.style.display = "none";
  document.querySelector("button:first-child").style.display = "block"; // show "previous" button when moving forward
  document.body.scrollTop = document.documentElement.scrollTop = 0;
}
// Previous
function prevSection() {
  var currentSection = document.querySelector(
    'section[style*="display: block"]'
  );

  if (currentSection.getAttribute("id") === "section2") {
    document.querySelector(".color2").style.backgroundColor =
      "rgb(194, 225, 177)";
    document.getElementById("section1").style.display = "block";
    document.querySelector("button:first-child").style.display = "none"; // hide "previous" button on first section
  } else if (currentSection.getAttribute("id") === "section3") {
    document.querySelector(".color3").style.backgroundColor =
      "rgb(194, 225, 177)";
    document.getElementById("section2").style.display = "block";
    
  } else if (currentSection.getAttribute("id") === "section4") {
    document.querySelector(".color4").style.backgroundColor =
      "rgb(194, 225, 177)";
    document.getElementById("section3").style.display = "block";
    
  }else if (currentSection.getAttribute("id") === "section5") {
    document.querySelector(".color5").style.backgroundColor =
      "rgb(194, 225, 177)";
    document.getElementById("section4").style.display = "block";
    document.getElementById("section5").style.display = "none";
    document.querySelector("button:last-child").style.display = "block"; // show "next" button when moving back from last section
  }

  currentSection.style.display = "none";
  document.querySelector("button:last-child").style.display = "block"; // show "next" button when moving backward
  document.body.scrollTop = document.documentElement.scrollTop = 0;

}

// Addresses

const sameAsPermanentCheckbox = document.getElementById('same-as-permanent');
      const permanentAddressLine1 = document.getElementById('permanent-address');
      const permanentZipCode = document.getElementById('permanent-zip');
      const presentAddressLine1 = document.getElementById('present-address');
      const presentZipCode = document.getElementById('present-zip');
      
      sameAsPermanentCheckbox.addEventListener('change', function() {
        if (this.checked) {
          presentAddressLine1.value = permanentAddressLine1.value;
          presentZipCode.value = permanentZipCode.value;
        } 
        else {
          presentAddressLine1.value = '';
          presentZipCode.value = '';
        }
      });
  