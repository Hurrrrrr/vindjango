"use strict";

let chart_data = document.body.dataset.chartData;
let colorDataString = document.body.dataset.colorData;
// turn the JSON string into JS object
// this is stupid but it won't work without it
colorDataString = he.decode(colorDataString);
colorDataString = colorDataString.replace(/'/g, '"');
const color_data = JSON.parse(colorDataString);
const chartColor = "rgb(" + color_data.appearance_red +
                        "," + color_data.appearance_green +
                        "," + color_data.appearance_blue + ")";

window.drawChart = function() {

    if (chart_data) {

        let chartDataString = JSON.parse('"' + chart_data + '"');
        chart_data = JSON.parse(chartDataString);

        let svg = d3.select("#chart")
            .append("svg")
            .attr("width", 500)
            .attr("height", 300);

        const x = d3.scaleBand()
            .domain(Object.keys(chart_data))
            .range([0, 500])
            .padding(0.1);

        const y = d3.scaleLinear()
            .domain([0, 255])
            .range([300, 0]);
        
        const tickValues = [25, 75, 125, 175, 225];
        const tickLabels = ['Low', 'Med-Low', 'Med', 'Med-High', 'High'];

        let yAxisGroup= svg.append("g")
            .attr("transform", "translate(50,0)");
        
        yAxisGroup.call(d3.axisLeft(y)
            .tickValues(tickValues)
            .tickFormat(function(d, i) { return tickLabels[i]; }))

        svg.selectAll(".bar")
            .data(Object.entries(chart_data))
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d[0]); })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return 300 - y(d[1]); })
            .attr("fill", chartColor)
            .attr("stroke", "black")
            .attr("stroke-width", 1);

        svg.append("g")
            .attr("transform", "translate(0," + 300 + ")")
            .call(d3.axisBottom(x));

        } else {
            console.log("chart_data does not exist");
        }
    }

window.autocomplete = function() {
    $(document).ready(function(){
        $( function() {
            $( ".autocomplete" ).each(function() {
                const availableChoices = JSON.parse($(this).attr('data-choices'));
                $(this).autocomplete({
                    source: availableChoices
                });
            });
        });
    });
}