var port = chrome.runtime.connectNative('youtubedl');

port.onMessage.addListener(function(msg) {
  console.log("Received" + msg);
});

port.onDisconnect.addListener(function() {
  console.log("Disconnected");
});

chrome.browserAction.onClicked.addListener(
  function(tab) {
    port.postMessage({ text: tab.url });
  }
);

