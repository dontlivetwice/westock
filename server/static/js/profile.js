$('#interestModal').modal()

var form = document.forms.namedItem("interest-form");

form.addEventListener('submit', function(ev) {

  var oData = new FormData(form);

  var oReq = new XMLHttpRequest();

  oReq.open("POST", "/interests/", false);

  oReq.onload = function(oEvent) {
    if (oReq.status == 200) {
        // close dialog on success
        $('#interestModal').modal('hide');

        // re-direct to home page
        window.location.href = "/"
    } else {
    }
  };

  oReq.send(oData);
  ev.preventDefault();
}, false);
