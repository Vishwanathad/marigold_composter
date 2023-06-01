
odoo.define('marigold_composter.dashboard', function(require) {
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var ajax = require("web.ajax");

    var MarigoldBarChartWidget = PublicWidget.Widget.extend({

        selector: '.marigold_bar_chart',
        
        start: function() {
            self = this;
            rpc.query({
                route: '/mc/barchart/chartdata',
                params: {},
            }).then(function (result) {
               self.drawChart(result)
            });
        },

        drawChart : function(result) {
            let labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            let barColors = ['Red', 'SlateGrey', 'Tan','MediumSeaGreen','Violet','Olive','Orange','Peru','SandyBrown','Teal']
            let data = [];
            let dataSets = []

            labels.forEach((item,index)=>{
                data.push(result.waste_collected[item] !== undefined ? result.waste_collected[item] : 0 )

                })

            let counter = 0;
            for (key in result.formTwoData){
                dataSets.push({
                    label: key,
                    backgroundColor: barColors[counter],
                    borderColor: barColors[counter],
                    borderWidth: 1,
                    data: result.formTwoData[key]
                })
                counter++;
            }

            counter = 0;

            var ctx = $('#o_bar_chart_dashboard_canvas')[0].getContext('2d');
            var bar_chart_canvas = new Chart(ctx, {
                type: 'horizontalBar',
                data: {
                    labels : labels,
                    datasets: [{
 
                        label: 'Waste in Tons',
                        data: data,
                        backgroundColor: 'rgb(2, 120, 86)',
                        // borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            beginAtZero: true,
                            scaleLabel:{
                                display:true,
                                labelString: 'Waste in Tonns' 
                            },
                            gridLines:{
                                display: false
                            }

                        }],
                        yAxes: [{
                            scaleLabel:{
                                display:true,
                                labelString: 'Months' 
                            },
                            gridLines:{
                                display: false
                            }
                        }],
                    },
                    title: {
                        display: true,
                        text: 'Monthly Collected Waste ',
                        // position: "bottom"
                    }
                }
            });

            var graph2Context = $('#o_bar_chart_canvas_company')[0].getContext('2d');
            new Chart(graph2Context, {
                type: 'bar',
                data: {
                    labels : labels,
                    datasets: dataSets
                },
                options: {
                    scales: {
                        xAxes: [{
                            beginAtZero: true,
                            scaleLabel:{
                                display:true,
                                labelString: 'Months' 
                            },
                            gridLines:{
                                display: false
                            }

                        }],
                        yAxes: [{
                            scaleLabel:{
                                display:true,
                                labelString: 'Waste in Tonns' 
                            },
                            gridLines:{
                                display: false
                            }
                        }],
                    },
                    title: {
                        display: true,
                        text: 'Monthly Collected Waste by Groups',
                        // position: "bottom"
                    }
                }
            });
        },
    });
    PublicWidget.registry.marigold_composter_chart = MarigoldBarChartWidget;
    return MarigoldBarChartWidget;
});
