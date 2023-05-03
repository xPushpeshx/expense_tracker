const xValues = [50,60,70,80,90,100,110,120,130,140,150];
const yValues = [7,8,8,9,9,9,10,11,14,14,15];

// Chart.defaults.global.defaultFontColor = "#fff";

var chart1_data_limit = document.getElementById("graph1-data-limit").innerHTML.split(',').map( (x)=>{return parseFloat(x);} )
var chart1_data_expense = document.getElementById("graph1-data-expense").innerHTML.split(',').map( (x)=>{return parseFloat(x);} )


new Chart("myChart1", {
    type : 'bar',
    data : {
        labels : [ "Jan", "Feb", "Mar", "Apr", "May", "June" , "July" , "Aug", "Sep", "Oct", "Nov", "Dec" ],
        datasets : [
                {
                    data : chart1_data_limit,
                    label : "Limit",
                    borderColor : "#fff",
                    backgroundColor : "#0e7490",
                    fill : false,
                },
                {
                    data : chart1_data_expense,
                    label : "Expense",
                    borderColor : "#0e7490",
                    backgroundColor : "#059669",
                    fill : false,
                },
            ]
    },
    options : {
        scales : {
            y : {
                ticks : {
                    color: "#000",
                }
            },
            x : {
                ticks : {
                    color: "#000",
                },
                title: {
                    display: true,
                    text: 'Months'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Limit and Expense per Month',
                
              }
        },
        // plugins: [chartAreaBorder]
    },
});

////////////////////////////////////////////////// CHART 2 ///////////////////////////////////////////

function myFunction() {
    var today = new Date();
    var month = today.getMonth();
    return (daysInMonth(month + 1, today.getFullYear()));
}

function daysInMonth(month,year) {
  return new Date(year, month, 0).getDate();
}

var days = myFunction();
var days_labels = [];
for (var i = 0 ; i<days ;i++){
    days_labels.push(i+1);
}

var chart2_data = document.getElementById("graph2-data").innerHTML.split(',').map( (x)=>{return parseFloat(x);} )
var dates_for_label = [];

new Chart("myChart2", {
    type : 'line',
    data : {
        labels : days_labels,
        datasets : [
                {
                    data : chart2_data,
                    label : "Daily Expense",
                    borderColor : "#3cba9f",
                    fill : false
                },
                {
                    data : [],
                    label : "some thing else",
                    borderColor : "#626CFC",
                    fill : false
                } ]
    },
    options : {
        scales : {
            y : {
                ticks : {
                    color: "#000",
                }
            },
            x : {
                ticks : {
                    color: "#000",
                    maxRotation: 0,
                    minRotation: 0,
                },
                title: {
                    display: true,
                    text: 'Days'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Monthly Expenses',
                
              }
        },
},
    plugins: []
});
