
function drop(value, id){
  $(id+'view').css("display", "block"); 
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
  $(id+'view').css("display", "block"); 
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