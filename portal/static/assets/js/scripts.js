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
function selectMessages()
{

    var selectMessageButton = document.getElementById("select_message_button");
    var deleteSelectMessageButton = document.getElementById("delete_select_message_button");

    var checkbox = document.getElementsByClassName("selectMessage");
    for(var i=0; i<checkbox.length; i++) {
      if (checkbox[i].style.display === "none") {
        checkbox[i].style.display = "block";
        selectMessageButton.className = "btn btn-warning btn-block";
        deleteSelectMessageButton.style.display = "block";
      } else {
        checkbox[i].style.display = "none";
        selectMessageButton.className = "btn btn-success btn-block";
        deleteSelectMessageButton.style.display = "none";
      }
    }
    if(selectedMessage.length > 0){
      deleteSelectMessageButton.className = "btn btn-danger btn-block";
    } else {
      deleteSelectMessageButton.className = "btn btn-secordary btn-block";
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

    var deleteSelectMessageButton = document.getElementById("delete_select_message_button");
    if(selectedMessage.length > 0){
      deleteSelectMessageButton.className = "btn btn-danger btn-block";
    } else {
      deleteSelectMessageButton.className = "btn btn-secordary btn-block";
    }

    // console.log(selectedMessage);

}

function deleteSelectedMessage()
{
    var current_url = document.getElementById("currentURL");
    var deleteSelectMessageButton = document.getElementById("delete_select_message_button");
    if(deleteSelectMessageButton.className == "btn btn-secordary btn-block"){
      return;
    } else {
      $.ajax({
             type: "POST",
             url: current_url,
             data: {selectedMessage: selectedMessage,
                    Delete_multi_msg: true,
                    'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),},
             success: function() {
                location.reload();
             }
          });
    }

}

function deleteCate(cate_id)
{
    var current_url = document.getElementById("currentURL");
    $.ajax({
           type: "POST",
           url: current_url,
           data: {deleteCate: cate_id,
                  'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),},
           success: function() {
              location.reload();
           }
        });

}
