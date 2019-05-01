// This function detect how user sort the category and return the order to server
function returnOrder(){
  var items = document.querySelectorAll("#columns li"),
  order = [];

  for (var i = 0; i < items.length; i++){
    order.push(items[i].id);
  }
  $.ajax({
    type:"POST",
    url:"reorder/",
    data:{
      order : order,
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success:function(data){
       location.reload();
    }
  })
}
