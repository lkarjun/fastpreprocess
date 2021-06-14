function action_main(action, value){
  column = $('#'+value).val();
  action_ = $('#'+action).val();
  console.log("Column", column);
  console.log("Action", action_);
  $('#action_btn').css('display', 'none');
  
  $.ajax({
    type: 'get',
    url: '/action',
    data: {'column': String(column), 'action': String(action_)},
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

function testing(){ 

  $.ajax({
      type: 'get',
      url: '/testing',
      data: {'testing': 'testing'},
      contentType: "application/json",
      success: function(data){
        console.log('Testing...')
      },
      error: function(data){
      alert(data);
    }
  })
}



// Advance section scripts.....


// $('#form_replace').on('submit',(function(e) {
//   e.preventDefault();
//   $('#replace_button').css('display', 'none');
//   replacer_ = $('#replacer').val()
//   value = $('#select_var').val();
//   to = $('#replace_to').val();
//   reg = $('#reg_check').is(":checked");
//   $.ajax({

//       type:'GET',
//       url: '/replace',
//       data:{'rep': replacer_,'column': value, 'to': to, 'reg': String(reg)},
//       contentType: "application/json",
//       success: function(data){
//           alert(data);
//           console.log(data);
//           $('#replace_button').css('display', 'block');
//           var_change();
//       },
//       error: function(data){
//           alert(data);
//           $('#replace_button').css('display', 'block');
//       }

//   });
// }));



// function var_change() {
//   $('#select_var').css("display", "none");
//   value = $('#select_var').val();

//   $('#var_name').html(value);
//   $('#select_var').css("display", "block");

//   if(value != 'None'){
//       $.ajax({
//           type: 'get',
//           async: true,
//           url: '/info',
//           data: {'column': value},
//           contentType: "application/json",
//           success: function(data){
//               console.log(data);
//               $('#dtype').html(data.dtype);
//               $('#count').html(data.count);
//               $('#unique').html(data.unique);
//               $('#replacer').empty();
//               // $("#replacer").append("<option id='ALL' value='ALL*' class='font-weight-bold'>###Replace ALL###</option>")
//           //     data.unique_values.forEach(element => {
//           //             var v = '<option id='+element+' value='+ element+'>'+element+'</option>';
//           //     $("#replacer").append(v)
//               $("#IndAdv").css('display', 'block')
//           // });
    
//       },
//           error: function(data){
//               alert(data);
//       }
//   });
//   }
//   else{
//       $('#dtype').html('None');
//       $('#count').html('None');
//       $('#unique').html('None');
//   }
//   }