var bkg = chrome.extension.getBackgroundPage();
window.onload = function() {
	bkg.console.log('HELLO PEOPLE: ' + bkg);
};

