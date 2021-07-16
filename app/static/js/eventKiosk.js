function enterFullscreen() {
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
};

$('#submitScannerData').on('change', function() {
  console.log("Worked");
  $(this).closest('form').submit();
});
//
// function submitData() {
//   console.log("Created");
//   $('#kioskForm').delay(200).submit();
//   $('')
// }
