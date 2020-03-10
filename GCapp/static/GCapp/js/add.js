function addcollection(game_id) {
    console.log(game_id);
    $.ajax({
        type: 'post',
        dataType: "json",
        url: "/GCapp/add/",
        data: {
            game_id: game_id,
        },
        success: function (data) {
            location.reload();
        },
        error: function (jqXHR) {
            console.log("Error: " + jqXHR.status);
        }
    });
}