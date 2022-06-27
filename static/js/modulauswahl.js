$(document).ready(function (){

    $(".li").click(function(){
/*
        my_arr = []
        $(".semester-list").children().each(function(){
            my_arr.push($(this).attr("id"))
            console.log(my_arr)
        })

    */

        $.ajax({
            url: "/modulauswahl",
            type: "get",
            contentType: "application/json",
            data: {
                value: $(this).val(),
                //text: $(this).text(),
                //selectedModules: $(".semester-list").children().text(),
                //selectedModules: $(".semester-list").children("*").attr("id")
                //selectedModules: my_arr.join(",")
            },
            success: function(response){

                $( "body").load("modulauswahl")
            },
            error: function(){
                alert("Duplikat")
            }
        })


    })

    $(".semester-list").click(function(){
/*
        my_arr = []
        $(".semester-list").children().each(function(){
            my_arr.push($(this).attr("id"))
            console.log(my_arr)
        })

 */

        $.ajax({
            url: "/modulauswahl",
            type: "get",
            contentType: "application/json",
            data: {
                value: $(this).val(),
                class: $(this).attr("class"),
                id: $(this).attr("id")
                //text: $(this).text(),
                //selectedModules: $(".semester-list").children().text(),
                //selectedModules: $(".semester-list").children("*").attr("id")
                //selectedModules: my_arr.join(",")
            },
            success: function(response){
                $( "body").load("modulauswahl")
            },
            error: function(){
                alert("Duplikat")
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