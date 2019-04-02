$(document).ready(function(){
  $("#new-website").click(function(){
    autocomplete(document.getElementById("message_title"), course_identifiers);
  });
});
