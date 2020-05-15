$(document).ready(function () {
    var $form = $("#registrationForm");
    var $input = $('#id_contactNumber');
    $input.on("keyup", function (event) {


        // 1
        var $this = $(this);
        var input = $this.val();

        // 2
        var input = input.replace(/[\D\s\._\-]+/g, "");


        // 3
        var split = 3;
        var chunk = [];

        for (var i = 0, len = input.length; i < len; i += split) {
            split = (i >= 4 && i <= 10) ? 4 : 3;
            chunk.push(input.substr(i, split));
        }

        // 4
        $this.val(function () {
            return chunk.join("-").toUpperCase();
        });

    });
});
