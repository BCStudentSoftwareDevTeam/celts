function enterFullscreen() {
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

function submitData() {
  console.log($("#submitScannerData").val().length);
  if ($("#submitScannerData").val().length > 20){
    $("#kioskForm").submit()
  }
}

function hideElements(hide=true) {

  if (hide == true) {

    $("footer").hide();
    $("nav").animate({ opacity: 0 }, 1);
    $("a").hide();
    $("nav").css("width", "0.1rem")
  } else {
    $("footer").show()
    $("nav").animate({ opacity: 1 }, 1);
    $("a").show();
    $("nav").css("width", "inherit")
  }
}
