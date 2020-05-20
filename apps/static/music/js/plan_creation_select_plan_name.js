function PlanCreationFunction(x, y) {


  // console.log(x, y);
  // console.log(j);
  // console.log($("#id_category option:contains(j)"));
  // $("#id_category option:contains(j)");
  $('#id_category').val(y).trigger('change');
  
  for (var i = 0; i < $("#selectContains").find("select").length; i++) {





    if ($($("#selectContains").find("select")[i]).attr("id") == ("id_plan_name_" + x + "")) {


      $($("#selectContains").find("select")[i]).show();
    } else {
      $($("#selectContains").find("select")[i]).hide();
    }
  }


}