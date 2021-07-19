$(document).on('keypress',function(e) {
    if(e.which == 13) {
        $("#kioskForm").submit();
    }
});

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
    hideElements();
  }
  $('#submitScannerData').focus();
};

function submitData(){
  var eventid = $("#eventid".val())
  var bNumber = $("#submitScannerData").val()
  console.log(eventid)
  console.log($("#submitScannerData").val().length);
  // if ($("#submitScannerData").val().length > 20){
  $.ajax({
    method: "POST",
    url: '/'+ eventid + '/signintoKiosk',
    data: bNumber,
    success: function(response) {
      msgFlash(flasherMessage, "success")
      // console.log(flasherMessage)
    },
    error: function(request, status, error) {
      console.log(status,error);
      msgFlash(flasherMessage, "danger")
      // console.log(flasherMessage)
    }
  })
  // }
}

function hideElements(hide=true) {

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
