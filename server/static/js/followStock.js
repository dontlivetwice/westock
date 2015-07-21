
function followUnfollowStock(obj, csrf_token) {
    var req = new XMLHttpRequest();

    req.onreadystatechange=function(evt) {
        if (req.readyState==4 && req.status==200) {
            var arrayResp = JSON.parse(req.response);

            var stock = document.getElementById(arrayResp.ticker);

            var count = 0;

            if (stock.text == "Follow") {
                stock.text = "UnFollow";
                count = 1;
            }
            else {
                stock.text = "Follow";
                count = -1;
            }

            var followers = document.getElementById(arrayResp.ticker+"Followers");
            followers.innerHTML = parseInt(followers.textContent) + count;
        }
        else if (req.readyState==4 && req.status!=200) {
            $('#errorModal').modal();
        }
      }

    var data = new FormData();
    data.append('ticker', obj.id);
    data.append('csrf_token', csrf_token);

    var method = '';

    if (obj.text == "Follow") {
        method = 'POST';
        url = '/me/following/stocks/'
    }
    else {
        method = 'DELETE';
        url = '/me/following/stocks/'+obj.id
    }

    req.open(method, url, true);
    req.send(data);
}

function drawGrid(stocks, is_owned){
    if (stocks != null) {
        for (i = 0; i < stocks.length; i++) {
            ticker = stocks[i].ticker;
            name = stocks[i].name;
            time = stocks[i].time;
            about = stocks[i].about;
            open = stocks[i].open;

            days_high = stocks[i].days_high;
            days_low = stocks[i].days_low;
            year_high = stocks[i].year_high;
            year_low = stocks[i].year_low;
            volume = stocks[i].volume;
            market_cap = stocks[i].market_cap;
            pe_ratio = stocks[i].pe_ratio;
            div_yield = stocks[i].div_yield;
            change = stocks[i].change;
            change_percent = stocks[i].change_percent;
            followers = stocks[i].followers;
            prices = stocks[i].prices;

            addStockNode(ticker, name, time, about, is_owned, open, days_high, days_low, year_high, year_low, volume,
            market_cap, pe_ratio, div_yield, change, change_percent, followers);

            google.setOnLoadCallback(drawChart(ticker, prices));

            var follow = document.getElementById(ticker);
            follow.addEventListener("click", function(){followUnfollowStock(this, "{{ csrf_token() }}")}, true);
        }
    }
}

function generateServerRequest(data, url, method, async, callback, args) {
    var req = new XMLHttpRequest();

    req.onreadystatechange=function(evt) {
        if (req.readyState==4 && req.status==200) {
            var arrayResp = JSON.parse(req.response);
            callback(arrayResp.data, args)
        }
        else if (req.readyState==4 && req.status!=200) {
            $('#errorModal').modal();
        }
      }

    req.open(method, url, async);

    if (data != null) {
        req.send(data);
    }
    else {
        req.send();
    }
}
