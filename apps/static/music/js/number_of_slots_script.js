
    $(document).ready(function()
    {
        // console.log($("number_of_slots").val());
        $(document).on("change", "#exampleFormControlSelect1", function()
        {
            var elem_1 = $(this).children("option:selected").val();
            var elem_2 = $("#payment").attr("data");
            var elem_3 = $("#total").attr("data");
            $("#total").html("$" +  (elem_1 * elem_2));
        });

            var elem_1 = $("#exampleFormControlSelect1").children("option:selected").val();
            var elem_2 = $("#payment").attr("data");
            var elem_3 = $("#total").attr("data");
            $("#total").html("$" +  (elem_1 * elem_2));
            if ($("#total").html() == "$NaN")
            {
                $("#total").html("$" + "0");
            }

    });

