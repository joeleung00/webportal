// Ref: https://www.w3schools.com/howto/howto_js_autocomplete.asp

// TODO: release the resources when autocomplete is not needed to avoid memory leak

var course_identifiers = ["CENG2010","CENG2400","ESTR2100","CENG3150","CENG3410","CENG3420","CENG3430","ESTR3100","CENG3470","CENG3490","CENG4100","CENG4120","CENG4480","CENG4998","CENG4999","CENG5030","CENG5050","CENG5270","CENG5271","CENG5410","ENGG5101","CENG5420","CENG5440","CENG5430","CSCI1020","CSCI1030","CSCI1040","CSCI1050","CSCI1110","CSCI1120","ESTR1100","CSCI1130","ESTR1102","CSCI1140","CSCI1510","CSCI1520","CSCI1530","CSCI1540","CSCI1580","CSCI2100","ESTR2102","CSCI2110","CSCI2120","CSCI2510","CSCI2520","CSCI2720","CSCI2800","CSCI3100","CSCI3120","CSCI3130","CSCI3150","ESTR3102","CSCI3160","ESTR3104","CSCI3170","CSCI3180","ESTR3106","CSCI3190","CSCI3220","CSCI3230","ESTR3108","CSCI3250","CSCI3251","CSCI3260","CSCI3270","CSCI3280","CSCI3290","CSCI3310","CSCI3320","CSCI3420","CSCI4120","CSCI4140","CSCI4160","CSCI4180","ESTR4106","CSCI4190","CSCI4210","CSCI4220","CSCI4230","CSCI4430","ESTR4120","CSCI4998","CSCI4999","CSCI5010","CSCI5020","CSCI5030","CSCI5050","CSCI5060","CSCI5070","CSCI5080","CSCI5120","CSCI5150","CSCI5160","ENGG5102","CSCI5170","CSCI5180","ENGG5103","CSCI5210","CSCI5240","CSCI5250","ENGG5106","CSCI5280","ENGG5104","CSCI5320","CSCI5350","CSCI5370","CSCI5390","CSCI5430","CSCI5440","CSCI5450","CSCI5460","ENGG5105","CSCI5470","CSCI5510","ENGG5108","CSCI5530","CSCI5520","CSCI5550","CSCI5560","CSCI5570","CSCI5580","CSCI5590","CSCI5600","ENGG1310","ESTR1003","ENGG1410","ESTR1004","ENGG1820","ENGG2020","ESTR2104","ENGG2420","ESTR2000","ENGG2430","ESTR2002","ENGG2440","ESTR2004","ENGG3802","ENGG3803","ENGG4030","ESTR4300","IERG4300","ENGG5781"]

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}
