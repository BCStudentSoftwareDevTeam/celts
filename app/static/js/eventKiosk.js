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

function triggerCamera() {
  // Find the textbox element by its ID
  var textboxElement = document.getElementById('submitScannerData');
  // Check if the browser supports the getUserMedia method
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    let videoWidth;
    let videoHeight;

    // Determine the video width and height based on the device's viewport
    if (window.innerWidth >= 640 && window.innerHeight >= 320) {
      // If the viewport is large enough, use the ideal width and height
      videoWidth = 640;
      videoHeight = 320;
    } else {
      // If the viewport is smaller, use reduced width and height
      videoWidth = window.innerWidth;
      videoHeight = videoWidth / 1.5;
    }
    const scanSound = document.getElementById('scanSound');
    const videoConstraints = {
      width: { ideal: videoWidth },
      height: { ideal: videoHeight },
      facingMode: 'environment', // Use the rear-facing camera if available
      focusMode: 'continuous'
    };
    // Request permission to access the camera
    navigator.mediaDevices.getUserMedia({ video: videoConstraints })
      .then(function(stream) {
        // Access to the camera is granted, do something with the stream
        var videoElement = document.createElement('video');
        videoElement.srcObject = stream;
        var parentElement = textboxElement.parentNode;
      
        // Append the video element to the parent element, right after the camera button
        parentElement.insertBefore(videoElement, cameraButton.nextSibling);

        // Optional: Play the video stream
        videoElement.play();
        // Disable the camera button after displaying the video
        cameraButton.disabled = true;

        // Configure QuaggaJS to detect barcodes
        Quagga.init({
          inputStream: {
            name: "Live",
            type: "LiveStream",
            target: videoElement
          },
          decoder: {
            readers: ['ean_reader', 'code_128_reader', 'ean_8_reader', 'code_39_reader', 'code_39_vin_reader', 'codabar_reader', 'upc_reader', 'upc_e_reader', 'code_93_reader']
          }
        }, function(err) {
          if (err) {
            console.log('Error initializing Quagga:', err);
            return;
          }
          console.log('Quagga initialized successfully');
          
          // Start barcode detection
          Quagga.start();
        });

        function playScanSound() {
          scanSound.play();
        }

        // Listen for barcode detection events
        Quagga.onDetected(function(result) {
          playScanSound();
          // Handle the detected barcode result
          console.log('Barcode detected:', result.codeResult.code);
          
          // Stop barcode detection
          Quagga.stop();
          
          // Extract the barcode value and do something with it
          var barcodeValue = result.codeResult.code;
          textboxElement.value = barcodeValue;
          // Handle the barcode value as needed
        });
      })
      .catch(function(error) {
        // An error occurred or the user denied permission, handle the error
        console.log('Unable to access the camera:', error);
      });
  } else {
    // The getUserMedia method is not supported by the browser
    console.log('getUserMedia is not supported');
  }
}

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
