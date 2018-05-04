function list_items (items, table) {
    for (i = 0; i < items.length; i++) {
        var name = "<h3><a href='" + $SCRIPT_ROOT + "/items/" + items[i]["id"] + "'>" + items[i]["name"] + "</a></h3>";

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
            if (items[i]["bidding_time_left"]["hours"] <= 0) {
                if (items[i]["bidding_time_left"]["minutes"] <= 0) {
                    if (items[i]["bidding_time_left"]["seconds"] <= 0) {
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

        var quality = "<h3>" + items[i]["quality"] + "</h3>";

        var seller = "<td><a href='" + $SCRIPT_ROOT + "/user/" + items[i]["seller_id"] + "'>" + items[i]["seller"] + "</a></td>";

        table.append("<div class='item-container'>" +  image + name +  bidding_time_left + latest_bid + "</div>")
    }
};

function call_ajax(obj) {
    var current_obj = obj,
        url = current_obj.attr('action'),
        method = current_obj.attr('method'),
        data = {};

    current_obj.find('[name]').each(function(index, value) {
        var that = $(this),
            name = that.attr('name'),
            value = that.val();

        data[name] = value;
    });

    $.ajax({
        url: url,
        type: method,
        data: data,
        success: function(response) {
            list_items(response.items, $('#item-ajax-div'));
            check_page(response.next_page);
            item_counter(response.item_count);
        }
    });

    return false;
};

function item_counter (item_count) {
    $('#item-counter').empty();
    if (item_count == 1){
        $('#item-counter').text("Found 1 item");
    } else {
        $('#item-counter').text("Found " + item_count + " items");
    }
};

$('#item-search-form').on('submit', function() {
    $('#item-search-form').data('changed', false);
    $('#item-ajax-div').empty();
    $("#page").val(1);
    call_ajax($('#item-search-form'));
    return false;
});

$('#load-items-form').on('submit', function() {
    if($('#item-search-form').data('changed')){
        $('#item-ajax-div').empty();
        $("#page").val(1);
        $('#item-search-form').data('changed', false);
    }
    call_ajax($('#item-search-form'));
    return false;
});

call_ajax($('#item-search-form'));

function check_page (next_page) {
    if (next_page == null) {
        $("#load-items-form").hide();
    } else {
        $("#load-items-form").show();
        $("#page").val(next_page++);
    }
};

$("#item-search-form :input").change(function() {
    $(this).closest('form').data('changed', true);
});
