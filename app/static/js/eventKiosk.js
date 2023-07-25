$(document).keydown(function(e){
  if (e.key === "Escape") {
    $("#fullscreenCheck").prop("checked", false)
    toggleFullscreen();
  }
  else if(e.key === "Enter") {
      submitData(true);
  }
});
// Source: https://stackoverflow.com/questions/1125084/how-to-make-the-window-full-screen-with-javascript-stretching-all-over-the-screen
function toggleFullscreen() {
  if($("#fullscreenCheck").prop("checked") == false){
    hideElements(false);
    document.exitFullscreen()
    || document.webkitExitFullscreen()
    || document.msExitFullscreen()
  }
  else{
    hideElements(true);
    var el = document.documentElement
    , rfs = // for newer Webkit and Firefox
    el.requestFullscreen
    || el.webkitRequestFullScreen
    || el.mozRequestFullScreen
    || el.msRequestFullscreen
    ;
    if(typeof rfs!="undefined" && rfs){
      rfs.call(el);
    } else if(typeof window.ActiveXObject!="undefined"){
      // for Internet Explorer
      var wscript = new ActiveXObject("WScript.Shell");
      if (wscript!=null) {
        wscript.SendKeys("{F11}");
      }
    }
  }
  $('#submitScannerData').focus();
};

function eventFlasher(flash_message, status){
    if (status === "success") {
        category = "success";
        $("#signinData").append("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+flash_message+"</div>");
        $("#flasher").delay(5000).fadeOut();
    }
    else {
        category = "danger";
        $("#signinData").append("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+flash_message+"</div>");
        $("#flasher").delay(5000).fadeOut();
    }

}
var resultContainer = document.getElementById('qr-reader-results');
var lastResult, countResults = 0;

function onScanSuccess(decodedText, decodedResult) {
    if (decodedText !== lastResult) {
        ++countResults;
        lastResult = decodedText;
        // Handle on success condition with the decoded message.
        console.log(`Scan result ${decodedText}`, decodedResult);
    }
}

var html5QrcodeScanner = new Html5QrcodeScanner(
    "qr-reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);

function submitData(hitEnter = false){
  if(hitEnter){
    $("#flasher").remove()
    $.ajax({
      method: "POST",
      url: '/signintoEvent',
      data: {
        "eventid": $("#eventid").val(),
        "bNumber": $("#submitScannerData").val()
      },
      success: function(result) {
        flasherStatus = "success"
        if (result.status == "already in") {
          message = result.user + " Already Signed In!"
        } else if (result.status === "banned") {
          message = result.user + " is ineligible."
          flasherStatus = "danger"
        } else if (result.status === "does not exist") {
          message = "User does not exist"
          flasherStatus = "danger"
        } else {
          message = result.user + " Successfully Signed In!"
        }
        eventFlasher(message, flasherStatus);
        $("#submitScannerData").val("").blur();
        $('#submitScannerData').focus();
      },
      error: function(request, status, error) {
        console.log(status, error);
        eventFlasher("See Attendant; Unable to Sign In.", "danger");
        $("#submitScannerData").val("").blur();
        $('#submitScannerData').focus();
      }
    })
  }
}

function hideElements(hide) {

  if (hide == true) {

    $("footer").hide();
    $("button").animate({ opacity: 0 }, 1);
    $("button").css("width", "0");
    $("button").prop("disabled", true);
    $("a").hide();
    $("nav").css("width", "0");
  } else {
    $("footer").show();
    $("button").css("width", "inherit");
    $("button").animate({ opacity: 1 }, 1);
    $("button").prop("disabled", false);
    $("a").show();
    $("nav").css("width", "inherit");
  }
}
