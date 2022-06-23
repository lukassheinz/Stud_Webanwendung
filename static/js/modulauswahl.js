$(document).ready(function (){

    $(".li").click(function(){
        $.ajax({
            url: "/modulauswahl",
            type: "get",
            contentType: "application/json",
            data: {
                value: $(this).val(),
                //selectedModules: $(".semester-list").children().text(),
                selectedModules: $(".semester-list").children().attr("value")

            },
            success: function(response){
                $(".semester-list").append("<li value = " + response.ID + ">" + response.modultitel + "</li>")
            }
        })

    })

    $(".weiterbutton").click(function(){
        $.ajax({
            url: "/modulauswahl",
            type: "get",
            contentType: "application/json",
            data: {
                button_text: $(this).text()
            }
        })

    })

})