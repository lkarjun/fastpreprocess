function action_center(value){
  select = '#'+value+'form'
  values = $(select).val()
  console.log(values)
  console.log(select);
  console.log(value);

  $.ajax({
    type: 'get',
    url: '/action',
    data: {'column': value, 'action': values},
    contentType: "application/json",
    success: function(data){
      alert(data);
      console.log(data);
    }
});
}

function drop(value, id){
  $(id+'drop').css("display", "none");
  $.ajax({
      type: 'get',
      url: '/drop',
      data: {'column': value},
      contentType: "application/json",
      success: function(data){
        alert("okay");
        console.log(data);
      }
  });
}


function get_dummy(value, id){ 
  $(id+'getdummy').css("display", "none");

  $.ajax({
      type: 'get',
      url: '/get_dummy',
      data: {'column': value},
      contentType: "application/json",
      success: function(data){
        alert("Okay");
        console.log(data);
      }
  })
}



