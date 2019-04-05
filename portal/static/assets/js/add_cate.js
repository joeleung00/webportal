
$("#add_category_form").submit(function(e){
 e.preventDefault();
 $.ajax({
   type:"POST",
   url:"",
   data:{
     'new_cate_title':$('#new_cate_title').val(),
     'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
   },
   success:function(data){
     if (data == "error"){
       $( "#category_error_msg" ).text( "Duplicated category name, Please enter again" ).show();
     }
     else{
        //document.getElementById("add_category_form").reset();
       $( "#category_error_msg" ).text("").show();
       location.reload();
     }

   }
 })
});
