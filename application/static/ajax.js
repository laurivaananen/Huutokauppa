var next_page = $("#load-items-button").attr("name");

function list_items (items, table) {
    for (i = 0; i < items.length; i++) {
        var name = "<td><a href='" + $SCRIPT_ROOT + "/items/" + items[i]["id"] + "'>" + items[i]["name"] + "</a></td>";

        var starting_price = "<td>" + items[i]["starting_price"] + "</td>";

        if (items[i]["latest_bid"]){
            var latest_bid = "<td>" + items[i]["latest_bid"] + "</td>";
        } else {
            var latest_bid = "<td class='info-text'>No bids yet</td>";
        }

        if (items[i]["bidding_time_left"]["hours"] > 24) {
            var bidding_time_left = "<td>" + items[i]["bidding_end"] + "</td>";
        } else {
            var bidding_time_left = "<td>" + items[i]["bidding_time_left"]["hours"] + "h ";

            if (items[i]["bidding_time_left"]["minutes"] > 0) {
                bidding_time_left +=  items[i]["bidding_time_left"]["minutes"] + "m ";
            }
            if (items[i]["bidding_time_left"]["seconds"] > 0) {
                bidding_time_left +=  items[i]["bidding_time_left"]["seconds"] + "s";
            }
            bidding_time_left += "</td>"
        }

        var quality = "<td>" + items[i]["quality"] + "</td>";

        var seller = "<td><a href='" + $SCRIPT_ROOT + "/user/" + items[i]["seller_id"] + "'>" + items[i]["seller"] + "</a></td>";

        table.append("<tr>" + name +  starting_price +  latest_bid + bidding_time_left + quality + seller + "</tr>")
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
        list_items(data.items, $('#item-ajax-table')),
        check_page(next_page)
    });
    return false;
};

function start () {
    $.getJSON($SCRIPT_ROOT + '/loaditems', {
        page: next_page
    }, function(data) {
        next_page = data.next_page,
        create_table(data.items),
        list_items(data.items, $('#item-ajax-table')),
        check_page(next_page)
    });
    return false;
}

start();
