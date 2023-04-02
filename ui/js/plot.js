function NewChart (data) {

    const ctx = document.getElementById('myChart');

    const DISPLAY = true;
    const BORDER = true;
    const CHART_AREA = true;
    const TICKS = true;
    var TIME_data = [];

    for (let i=0;i<0.5;i= i+0.001) {
        
        TIME_data.push(i.toFixed(4));
    }
    console.log(TIME_data.length);

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
        labels: TIME_data,
        datasets: [{
            label: '# Gamma',
            data: data,
            borderWidth: 1,
            
        }]
        },
        options: {  responsive: true,
        plugins: {
            title: {
            display: true,
            text: 'Grid Line Settings'
            }
        },
        scales: {
            x: {
            border: {
                display: BORDER
            },
            grid: {
                color: '#b0b0b0'
            }
            },
            y: {
            border: {
                display: false
            },
            grid: {
                color: '#b0b0b0' 
            }
                }
            
            }
        }
        }
    );
}