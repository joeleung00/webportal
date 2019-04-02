$(document).ready(function(){
  $("#new-website").click(function(){
    var element_name = 'message_title';
    if ((element_name in autocomplete_invoked) && (!autocomplete_invoked[element_name])) {
      autocomplete(document.getElementById(element_name), recommendation);
      autocomplete_invoked[element_name] = true;
    }
  });
  $("#new-category").click(function(){
    var element_name = 'cate_title';
    if ((element_name in autocomplete_invoked) && (!autocomplete_invoked[element_name])) {
      autocomplete(document.getElementById(element_name), course_identifiers);
      autocomplete_invoked[element_name] = true;
    }
  });
});
