$("#add_website_form").submit(function(e){
 var check;
 if ($('#add_to_calendar').is(':checked')) {
    check = 1
}
else {
    check = 0
}
 e.preventDefault();
 $.ajax({
   type:"POST",
   url:"",
   data:{
     'message_title':$('#message_title').val(),
     'category_dropdown':$('#category_dropdown').val(),
     'crawllink':$('#crawllink').val(),
     'crawltag':$('#crawltag').val(),
     'add_to_calendar': check,
     'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
   },
   success:function(data){
     $( "#msg_title_error_msg" ).text( "" ).show();
     $( "#url_error_msg" ).text( "" ).show();
     $( "#css_selector_error_msg" ).text( "" ).show();
     if (data == 0){
       $( "#msg_title_error_msg" ).text( "Invalid Title" ).show();
     }
     else if (data == 2){
       $( "#url_error_msg" ).text( "Invalid URL" ).show();
     }
     else if (data == 3){
       $( "#css_selector_error_msg" ).text( "Invalid CSS Selector" ).show();
     }
     else if (data == 4){
       $( "#add_to_calendar_err_msg" ).text( "You have not authorize Google Calendar" ).show();

     }
     else{
        //document.getElementById("add_category_form").reset();
       location.reload();
     }

   }
 })
});
