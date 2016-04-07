$(document).ready(function() {
	console.log("ready");
    // $("#vote").click(function() {
    //     console.log("status req");
    //     parent.postMessage('from HF, give status please', '*');
    // });
    $("input[name='radioface']").on("change", function() {
    	console.log("status req");
    	parent.postMessage('from HF, give status please', '*');
    });
});
// halp? functionality
// ? : sup
function saveVote(stat) {
	var selectedVal = "";
	var selected = $("#radioface input[type='radio']:checked");
	if (selected.length > 0) {
		selectedVal = selected.val();
	}
	var xhr = createCORSRequest("POST", 'http://checkbox.io:3002/api/study/vote/submit/');
	xhr.setRequestHeader('Content-Type', 'application/json');
	var requestData = {
		"studyId": "569e667f12101f8a12000001",
		"fingerprint": "5331665335",
		"answers": [
		{
			"question": 1,
			"kind": "singlechoice",
			"answer": selectedVal
		},
		{
			"question": 2,
			"kind": "textarea",
			"answer": "Simplistic Face Based Survey (1 to 5, happy to angry)"
		},
		{
			"question": 3,
			"kind": "textarea",
			"answer": stat
		}
		],
		"contact": "false"
	};
	xhr.onload = function(resp, a, b) {
		console.log(a, b);
	}
      


	requestData.answers = JSON.stringify(requestData.answers);
	xhr.send(JSON.stringify(requestData));
	$("#feedback").text("Thank you for your feedback!");
	$("#feedback").show(500); 
	setTimeout(function(){$("#feedback").hide(500)}, 5000);
    //$("#feedback").hide(500).delay(5000); Does not work
    // test variance
}

function createCORSRequest(method, url) {
	var xhr = new XMLHttpRequest();
	if ("withCredentials" in xhr) {
        // Check if the XMLHttpRequest object has a "withCredentials" property.
        // "withCredentials" only exists on XMLHTTPRequest2 objects.
        xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined") {
        // Otherwise, check if XDomainRequest.
        // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
        xhr = new XDomainRequest();
        xhr.open(method, url);
    } else {
        // Otherwise, CORS is not supported by the browser.
        xhr = null;
    }
    return xhr;
} 