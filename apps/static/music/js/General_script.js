$(document).ready(function () {
    $(".form-control").css("border-radius", "0px !important");
    $(".form-control").attr("autocomplete", "off");
    $(".card").addClass("shadow");
    $("select").addClass("form-control");
    $(".mx-auto .card").addClass("mt-5");
    $(".mx-auto .card").addClass("mb-5");
    $("label").addClass("font-weight-bold");

});


$(document).ready(function () {
    $('.btn').removeClass('activated'); //eventually removeClass of some previous class
});

$('.btn').on('click', function () {
    $('.btn').removeClass('activated'); //eventually removeClass of some previous class
    //other stuff
});