
const ctx = document.getElementById('myChart');

const DISPLAY = true;
const BORDER = true;
const CHART_AREA = true;
const TICKS = true;

const TIME_data = [];

for (let i=0;i<0.51;i= i+0.01) {
        
    TIME_data.push(i.toFixed(4));
}

window.myChart = new Chart(ctx, {
    type: 'line',
    data: {
    labels: TIME_data,
    datasets: [{
        label: '# Gamma',
        data: [],
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
            display: BORDER
        },
        grid: {
            color: '#b0b0b0' 
        }
            }
            
           }
        }
        }
    );


function removeData() {
    window.myChart.destroy();
    }

function addData(data) {

    window.myChart = new Chart(ctx, {
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
                display: BORDER
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