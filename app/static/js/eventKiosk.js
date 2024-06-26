$(document).keydown(function(e){
  console.log(e.key)
  if (e.key== "Escape"){
    $("#fullscreenCheck").prop("checked", false)
    console.log("here test")
    hideElements(false);
    document.exitFullscreen() || document.webkitExitFullscreen() || document.msExitFullscreen()
    console.log("in toggle function keydown-2")
  }
})

$(document).ready(function(e) {
    $("#submitScannerData").focus();


    $("#submitScannerData").keydown(function(e) {
      console.log("in submit keydopnw")
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

function hideElements(hide) {
  if (hide == true) {
    $("col-md-auto d-print-none d-lg-none").css("width", "0");
    $("footer").hide();
    $("kiosk-hide").animate({ opacity: 0 }, 1);
    $("kiosk-hide").css("width", "0");
    $("kiosk-hide").prop("disabled", true);
    $("position-fixed float-start").hide();
    $("position-fixed float-start").css("width", "0");
    $("#sideBarContainer").attr("class", "col-md-0  d-print-none d-none d-lg-block")
    $("#sideBar").attr("class", "position-fixed float-start d-none")
    $("#sideBarSandwichUI").attr("class","btn btn-dark rounded-0 rounded-end kiosk-hide d-none")
  } else 
   {
    console.log("in hide element before keydown")
    $("footer").show();
    $("kiosk-hide").css("width", "inherit");
    $("kiosk-hide").animate({ opacity: 1 }, 1);
    $("kiosk-hide").prop("disabled", false);
    $("a").show();
    $("#sideBarContainer").attr("class", "col-md-auto d-print-none d-none d-lg-block")
    $("#sideBar").attr("class", "position-fixed float-start")
    $("#sideBarSandwichUI").attr("class","btn btn-dark rounded-0 rounded-end kiosk-hide")
    console.log("in hide element after keydown")
  }
}

// Source: https://stackoverflow.com/questions/1125084/how-to-make-the-window-full-screen-with-javascript-stretching-all-over-the-screen
function toggleFullscreen() {
  if($("#fullscreenCheck").prop("checked") == true){
    exited = true
    console.log(exited)
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
  }else if(typeof window.ActiveXObject!="undefined"){
      // for Internet Explorer
      var wscript = new ActiveXObject("WScript.Shell");
      if (wscript!=null) {
        wscript.SendKeys("{F11}");
      }
    } 
  }else if ($("#fullscreenCheck").prop("checked") == false){
    console.log("here test")
    hideElements(false);
    document.exitFullscreen() || document.webkitExitFullscreen() || document.msExitFullscreen()
    console.log("in toggle function keydown-2")
  }
  $('#submitScannerData').focus();
};
/*if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.mozFullScreenElement && !document.msFullscreenElement) {
  console.log("Fullscreen mode was exited");
}*/
if (document.fullscreenElement && document.webkitFullscreenElement && document.mozFullScreenElement && document.msFullscreenElement) {
  console.log("Fullscreen mode was entered");
}
