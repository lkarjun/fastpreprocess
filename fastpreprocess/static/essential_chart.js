function corr(data){

    var options = {
          legend: {
              show: false
            },  
          plotOptions: {
          heatmap: {
            radius: 8,
            colorScale: {
              ranges: [{from: 0, to: 1, color: '#01579B'},
                       {from: -1, to: 0, color: '#004D40'}
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
  
  
  function distribution(values, xaxisdata){
  
    var options = {
      series: [{
  
            data: values.data}],
      chart: { type: "histogram", foreColor: "#999"},
      plotOptions: {
            bar: {borderRadius: 8, horizontal: false}},
      
      title: {
            text: "Distribution Plot"
          },
      xaxis: {  categories: values.categories, 
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
  
    var chart = new ApexCharts(document.querySelector("#numerical_dis"), options);
    chart.render();
  
  };
  
  
  function chartbar(data){
  
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
    var chart = new ApexCharts(document.querySelector("#boxplot_chart"), options);
    chart.render();
  };    
  
  
  function plot_piechart(missing, total){
    var options = {
          series: [missing, total],
          chart: {
                  type: 'donut',
                },
          
          title: {
                text: "Data"
                },
          
          responsive: [{
                  breakpoint: 480,
                  options: {
                      legend: {
                        position: 'bottom'
                        }
                    }
                }],
          labels: ['Missing', 'Non Missing'],
        };
  
        var chart = new ApexCharts(document.querySelector("#overview"), options);
        chart.render();
  };
  
  
  

  function makeanalysis(data){
    chartbar(data.BarPlot)
    $('#cat1').html(data.MostCommon.categories[0])
    $('#cat2').html(data.MostCommon.categories[1])
    $('#m1').html(data.MostCommon.data[0])
    $('#m2').html(data.MostCommon.data[1])
    $('#s1').html(data.Summary.Highest_occuring_values)
    $('#s2').html(data.Summary.Number_of_u0nique_values)
    $('#s3').html(data.Summary.Highest_occuring_values)
    missing = data.Summary.Total_Missing
    if (missing == null){
        $('#total_miss_count').html('0')
        $('#total_miss').html('No Missing Values')

    }
    else{
        $('#total_miss_count').html(missing[0])
        $('#total_miss').html("Total Missing :  "+missing[1]+"%")
    }
    
}

function stat(name){
  $('#statdisplay').css('display', 'block');
  $('#name').html(name);

  $.ajax({
      type: 'get',
      url: '/col_stat',
      data: {'colname': name},
      contentType: "application/json",
      success: function(data){
          console.log(data);
          makeanalysis(data)
      },
      error: function(data){
      alert(data);
  }
})
}


function make_numeric_summary(data, name){
  distribution(data.Distribution, name)
  $('#sn1').html(data.Summary.Number_of_observations)
      $('#sn2').html(data.Summary.Mean)
      $('#sn3').html(data.Summary.Standard_Deviation)
      $('#sn4').html(data.Summary.Minimum)
      $('#sn5').html(data.Summary.Quartile_1)
      $('#sn6').html(data.Summary.Median)
      $('#sn7').html(data.Summary['Quartile 2'])
      $('#sn8').html(data.Summary.Maximum)
      $('#sn9').html(data.Summary.Skewness)
      $('#sn10').html(data.Summary.Kurtosis)


      $('#n1').html(data.Facts.VType)
      $('#n4').html(data.Facts['Outlier Count'])
      missing = data.Facts.TotalMissing
      if (missing == null){
          $('#n2').html('No Missing')
          $('#n3').html('No Missing')
      }
      else{
          $('#n2').html(missing[0])
          $('#n3').html(missing[1])
      }
}

function statnumerical(name){
  $('#numstatdisplay').css('display', 'block');
  $('#name_numerical').html(name);

  $.ajax({
      type: 'get',
      url: '/col_stat',
      data: {'colname': name},
      contentType: "application/json",
      success: function(data){
          console.log(data);
          make_numeric_summary(data, name)                        
      },
      error: function(data){
      alert(data);
  }
})
}