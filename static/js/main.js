
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


function corr(data){

  var options = {
        legend: {
            show: false
          },  
        plotOptions: {
        heatmap: {
          radius: 8,
          colorScale: {
            ranges: [{from: 0, to: 1, color: '#0000ff'},
                     {from: -1, to: 0, color: '#ff0000'}
                     ],
          },
          }
        },
        
        chart: {
          type: 'heatmap'
        },
  
        series: data
}
var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render()

};



function boxplot(data, div_id){
  var options = {
    series: data,
    
    chart: {
      type: 'boxPlot',
      height: 350 },
      
      colors: ['#008FFB', '#FEB019'],
      title: {
      text: 'BoxPlot',
      align: 'left'
    },
    tooltip: {
      shared: false,
      intersect: true
    }
  };

  var chart = new ApexCharts(document.querySelector(div_id), options);
  chart.render();

};


function distribution(values, div_id, xaxisdata){
  console.log(values[0].data)
  var options = {
    series: [{

          data: values[0].data}],
    chart: { type: "histogram", foreColor: "#999"},
    plotOptions: {
          bar: {borderRadius: 8, horizontal: false}},
    
    title: {
          text: "Distribution Plot"
        },
    xaxis: {  categories: values[0].categories, 
              axisBorder: { show: false},
              axisTicks: { show: true },
              title: {
                text: xaxisdata,
              }},

    yaxis: {   tickAmount: 6, 
               labels: { offsetX: -5, offsetY: -5 },
               title: {
                text: 'Count',
              }
              },
    dataLabels: { enabled: false }
  
  };

  var chart = new ApexCharts(document.querySelector(div_id), options);
  chart.render();

};


function chartbar(data, div_id){
  console.log(data);
  var options = {
                series: [{
                      data: data.data
                    }],
                
                title: {
                      text: "Bar Plot"
                  },
                chart: {
                      type: 'bar',
                      height: 350
                    },
                
                plotOptions: {
                      bar: {  borderRadius: 15,
                      horizontal: true,
                      }
                  },
   
                dataLabels: {
                      enabled: true
                  },
                    
                xaxis: {
                      categories: data.categories
                  }
                };
  var chart = new ApexCharts(document.querySelector(div_id), options);
  chart.render();
};


