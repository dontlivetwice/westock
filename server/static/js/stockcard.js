
function addStockNode(ticker, name, time, about, is_owned, open, days_high, days_low, year_high, year_low,
    volume, market_cap, pe_ratio, div_yield, change, change_percent, followers) {

    var stockInfo = [open, volume, days_high, change_percent, days_low, market_cap, year_high, pe_ratio,
        year_low, div_yield];

    var stockInfoStrings = ["OPEN", "VOLUME", "HIGH", "CHANGE", "LOW", "MKT CAP", "52 WK HIGH", "P/E RATIO",
        "52 WK LOW", "DIV/YIELD"];

    var stock = document.createElement("div");
    stock.className = "col-md-4";

    var thumbnail = document.createElement("div");
    thumbnail.className = "thumbnail"
    stock.appendChild(thumbnail);

    var chartDiv = document.createElement("div");
    var chart = document.createElement('div');
    chart.id = ticker+'Chart';
    chartDiv.appendChild(chart);
    thumbnail.appendChild(chartDiv);

    var caption = document.createElement("div");
    caption.className = "caption";
    thumbnail.appendChild(caption);

    var title = document.createElement("H4");
    var text = document.createTextNode(ticker);
    title.appendChild(text);
    caption.appendChild(title);

    var sub_title = document.createElement("H5");
    var text = document.createTextNode(name);
    sub_title.appendChild(text);
    caption.appendChild(sub_title);

    var timeDiv = document.createElement("H6");
    var text = document.createTextNode(time);
    timeDiv.appendChild(text);
    caption.appendChild(timeDiv);

    <!-- start stock card -->
    var container = document.createElement("div");
    container.className = "container-fluid stockCard";

    for (var i = 0; i < stockInfo.length; i++) {
        stockInfo[i];

        if (i % 2 == 0) {
            var row = document.createElement("row");
            row.className = "row-fluid";
        }

        var col = document.createElement("div");

        if (i % 2 == 0) {
            col.className = "col-md-6 colCardLeft";
        } else {
            col.className = "col-md-6 colCardRight";
        }

        var valueDiv = document.createElement("P");
        valueDiv.className = 'text-left alignleft small';
        var text = document.createTextNode(stockInfoStrings[i] + ':');
        valueDiv.appendChild(text);
        col.appendChild(valueDiv);

        var valueDiv = document.createElement("P");
        valueDiv.className = 'text-right strong alignRight small';
        var text = document.createTextNode(stockInfo[i]);
        valueDiv.appendChild(text);
        col.appendChild(valueDiv);

        row.appendChild(col);

        if (i % 2 == 0) {
            container.appendChild(row);
        }
    }

    caption.appendChild(container);
    <!-- end stock card -->

    var aboutDiv = document.createElement("P");
    aboutDiv.className = 'collapse';
    var text = document.createTextNode(about);
    aboutDiv.appendChild(text);
    caption.appendChild(aboutDiv);

    var ul = document.createElement("ul");
    ul.className = 'list-inline'

    var link = document.createElement("li");

    var follow = document.createElement("A");
    follow.className = 'btn btn-primary';
    follow.id = ticker;
    follow.value = is_owned;
    follow.type = 'follow';

    var text = 'Follow';

    if (Boolean(is_owned)) {
        text = 'UnFollow';
    }

    textDiv = document.createTextNode(text);
    follow.appendChild(textDiv);
    link.appendChild(follow);
    ul.appendChild(link);

    var followerDiv = document.createElement("li");
    var valueDiv = document.createElement("P");
    valueDiv.className = 'text-right strong alignRight small';
    var text = document.createTextNode(followers);
    valueDiv.id = ticker + "Followers";
    valueDiv.appendChild(text);
    followerDiv.appendChild(valueDiv)
    ul.appendChild(followerDiv);

    var followerDiv = document.createElement("li");
    var valueDiv = document.createElement("P");
    valueDiv.className = 'text-right strong alignRight small';
    var text = document.createTextNode(" Followers");
    valueDiv.appendChild(text);
    followerDiv.appendChild(valueDiv)
    ul.appendChild(followerDiv);

    caption.appendChild(ul);
    var container = document.getElementById('stockContainer');
    container.appendChild(stock);
}