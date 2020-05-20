// Set up Stripe.js and Elements to use in checkout form
var stripe = Stripe('pk_test_7Caol5AeV11tgvLYCf7FlGXr00hMYbhIfm');

var elements = stripe.elements();

var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '25px',
    '::placeholder': {
      color: '#aab7c4',
    },
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a',
  },
};

var cardElement = elements.create('card', { style: style });
cardElement.mount('#card-element');
var form = document.getElementById('subscription-form');
//------------------------------------------------------------------------------

var first_name = document.getElementById('first_name');
var last_name = document.getElementById('last_name');
var Phone_number = document.getElementById('Phone_number');
var emailid = document.getElementById('emailid');
var City = document.getElementById('City');
var State = document.getElementById('State');
var Country = document.getElementById('Country');


//-------------------------------------------------------------------------------


form.addEventListener('submit', function(event) {
  // We don't want to let default form submission happen here,
  // which would refresh the page.
  event.preventDefault();
  
  stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
    billing_details: {
      email: emailid.value,
      name:(first_name.value).concat(last_name.value) 
      ,
      phone:Phone_number.value,
      address: {
        "city": City.value,
        "country": Country.value,
        "postal_code": null,
        "state": State.value
      },
     
    },


  }).then(stripePaymentMethodHandler);
});

function stripePaymentMethodHandler(result, email) {
  // **************** Billing Address **************************** //
  var B_address_line1 = document.getElementById('B_address_line1');
  var B_address_line2 = document.getElementById('B_address_line2');
  var B_City = document.getElementById('B_City');
  var B_State = document.getElementById('B_State');
  var B_Postal_code = document.getElementById('B_Postal_Code');
  var B_Country = document.getElementById('B_Country');

  // **************** Shipping Address **************************** //
  var C_address_line1 = document.getElementById('C_address_line1');
  var C_address_line2 = document.getElementById('C_address_line2');
  var C_City = document.getElementById('C_City');
  var C_State = document.getElementById('C_State');
  var C_Postal_code = document.getElementById('C_Postal_Code');
  var C_Country = document.getElementById('C_Country');


  if (result.error) {
    alert((result))
  } else {
    // Otherwise send paymentMethod.id to your server
    fetch('/charge', {
      method: 'post',
      credentials: "same-origin",
      headers: {'Content-Type': 'application/json'},
      
      body: JSON.stringify({
        
        payment_method: result.paymentMethod.id,
        card: result.paymentMethod.card,
        details: result.paymentMethod.billing_details,
        //    ********* Billing Address *************** //
        B_address_line1: B_address_line1.value,
        B_address_line2: B_address_line2.value,
        B_City: B_City.value,
        B_State:B_State.value,
        B_Postal_code:B_Postal_code.value,
        B_Country:B_Country.value,
        //    ********* Shipping Address *************** //
        C_address_line1: C_address_line1.value,
        C_address_line2: C_address_line2.value,
        C_City: C_City.value,
        C_State:C_State.value,
        C_Postal_code:C_Postal_code.value,
        C_Country:C_Country.value
        //    ****************************************** //
 

      }),
   
    }).then(function(result) {
     //window.open('http://127.0.0.1:8000/admin/')
      window.location.replace('/profile')
      return result.json();

    }).then(function(customer) {
      // 
    });
  }
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}