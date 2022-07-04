$(document).ready(function (){
    /*
    $.ajax({
        type: "GET",
        url: "modulauswahl",
        contentType: "application/json",
        data: {
            initializeCurrentSemester : 1
        },
        success:  function(response){
                $( "body").load("modulauswahl")
            },
            error: function(){
                $( "body").load("modulauswahl")
                alert("AKWJDN")
            }
    })*/

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
                $( "body").load("modulauswahl")
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
                $( "body").load("modulauswahl")
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

    $(".semester").click(function(){
        $.ajax({
            url:"/modulauswahl",
            type: "get",
            contentType: "application/json",
            data:{
                class: $(this).attr("class"),
                id: $(this).attr("id"),
            },
            success: function(response){
                $( "body").load("modulauswahl")
            },
            error: function(){
                $( "body").load("modulauswahl")
            }
        })
    })

})

function addSemester(){
    let semesterListe = document.querySelector(".semester-liste")
    let letztesSemester = document.querySelector(".semester-liste li:last-child")
    let letztesSemesterNr = letztesSemester.getAttribute("id")
    let newSemesterNr = parseInt(letztesSemesterNr) + 1;
    let entry = document.createElement("li")
    entry.setAttribute("class", "semester")
    entry.textContent = newSemesterNr + ". Semester"
    entry.setAttribute("id", newSemesterNr)
    semesterListe.appendChild(entry)
}

function deleteLastSemester(){
    let semesterListe = document.querySelector(".semester-liste")
    let letztesSemester = document.querySelector(".semester-liste li:last-child")
}

$(".semester-liste").on("click", "li", function(e){
    $(this).parent().find("li.active").removeClass("active");
    $(this).addClass("active");
})