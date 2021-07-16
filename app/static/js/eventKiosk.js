function enterFullscreen() {
  if($("#fullscreenCheck").prop("checked") == false){
    document.cancelFullScreen
    || document.webkitCancelFullScreen
    || document.mozCancelFullScreen
  }
  else{
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

function submitData() {
  console.log($("#submitScannerData").val().length);
  if ($("#submitScannerData").val().length > 20){
    $("#kioskForm").submit()
  }
}
