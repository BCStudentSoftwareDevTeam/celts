$(document).keydown(function(e){
    if (e.key === "Escape") {
        $("#fullscreenCheck").prop("checked", false)
        toggleFullscreen();
    }
});

$(document).ready(function(e) {
    $("#submitScannerData").focus();

    $("#submitScannerData").keydown(function(e) {
        if (e.key === "Enter") {
            submitData();
        }
    });

    //  Opens the camera to scan the ID
    $('.qr-reader-button').on("click", function() {
      $('#qr-reader').toggle()
      let lastResult, countResults = 0;
      let onScanSuccess = function(decodedText, decodedResult) {
          if (decodedText && decodedText.length > 9 && decodedText !== lastResult) {
              lastResult = decodedText;
            
              $("#submitScannerData").val(decodedText)
              submitData();
          } else {
            message = decodedText + " Invalid B-number"
            flasherStatus = "danger"
          }
      }
      let qrboxFunction = function(viewfinderWidth, viewfinderHeight) {
        let minEdgePercentage = 0.9; // 90%
        let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
        let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
        return {
            width: qrboxSize,
            height: qrboxSize
        };
      }
      let scanner = new Html5QrcodeScanner("qr-reader", { 
                  fps: 2, 
                  qrbox: qrboxFunction, 
                  preferFrontCamera: false,
                  facingMode: { exact: "environment" },
                  useBarCodeDetectorIfSupported: true,
              }, true);
      scanner.render(onScanSuccess);

      
      // we have to delay this so that the element exists before we try to add the event
      window.setTimeout(function() {
          $('#html5-qrcode-button-camera-stop').on("click", function() {
            $('#qr-reader').toggle()
          })}, 500);
    })

});

function submitData(){
    $(".alert").remove()
    $.ajax({
      method: "POST",
      url: '/signintoEvent',
      data: {
        "eventid": $("#eventid").val(),
        "bNumber": $("#submitScannerData").val()
      },

      success: function(resultID) {
        if (resultID.status == "already signed in") {
          msgFlash(`${resultID.user} already signed in!`, "warning");
        } else if (resultID.status === "banned") {
          msgFlash(`${resultID.user} is ineligible!`, "danger");
        } else if (resultID.status === "does not exist") {
          msgFlash("User does not exist", "danger");
        } else {
          msgFlash(`${resultID.user} successfully signed in!`, "success");
        }
        $("#submitScannerData").val("").blur();
      },

      error: function(request, status, error) {
        console.log(status, error);
        msgFlash("See Attendant; Unable to sign in.", "danger");
        $("#submitScannerData").val("").blur();
      }
    })
}

function disabledElements(disabled) {
  if (disabled== true) {

    // $("footer").disabled();
    // $("kiosk-disabled").animate({ opacity: 0 }, 1);
    // $("kiosk-disabled").css("width", "0");
    // $("kiosk-disabled").prop("disabled", true);
    // $("a").disabled();
    $("col-md-auto d-print-none d-lg-none").css("width", "0");
  } 
  // else {
  //   $(".footer").show();
  //   $("kiosk-disabled").css("width", "inherit");
  //   $("kiosk-disabled").animate({ opacity: 1 }, 1);
  //   $("kiosk-disabled").prop("disabled", false);
  //   $("a").show();
  //   $("nav").css("width", "inherit");
  // }
}

// Source: https://stackoverflow.com/questions/1125084/how-to-make-the-window-full-screen-with-javascript-stretching-all-over-the-screen
function toggleFullscreen() {
  if($("#fullscreenCheck").prop("checked") == false){
    disabledElements(false);
    document.exitFullscreen() || document.webkitExitFullscreen() || document.msExitFullscreen()
  } else {
    disabledElements(true);

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

