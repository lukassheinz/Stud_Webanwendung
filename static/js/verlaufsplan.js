$(document).ready(function () {
    $(".flex-item.modul").click(function () {
        $.ajax({
            url: "/verlaufsplan",
            type: "get",
            contentType: "application/json",
            data: {
                class: $(this).attr("class"),
                value: $(this).attr("value"),
                semester: $(this).parent(this).attr("value")
            },
            success: function (response) {
                $("body").load("verlaufsplan");
            },
            error: function () {
                $("body").load("verlaufsplan");
            }
        })
    })
})