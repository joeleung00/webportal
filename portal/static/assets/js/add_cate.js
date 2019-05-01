// User created category will be post by this ajax function so we can create new category without refreshing the page
$("#add_category_form").submit(function(e){
 e.preventDefault();
 $.ajax({
   type:"POST",
   url:"",
   data:{
     'new_cate_title':$('#new_cate_title').val(), // the category title will be sent
     'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val() // security concern: prevent CSRF
   },
   success:function(data){
     // The server will send the error message if the created category is invalid
     if (data == "error"){
       $( "#category_error_msg" ).text( "Duplicated category name or name is empty. Please enter again" ).show();
     }
     else{
        //document.getElementById("add_category_form").reset();
       $( "#category_error_msg" ).text("").show();
       location.reload();
     }

   }
 })
});
