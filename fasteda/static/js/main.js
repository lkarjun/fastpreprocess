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

function dropna(){
  $.ajax({
      type: 'get',
      url: '/drop',
      data: {'data': 'value'},
      contentType: "application/json",
      success: function(data){
        alert(data);
        window.location.reload();
        alert(data);
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


