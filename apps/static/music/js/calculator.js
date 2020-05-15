$(document).ready(function () {




    $('#savings_amount').html(" ");


    $("[name='totalcostAmount']").keyup(function (e) {
        e.preventDefault();
        var x = $('[name="options"]');
        var y = $('[name="accounts"]');
        var z = $('[name="totalcostAmount"]');
        var w = $('#savings_amount');
        var results = 0;
        if ($("#options1").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 30)) * 12;
        }

        if ($("#options2").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 30)) * 12;
        }

        if ($("#options3").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 35)) * 12;
        }



        if (results < 0) {
            results = "Looks like you already have a great deal! You might want to compare what you’re getting on your plan compared to one of ours";
            w.css("font-size", "14px");

            w.html(results);
        } else {
            if (isNaN(results)) {
                results = 0;
            }
            var R = "$" + results + "/year";
            w.html(R);
        }


    });


    $(document).on("change", "#customRange1", function () {

        $('[for="foo"]').css("left", "0px");
        var values = $(this).val() * 26.5 + "px";
        if ($(this).val() * 26.5 <= "133") {
            values = $(this).val() * 26.5 - "20" + "px";
        }
        $('[for="foo"]').css("left", values);
        $('[for="foo"]').html($(this).val())



        var x = $('[name="options"]');
        var y = $('[name="accounts"]');
        var z = $('[name="totalcostAmount"]');
        var w = $('#savings_amount');
        var results = 0;
        if ($("#options1").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 30)) * 12;
        }

        if ($("#options2").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 30)) * 12;
        }

        if ($("#options3").is(':checked')) {

            results = parseFloat(parseFloat(z.val()) - (parseInt(y.val()) * 35)) * 12;
        }



        if (results < 0) {
            results = "Looks like you already have a great deal! You might want to compare what you’re getting on your plan compared to one of ours";
            w.css("font-size", "14px");

            w.html(results);
        } else {
            if (isNaN(results)) {
                results = 0;
            }
            var R = "$" + results + "/year";
            w.html(R);
        }







    });


});