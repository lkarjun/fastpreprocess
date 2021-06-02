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
      if(action_ == 'drop' || action_ == 'get_dummy'){
        $('#'+column).css('display', 'none');
      }
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
  $('#dropingall').css('display', 'none');
  $.ajax({
      type: 'get',
      url: '/drop',
      data: {'data': 'value'},
      contentType: "application/json",
      success: function(data){
        alert(data);
        window.location.reload();
        console.log(data);
        $('#dropingall').css('display', 'block');
      },
      error: function(data){
      alert(data);
      $('#dropingall').css('display', 'block');
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




// Advance section scripts.....

function var_change() {
  $('#select_var').css("display", "none");
  value = $('#select_var').val();

  $('#var_name').html(value);
  $('#select_var').css("display", "block");

  if(value != 'None'){
      $.ajax({
      type: 'get',
      async: true,
      url: '/info',
      data: {'column': value},
      contentType: "application/json",
      success: function(data){
          console.log(data);
          $('#dtype').html(data.dtype);
          $('#count').html(data.count);
          $('#unique').html(data.unique);   
      },
      error: function(data){
          alert(data);
     }
  });
}
else{
      $('#dtype').html('None');
      $('#count').html('None');
      $('#unique').html('None');
}
} 