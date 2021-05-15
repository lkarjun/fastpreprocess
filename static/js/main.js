$(document).ready(function (e) {
    $('#UploadForm').on('submit',(function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append('file', $('#fileData')[0].files[0])
        var imgname  =  $('input[type=file]').val();
        var size  =  $('#fileData')[0].files[0].size;
        var type = $('#fileData')[0].files[0].type;
        console.log(size);
        console.log(imgname);
        console.log(type);
        $.ajax({
            type:'POST',
            url: '/edafileupload',
            data:formData,
            enctype: 'multipart/form-data',
            cache:false,
            contentType: false,
            processData: false,
            success:function(data){
                console.log("success");
                console.log(data);
                $("#upload-sec").css('display', 'none');
                $("#show-details").css('display', 'block');
                $('#filename').html(data.filename);
                $('#filesize').html(data.filesize);
                $('#filetype').html(data.filetype);

            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
    }));

});