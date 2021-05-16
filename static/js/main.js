import "apexcharts";

var options = {
  series: [{
  name: 'Metric1',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric2',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric3',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric4',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric5',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric6',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric7',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric8',
  data: generateData(18, {
    min: 0,
    max: 90
  })
},
{
  name: 'Metric9',
  data: generateData(18, {
    min: 0,
    max: 90
  })
}
],
  chart: {
  height: 350,
  type: 'heatmap',
},
dataLabels: {
  enabled: false
},
colors: ["#008FFB"],
title: {
  text: 'HeatMap Chart (Single color)'
},
};

var chart = new ApexCharts(document.querySelector("#myChart"), options);
chart.render();

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