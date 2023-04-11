const ctx_1 = document.getElementById('myChart_1');

const TIME_data_2 = [];

for (let i=0;i<0.51;i= i+0.001) {
    TIME_data_2.push(i.toFixed(4));
}

window.myChart_1 = new Chart(ctx_1, {
    type: 'line',
    data: {
    labels: TIME_data_2,
    datasets: [{
        label: '# Iкз',
        data: [],
        borderWidth: 1,
        borderColor: '#FF4500',       
        backgroundColor: "#FF4500"
    }]
    },
    options: {  responsive: true,
    plugins: {
        title: {
        display: true,
        text: 'Ток КЗ'
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


function addData_1(data) {

    window.myChart_1 = new Chart(ctx_1, {
        type: 'line',
        data: {
        labels: TIME_data_2,
        datasets: [{
            label: '# I кз',
            data: data,
            borderWidth: 0.5,
            borderColor: '#FF4500',
            backgroundColor: "#FF4500"
                
        },]
        },
        options: {  responsive: true,
        plugins: {
            title: {
            display: true,
            text: 'Ток КЗ'
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