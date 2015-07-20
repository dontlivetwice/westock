google.load('visualization', '1.1', {packages: ['line']});

function drawChart(ticker, values) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', '');
    data.addColumn('number', ticker);

    data.addRows(values);

    var options = {
    legend: {position: 'none'},
    curveType: 'function',
    };

    var chart = new google.charts.Line(document.getElementById(ticker+"Chart"));

    var formatter = new google.visualization.NumberFormat({pattern: '0.00'});
    formatter.format(data, 1);

    chart.draw(data, options);
}
