const CHART = document.getElementById("lineChart");
let lineChart = new Chart(CHART, {
    type: 'line',
    data: {
        
        datasets: [
            {
                
                fill: true,
                lineTension: 0.2,
                backgroundColor: "rgba(114, 1, 46, 0.2)",
                borderColor: "rgba(114, 1, 46, 0.6)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(114, 1, 46, 0.6)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHitRadius: 10,
                spanGaps: true,
                data: [{t: "2015-03-15T13:03:00Z",y: 12},
                  {t: "2015-03-16T13:02:00Z",y: 21},
                  {
                    t: "2015-04-25T14:12:00Z",
                    y: 32
                  },
                  {
                    t: "2015-10-25T14:12:00Z",
                    y: 32
                  },
                  {
                    t: "2016-10-25T14:12:00Z",
                    y: 10
                  }
                ],
            }           
        ]},
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'month'
                    },
                    distribution: 'linear'
                }]
            },
            legend: {
                display: false
            },
            
        },
    
    });