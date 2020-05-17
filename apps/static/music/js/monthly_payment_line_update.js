function updateLine(){
    var v = $("#id_currently_monthly_payment_per_line").val().trim();
    if (v.length == 0)
    {
      $("#currentLinePayment").hide();
    }
    else{
      $("#currentLinePayment").show();
    }
    var c =  $("#id_category :selected").text();
    var j  = 0
    if (c == "VERIZON")
    {
      j = ( v-30 )*12;
    }
    else if(c == "T-MOBILES")
    {
      j = ( v-28 )*12;
    }
    else if(c == "AT-T")
    {
      j = ( v-35 )*12;
    }
    
    var r  ="Great! We can save you about $" +  j + " per line a year."
    $("#currentLinePayment").html(r);
  }