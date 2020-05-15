
    function hasLowerCase(str) {
        return str.toUpperCase() != str;
    }

    function hasUpperCase(str) {
        return str.toLowerCase() != str;
    }

    function testPasswRegexp3(passw) {
        const extraStrong = /(?=.*[\!@#$%^&*()\\[\]{}\-_+=~`|:;"'<>,./?])/g;
        return extraStrong.test(passw);

    };

    function testPasswRegexpNumeric(passw) {
        const extraStrong = /(?=.*[\d])/g;
        return extraStrong.test(passw);

    };

    function checkConditoin() {
        var i = $("#id_password").val();
        if (hasLowerCase(i)) {
            $("#customCheck1").prop("checked", true);
        }
        else {
            $("#customCheck1").prop("checked", false);
        }
        if (hasUpperCase(i)) {
            $("#customCheck2").prop("checked", true);
        }
        else {
            $("#customCheck2").prop("checked", false);
        }

        if (i.length > 9) {
            $("#customCheck5").prop("checked", true);
        }
        else {
            $("#customCheck5").prop("checked", false);
        }

        if (testPasswRegexp3(i)) {

            $("#customCheck4").prop("checked", true);
        }
        else {
            $("#customCheck4").prop("checked", false);
        }

        if (testPasswRegexpNumeric(i)) {
            $("#customCheck3").prop("checked", true);
        }
        else {
            $("#customCheck3").prop("checked", false);
        }

    }