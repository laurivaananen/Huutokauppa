var next_page = $("#load-items-button").attr("name");

function list_items (items, table) {
    console.log("Starting to list on " + table)
    for (i = 0; i < items.length; i++) {
        console.log(items[i]["name"]);
        var name = "<h2><a href='" + $SCRIPT_ROOT + "/items/" + items[i]["id"] + "'>" + items[i]["name"] + "</a></h2>";

        var image = "<a href='" + $SCRIPT_ROOT + "/items/" + items[i]["id"] + "'><img src=" + items[i]["image_url"] + " alt=" + items[i]["name"] + "></a>"

        var starting_price = "<td>" + items[i]["starting_price"] + "</td>";

        if (items[i]["latest_bid"]){
            var latest_bid = "<h3 class='time-normal'>$ " + items[i]["latest_bid"] + "</h3>";
        } else {
            var latest_bid = "<p class='info-text'>No bids yet</p>";
        }

        if (items[i]["bidding_time_left"]["hours"] > 24) {
            var bidding_time_left = "<h3 class='time-normal'>" + items[i]["bidding_end"] + "</h3>";
        } else {
            console.log(items[i]["bidding_time_left"]["minutes"]);
            console.log("Something else");
            if (items[i]["bidding_time_left"]["hours"] <= 0) {
                console.log("No hours");
                if (items[i]["bidding_time_left"]["minutes"] <= 0) {
                    console.log("No minutes");
                    if (items[i]["bidding_time_left"]["seconds"] <= 0) {
                        console.log("No seconds");
                        var bidding_time_left = "<h3 class='time-normal'>"
                    } else {
                        var bidding_time_left = "<h3 class='time-danger'>"
                    }
                } else {
                    var bidding_time_left = "<h3 class='time-close'>"
                }
            } else {
                var bidding_time_left = "<h3 class='time-far'>"
            }

            console.log(bidding_time_left);

            if (items[i]["bidding_time_left"]["hours"] > 0) {
                bidding_time_left +=  items[i]["bidding_time_left"]["hours"] + "h ";
            }
            if (items[i]["bidding_time_left"]["minutes"] > 0) {
                bidding_time_left +=  items[i]["bidding_time_left"]["minutes"] + "m ";
            }
            if (items[i]["bidding_time_left"]["seconds"] > 0) {
                bidding_time_left +=  items[i]["bidding_time_left"]["seconds"] + "s";
            }
            bidding_time_left += "</h3>"
        }

        console.log(bidding_time_left);
        console.log(latest_bid);

        var quality = "<h3>" + items[i]["quality"] + "</h3>";

        var seller = "<td><a href='" + $SCRIPT_ROOT + "/user/" + items[i]["seller_id"] + "'>" + items[i]["seller"] + "</a></td>";

        table.append("<div class='item-container'>" + name + image +  bidding_time_left + latest_bid + "</div>")
    }
};

function check_page (next_page) {
    if (next_page == null) {
        $("#load-items-button").hide();
    }
};

function create_table (items) {
    console.log(items.length === 0);
    if (items.length > 0) {
        $("#item-ajax-div").append('<table class="detail-table-vertical" id="item-ajax-table">'
        +'<tr>'
        +    '<th>Item</th><th>Starting price</th><th>Latest bid</th><th>Auction ends</th><th>Quality</th><th>Seller</th>'
        +'</tr>');
    } else {
        $("#item-ajax-div").append('<p class="info-text empty-table">No items found</p>');
    }
};

document.getElementById("load-items-button").onclick = function am () {
    $.getJSON($SCRIPT_ROOT + '/loaditems', {
        page: next_page
    }, function(data) {
        next_page = data.next_page,
        list_items(data.items, $('#item-ajax-div')),
        check_page(next_page)
    });
    return false;
};

function start () {
    console.log("Starting");
    console.log(next_page);
    $.getJSON($SCRIPT_ROOT + '/loaditems', {
        page: 1
    }, function(data) {
        next_page = data.next_page,
        console.log(next_page);
        // create_table(data.items),
        list_items(data.items, $('#item-ajax-div')),
        check_page(next_page)
    });
    return false;
}

start();
