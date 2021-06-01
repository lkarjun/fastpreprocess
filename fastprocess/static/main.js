function action_main(action, value){
  column = $('#'+value).val();
  action_ = $('#'+action).val();
  console.log("Column", column);
  console.log("Action", action_);
  $('#action_btn').css('display', 'none');
  
  $.ajax({
    type: 'get',
    url: '/action',
    data: {'column': column, 'action': action_},
    contentType: "application/json",
    success: function(data){
      $('#action_btn').css('display', 'block');
      alert(data);
      console.log(data);
    },
    error: function(data){
      $('#action_btn').css('display', 'block');
      alert(data);
    }
});
}




function action_center(value){
  select = '#'+value+'form'
  button = '#'+value+'button'
  values = $(select).val()
  console.log(values)
  console.log(select);
  console.log(value);
  $(button).css('display', 'none');
  console.log(button);
  $.ajax({
    type: 'get',
    url: '/action',
    data: {'column': value, 'action': values},
    contentType: "application/json",
    success: function(data){
      $(button).css('display', 'block');
      alert(data);
      console.log(data);
    },
    error: function(data){
      $(button).css('display', 'block');
      alert(data);
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
        console.log(data);
      },
      error: function(data){
      alert(data);
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
      },
      error: function(data){
      alert(data);
    }
  })
}


