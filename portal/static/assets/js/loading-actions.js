$(document).ready(function(){
  $("#new-website").click(function(){
    autocomplete(document.getElementById("myInput"), countries);
  });
});
