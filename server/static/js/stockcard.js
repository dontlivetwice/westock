ticker = "{{ stock.get('ticker') }}";
name = "{{ stock.get('name') }}";
time = "{{ stock.get('time') }}";
about = "{{ stock.get('about') }}";

open = "{{ stock.get_open() }}";
days_high = "{{ stock.get_days_high() }}";
days_low = "{{ stock.get_days_low() }}";
year_high = "{{ stock.get_year_high() }}";
year_low = "{{ stock.get_year_low() }}";
volume = "{{ stock.get_volume() }}";
market_cap = "{{ stock.get_market_cap() }}";
pe_ratio = "{{ stock.get_pe_ratio() }}";
div_yield = "{{ stock.get_div_yield() }}";
change = "{{ stock.get_change() }}";
change_percent = "{{ stock.get_change_percent() }}";
is_owned = "{{ stock.is_owned }}";

addStockNode(ticker, name, time, about, is_owned, open, days_high, days_low, year_high, year_low, volume,
market_cap, pe_ratio, div_yield, change, change_percent);

if (change <= 0) {
    var data = {
        labels: {{ stock.get_price_labels() }},
        datasets: [
            {
                label: ticker,
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "#d10808",
                pointColor: "#d10808",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: {{ stock.get_price_values() }}
            }
        ]
    };
} else {
     var data = {
        labels: {{ stock.get_price_labels() }},
        datasets: [
            {
                label: ticker,
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "#099422",
                pointColor: "#099422",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: {{ stock.get_price_values() }}
            }
        ]
    };
}

// Get the context of the canvas element we want to select
var ctx = document.getElementById(ticker+'Chart').getContext("2d");

var options = {
    ///Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : true,

    //String - Colour of the grid lines
    scaleGridLineColor : "rgba(0,0,0,.05)",

    //Number - Width of the grid lines
    scaleGridLineWidth : 1,

    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,

    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: true,

    //Boolean - Whether the line is curved between points
    bezierCurve : true,

    //Number - Tension of the bezier curve between points
    bezierCurveTension : 0.4,

    //Boolean - Whether to show a dot for each point
    pointDot : false,

    //Number - Radius of each point dot in pixels
    pointDotRadius : 4,

    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth : 1,

    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius : 20,

    //Boolean - Whether to show a stroke for datasets
    datasetStroke : false,

    //Number - Pixel width of dataset stroke
    datasetStrokeWidth : 2,

    //Boolean - Whether to fill the dataset with a colour
    datasetFill : false,
};
var chart = new Chart(ctx).Line(data, options);

var follow = document.getElementById(ticker);
follow.addEventListener("click", followUnfollowStock, true);