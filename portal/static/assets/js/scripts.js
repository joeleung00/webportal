(function(window, undefined) {
  'use strict';

  /*
  NOTE:
  ------
  PLACE HERE YOUR OWN JAVASCRIPT CODE IF NEEDED
  WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR JAVASCRIPT CODE PLEASE CONSIDER WRITING YOUR SCRIPT HERE.  */


})(window);

var selectedMessage = [];

// use Shift + F5 (in Chrome) if Django cannot update the JS file
function selectMessage()
{

    var selectMessageButton = document.getElementById("select_message_button");
    var deleteSelectMessageButton = document.getElementById("delete_select_message_button");

    var checkbox = document.getElementsByClassName("selectMessage");
    for(var i=0; i<checkbox.length; i++) {
      if (checkbox[i].style.display === "none") {
        checkbox[i].style.display = "block";
        selectMessageButton.className = "btn btn-secordary btn-min-width";
        deleteSelectMessageButton.className = "btn btn-danger btn-min-width";
      } else {
        checkbox[i].style.display = "none";
        selectMessageButton.className = "btn btn-success btn-min-width";
        deleteSelectMessageButton.className = "btn btn-secordary btn-min-width";
      }
    }
}

function updateCheckBoxValue(messageID)
{
    isSelected = false;
    var index=0;
    // check is in array or not
    for(index=0; index<selectedMessage.length; index++){
        if(selectedMessage[index] == messageID){
          isSelected = true;
          break;
        }
    }

    if(isSelected){
      selectedMessage.splice(index,1);  // delete element
    } else {
      selectedMessage.push(messageID);  // add element
    }

    console.log(selectedMessage);

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken')

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function deleteSelectedMessage()
{
    var current_url = document.getElementById("currentURL");
    var deleteSelectMessageButton = document.getElementById("delete_select_message_button");
    if(deleteSelectMessageButton.className == "btn btn-secordary btn-min-width"){
      return;
    } else {
      var dataObj = {'Delete_multi_msg': selectedMessage};
      $.ajax({
             type: "POST",
             url: current_url,
             data: dataObj,
             success: function() {

             }
          });
    }

}
