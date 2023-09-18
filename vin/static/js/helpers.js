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
            .attr("width", 1200)
            .attr("height", 630);

        const x = d3.scaleBand()
            .domain(Object.keys(chart_data))
            .range([0, 1100])
            .padding(0.1);

        const y = d3.scaleLinear()
            .domain([0, 255])
            .range([600, 0]);
        
        const tickValues = [25, 75, 125, 175, 225];
        const tickLabels = ['Low', 'Med-Low', 'Med', 'Med-High', 'High'];

        let yAxisGroup= svg.append("g")
            .attr("transform", "translate(100,0)");
        
        yAxisGroup.call(d3.axisLeft(y)
            .tickValues(tickValues)
            .tickFormat(function(d, i) { return tickLabels[i]; }))
            .selectAll("text")
            .style("font-size", "16px");

        svg.selectAll(".bar")
            .data(Object.entries(chart_data))
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d[0]) + 100; })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return 600 - y(d[1]); })
            .attr("fill", chartColor)
            .attr("stroke", "black")
            .attr("stroke-width", 1.5);
        
        const xLabels = ["Sweetness", "Acidity", "Body", "Alcohol", "Tannin/Bitterness", "Finish"];
    
        svg.selectAll(".label")
            .data(xLabels)
            .enter().append("text")
            .attr("class", "label")
            .attr("x", function(d, i) { return x(Object.keys(chart_data)[i]) + 100 + x.bandwidth()/ 2; })
            .attr("y", 620)
            .attr("text-anchor", "middle")
            .text(function(d) { return d; })
            .style("font-size", "16px");

        let xAxisGroup = svg.append("g")
            .attr("transform", "translate(100," + 600 + ")")
            .call(d3.axisBottom(x));
        
        xAxisGroup.selectAll("text").remove();

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