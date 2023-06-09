
const ctx = document.getElementById('myChart');

var DISPLAY = true;
var BORDER = true;
var CHART_AREA = true;
var TICKS = true;

const TIME_data = [];
for (let i=0;i<0.51;i=i+0.01) {
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
        text: 'Типовая кривая тока КЗ',
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
    window.myChart_1.destroy();
    }

function addData(data) {

    const _data = [];

    for (let i = 0; i < data.length; i = i + (data.length)/51) {
        _data.push(data[i]);
        
    }
    console.log('Длина _data: %d', _data);
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
        labels: TIME_data,
        datasets: [{
            label: '# Gamma',
            data: _data,
            borderWidth: 1,   
            
        }]
        },
        options: {  responsive: true,
        plugins: {
            title: {
            display: true,
            text: 'Типовая кривая тока КЗ'
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