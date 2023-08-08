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
    $("#flasher").remove()
    $.ajax({
      method: "POST",
      url: '/signintoEvent',
      data: {
        "eventid": $("#eventid").val(),
        "bNumber": $("#submitScannerData").val()
      },

      success: function(resultID) {
        flasherStatus = "success"
        if (resultID.status == "already signed in") {
          message = resultID.user + " already signed in!"
          flasherStatus = "warning"

        } else if (resultID.status === "banned") {
          message = resultID.user + " is ineligible."
          flasherStatus = "danger"
          
        } else if (resultID.status === "does not exist") {
          message = "User does not exist"
          flasherStatus = "danger"
          
        } else {
          message = resultID.user + " successfully signed in!"
        }
        msgFlash(message, flasherStatus);
        $("#submitScannerData").val("").blur();
      },

      error: function(request, status, error) {
        console.log(status, error);
        msgFlash("See Attendant; Unable to sign in.", "danger");
        $("#submitScannerData").val("").blur();
      }
    })
}

function hideElements(hide) {
  if (hide == true) {

    $("footer").hide();
    $("kiosk-hide").animate({ opacity: 0 }, 1);
    $("kiosk-hide").css("width", "0");
    $("kiosk-hide").prop("disabled", true);
    $("a").hide();
    $("nav").css("width", "0");
  } else {
    $("footer").show();
    $("kiosk-hide").css("width", "inherit");
    $("kiosk-hide").animate({ opacity: 1 }, 1);
    $("kiosk-hide").prop("disabled", false);
    $("a").show();
    $("nav").css("width", "inherit");
  }
}

// Source: https://stackoverflow.com/questions/1125084/how-to-make-the-window-full-screen-with-javascript-stretching-all-over-the-screen
function toggleFullscreen() {
  if($("#fullscreenCheck").prop("checked") == false){
    hideElements(false);
    document.exitFullscreen() || document.webkitExitFullscreen() || document.msExitFullscreen()
  } else {
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

