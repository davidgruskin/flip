let languageOptions = [
	"Change the way you look at it",
	"Consider this:",
	"Talk to someone dealing with similar struggles",
	"This isn’t easy, but there is hope",
	"There are other options",
	"You matter",
	"#HopeHappens",
	"You aren’t alone",
	"Are you experiencing overwhelming pain? You’re not alone.",
	"Talking can help.",
	"Connect with the resources that best support you",
	"It’s OK to ask for help",
	"#IKeptLiving",
	"Mental health matters",
	"It’s OK to talk",
	"Breathe",
	"Start the conversation about mental health",
	"Whom do you wanna reach out to?"
]

function closeFlipContent() {
	document.getElementById("__flipcontent__").remove();
}

function appendElementToBody(message, url, mytitle) {
	var element = document.getElementsByTagName('body');
	var ourMessage = `
		<div id="__flipcontent__" style="font-family:'Helvetica';
			font-size:15px;position:fixed;width:100%;max-width:700px;top:0;text-align:center;right: 0;
			z-index:1000000;background:rgba(27, 163, 156, 1);color:white;border-radius:5px;padding:8px;">
			<div style="line-height:12px;">`
				+ message + 
			`</div>
			<div style="line-height:15px;"><a onclick="function hi(){
				document.getElementById('__flipcontent__').remove()
				document.body.style.marginTop = '0px';};
				hi()" style="font-size:17px;color:white;font-weight:bold;padding:4px;display: block;text-decoration:none;
				line-height:15px;" href="` + url + `">` + mytitle + `</a></div>
			<div onclick="function hi(){
				document.getElementById('__flipcontent__').remove()
				document.body.style.marginTop = '0px';};
				hi()" 
				style="line-height:15px;margin:0;padding:0;position: absolute;right: 0;top: 0;cursor: pointer;padding: 8px;font-weight: bold;">Close</div>

			<div onclick="function hi(){
				document.getElementById('__flipcontent__').remove()
				document.body.style.marginTop = '0px';};
				hi()" 
				style="line-height:12px;margin:0;padding:0;position:absolute;left:0;top:0;padding-top: 17px;cursor:pointer;padding:8px;
				font-weight:bold;margin-top: 4px;margin-left: 8px;background: blue;border-radius: 7px;font-size: 12px;width: 75px;">
					<div style="line-height:12px;">
						<a onclick="function hi(){
										document.getElementById('__flipcontent__').remove()
										document.body.style.marginTop = '0px';};
										hi()" style="line-height:12px;margin:0;padding:0;padding-top: 2px;color:white;display: block;text-decoration: none;" href="https://www.notokapp.com/">Talk to <br/> someone</a></div>
					</div>
				</div>
			</div>

			</div>
		</div>`

    document.body.innerHTML += ourMessage
    document.body.style.marginTop = "58px";
	sendResponse(element.innerHTML);

	var newElem = document.getElementById('__flipcontent__');
	console.log(newElem.innerHTML)
}

/* Listen for messages */
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.text && (msg.text == "report_back")) {
    	var element = document.getElementsByTagName('body');
    	var message = languageOptions[Math.floor(Math.random()*languageOptions.length)];
    	appendElementToBody(message, msg.url, msg.mytitle)
    }
});
