
var port = chrome.runtime.connectNative('youtubedl');

port.onMessage.addListener(function(msg) {
  console.log("Received" + msg);
});
port.onDisconnect.addListener(function() {
  console.log("Disconnected");
});

chrome.browserAction.onClicked.addListener(
  function(tab) {
    alert("Clicked with tab.url = " + tab.url);
    chrome.runtime.sendNativeMessage('youtubedl',
    { 
      text: "--extract-audio --audio-format mp3 --output \"%(artist)s-%(track)s.%(ext)s\" " + tab.url 
    }, 
    function(response) {
      console.log("Received " + response);
    });
  }
);
