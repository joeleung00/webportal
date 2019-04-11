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
