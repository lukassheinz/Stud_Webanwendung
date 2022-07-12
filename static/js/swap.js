$(document).ready(function () {
    $(".flex-item.modul").click(function () {
        $.ajax({
            url: "/swap",
            type: "get",
            contentType: "application/json",
            data: {
                class: $(this).attr("class"),
                value: $(this).attr("value"),
                semester: $(this).parent(this).attr("value")
            },
            success: function (response) {
                $("body").load("swap");
            },
            error: function () {
                $("body").load("swap");
            }
        })
    })
})