$(document).ready(function(){
  $("#new-website").click(function(){
    if (!autocomplete_invoked) {
      autocomplete(document.getElementById("message_title"), course_identifiers);
      autocomplete_invoked = true;
    }
  });
});
