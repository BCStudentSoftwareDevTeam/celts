var elem = document.getElementById("show");

$(document).on("fullscreenchange", function() {
    if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.mozFullScreenElement && !document.msFullscreenElement) {
        closeFullscreen(false); // Pass false to indicate not to toggle button text
    }
});

$(document).keydown(function(e) {
    if (e.key === "F11") {
        e.preventDefault();
        toggleFullscreen();
    }
});

function toggleFullscreen() {
    if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
        closeFullscreen(true); // Pass true to indicate toggling button text
    } else {
        openFullscreen();
    }
}

function openFullscreen() {
    $("#show").css({
        'background-color': 'white',
        'position': 'absolute',
        'top': '50%',
        'left': '50%',
        'transform': 'translate(-50%, -50%)',
        'height': '100%',
        'width': '100%',
        'box-sizing': 'border-box'
    });

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
    ensureFocus();
    $("#fullscreenCheck").attr("onclick", "toggleFullscreen()").text("Close Full Screen");
}

function ensureFocus() {
    if (!$("#submitScannerData").is(":focus")) {
        $("#submitScannerData").focus();
    }
}

function closeFullscreen(toggleButton) {
    $("#show").css({
        'background-color': 'white',
        'position': 'static',
        'top': 'auto',
        'left': 'auto',
        'transform': 'none',
        'height': 'auto',
        'width': 'auto',
        'box-sizing': 'content-box'
    });

    if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) { /* Safari */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE11 */
            document.msExitFullscreen();
        }
    }

    ensureFocus();

    if (toggleButton) {
        $("#fullscreenCheck").attr("onclick", "toggleFullscreen()").text("Open Full Screen");
    }
}

$(document).ready(function(e) {
    $("#submitScannerData").focus();

    $("#submitScannerData").keydown(function(e) {
        if (e.key === "Enter") {
            submitData();
        }
    });

    // Opens the camera to scan the ID
    $('.qr-reader-button').on("click", function() {
        $('#qr-reader').toggle();
        let lastResult, countResults = 0;
        let onScanSuccess = function(decodedText, decodedResult) {
            if (decodedText && decodedText.length > 9 && decodedText !== lastResult) {
                lastResult = decodedText;

                $("#submitScannerData").val(decodedText);
                submitData();
            } else {
                message = decodedText + " Invalid B-number";
                flasherStatus = "danger";
            }
        };
        let qrboxFunction = function(viewfinderWidth, viewfinderHeight) {
            let minEdgePercentage = 0.9; // 90%
            let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
            let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
            return {
                width: qrboxSize,
                height: qrboxSize
            };
        };
        let scanner = new Html5QrcodeScanner("qr-reader", {
            fps: 2,
            qrbox: qrboxFunction,
            preferFrontCamera: false,
            facingMode: { exact: "environment" },
            useBarCodeDetectorIfSupported: true,
        }, true);
        scanner.render(onScanSuccess);

        // Delay to ensure the element exists before adding the event
        window.setTimeout(function() {
            $('#html5-qrcode-button-camera-stop').on("click", function() {
                $('#qr-reader').toggle();
            });
        }, 500);
    });

});

function submitData() {
    $(".alert").remove();
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
    });
}

/*function hideElements(hide) {
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
      exited = false

    }else if(typeof window.ActiveXObject!="undefined"){
      // for Internet Explorer
      exited = false

      var wscript = new ActiveXObject("WScript.Shell");
      if (wscript!=null) {
        exited = false

        wscript.SendKeys("{F11}");
      }
    } 
  }else if ($("#fullscreenCheck").prop("checked") == false){
    hideElements(false);
    document.exitFullscreen() || document.webkitExitFullscreen() || document.msExitFullscreen()
  }
  $('#submitScannerData').focus();

};
/*  if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
  console.log("Fullscreen mode was entered");
  hideElements(true);
  console.log("here wewe")
} else {
  console.log("Fullscreen mode was exited");
}if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.mozFullScreenElement && !document.msFullscreenElement) {
  console.log("Fullscreen mode was exited");
}*/

  

