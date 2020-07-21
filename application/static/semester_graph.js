const semesterCHART = document.getElementById("semesterChart");
console.log("CHART");
let semesterChart = new Chart(semesterCHART, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [10, 20, 30,40,50],
            cutoutPercentage: 50,
            backgroundColor: ['#133337','#407294','#969dff','#c04847','#4b0082'],
            display: false 
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            '1',
            '2',
            '3',
            '4',
            '5'
        ]
    },
    options: {
         legend: {
            display: false
         },
        
    }
});