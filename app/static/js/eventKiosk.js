
// var elem = document.documentElement;
$( document ).ready(function() {
  var e = $.Event('keydown', { keyCode: 122 });
    $(document).trigger(e);
  //
  //   if (!document.fullscreenElement &&    // alternative standard method
  //     !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods
  //   if (document.documentElement.requestFullscreen) {
  //     document.documentElement.requestFullscreen();
  //   } else if (document.documentElement.msRequestFullscreen) {
  //     document.documentElement.msRequestFullscreen();
  //   } else if (document.documentElement.mozRequestFullScreen) {
  //     document.documentElement.mozRequestFullScreen();
  //   } else if (document.documentElement.webkitRequestFullscreen) {
  //     document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
  //   }
  // } else {
  //   if (document.exitFullscreen) {
  //     document.exitFullscreen();
  //   } else if (document.msExitFullscreen) {
  //     document.msExitFullscreen();
  //   } else if (document.mozCancelFullScreen) {
  //     document.mozCancelFullScreen();
  //   } else if (document.webkitExitFullscreen) {
  //     document.webkitExitFullscreen();
  //   }
  // }
});
