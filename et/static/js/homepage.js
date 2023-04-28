const xValues = [50,60,70,80,90,100,110,120,130,140,150];
const yValues = [7,8,8,9,9,9,10,11,14,14,15];

// Chart.defaults.global.defaultFontColor = "#fff";

const plugin = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
      const {ctx} = chart;
      ctx.save();
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = options.color || '#99ffff';
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    }
  };


new Chart("myChart1", {
    type : 'bar',
    data : {
        labels : [ 1500, 1600, 1700, 1750, 1800, 1850,
                1900, 1950, 1999, 2050 ],
        datasets : [
                {
                    data : [ 186, 205, 1321, 1516, 2107,
                            2191, 3133, 3221, 4783, 5478 ],
                    label : "America",
                    borderColor : "#3cba9f",
                    fill : false,
                }]
    },
    options : {
        scales : {
            y : {
                ticks : {
                    color: "#fff",
                }
            },
            x : {
                ticks : {
                    color: "#fff",
                }
            }
        },
        title : {
            display : true,
            text : 'Chart JS Line Chart Example'
        }
    }
});


new Chart("myChart2", {
    type : 'line',
    data : {
        labels : [ 1500, 1600, 1700, 1750, 1800, 1850,
                1900, 1950, 1999, 2050 ],
        datasets : [
                {
                    data : [ 186, 205, 1321, 1516, 2107,
                            2191, 3133, 3221, 4783, 5478 ],
                    label : "America",
                    borderColor : "#3cba9f",
                    fill : false
                },
                {
                    data : [ 1282, 1350, 2411, 2502, 2635,
                            2809, 3947, 4402, 3700, 5267 ],
                    label : "Europe",
                    borderColor : "#626CFC",
                    fill : false
                } ]
    },
    options : {
        scales : {
            y : {
                ticks : {
                    color: "#fff",
                }
            },
            x : {
                ticks : {
                    color: "#fff",
                }
            }
            
        },
    }
});


new Chart("myChart3", {
    type : 'line',
    data : {
        labels : [ 1500, 1600, 1700, 1750, 1800, 1850,
                1900, 1950, 1999, 2050 ],
        datasets : [
                {
                    data : [ 186, 205, 1321, 1516, 2107,
                            2191, 3133, 3221, 4783, 5478 ],
                    label : "America",
                    borderColor : "#3cba9f",
                    fill : false
                },
                {
                    data : [ 1282, 1350, 2411, 2502, 2635,
                            2809, 3947, 4402, 3700, 5267 ],
                    label : "Europe",
                    borderColor : "#626CFC",
                    fill : false
                } ]
    },
    options : {
        scales : {
            y : {
                ticks : {
                    color: "#fff",
                },
                grid: {
                    color: 'white',
                }
            },
            x : {
                ticks : {
                    color: "#fff",
                },
                grid: {
                    display: false,
                }
            },
        },
    }
});
