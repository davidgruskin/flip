var bkg = chrome.extension.getBackgroundPage();

window.onload = function() {
    console.log("Starting up!");
};

function sendDataToParser(tab, url) {
    var b = ['three','four'];

    var postData = {
      url: url,
      b: b,
    }

    $.ajax({
        url: "http://127.0.0.1:5000/google",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(postData),
        success: function(data){ 
            bkg.console.log("Server Response: " + data);
            //chrome.browserAction.setIcon({path:"test.png"});
            if (data != "nothing") {
                var jsonObj = JSON.parse(data);
                bkg.console.log(jsonObj.url_recommendation)
                seenUrls.push(jsonObj.url_recommendation)
                bkg.console.log(jsonObj.header)
                chrome.tabs.sendMessage(tab.id, { text: "report_back", url: jsonObj.url_recommendation, mytitle: jsonObj.header },
                                doStuffWithDOM);
            }
        }
    });
    
}

chrome.browserAction.onClicked.addListener(function(tab) { 
    bkg.console.log('icon clicked')
});


function doStuffWithDOM(domResponse) {
    bkg.console.log("I received the following DOM content:\n" + domResponse);
}


var seenUrls = []
var lastUrl = "";
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (tab.active && changeInfo.status=="loading" && lastUrl != tab.url) {
        if (seenUrls.indexOf(tab.url) > -1) {
            bkg.console.log("Article seen already");
            return;
        } 

        lastUrl = tab.url
        bkg.console.log("Sending Server Request: " + tab.url);

        var serverResponse = sendDataToParser(tab, tab.url)
    }
});




