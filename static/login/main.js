

	function my_fun(){
		document.getElementById("wss-form").classList.remove("d-none");
		document.getElementById("user-form").classList.add("d-none");
	}

	function user_log(){
	document.getElementById("wss-form").classList.add("d-none");
	document.getElementById("user-form").classList.remove("d-none");

	}


	async function wss_authenticate() {
	var ws_username =document.getElementById('ws-username').value;
	 var ws_password =document.getElementById('ws-password').value;
	 var ws_packet_id =document.getElementById('ws-packet').value;

		var myBody = {
			username: ws_username,
			password: ws_password,
			packet_id : ws_packet_id
		}
	const response = await fetch('http://127.0.0.1:8000/wss/log-test/', {
		method: 'POST',
		body: JSON.stringify(myBody), // string or object
		headers: {
		'Content-Type': 'application/json'
		}
	});
	const myJson = await response.json(); 
	if(response.status === 200){
				
	 //  ajax call
		 var myKeyVals = {
			 username: ws_username,
			 password: ws_password,
			 packet_id : ws_packet_id,
			 session_id : myJson.session_id
		 }
 
		 const full_host = location.protocol + '//' + location.host;
		 var saveData = $.ajax({
		 type: 'POST',
		 url: full_host+"/wss/login/",
		 data: myKeyVals,
		 dataType: "text",
		 success: function(resultData) { console.log("saved data")
		//  toast
		document.getElementById("desc").classList.add("bg-success");
		document.getElementById("desc").innerHTML=myJson.msg;
		var x = document.getElementById("toast")
         x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		window.location.replace("/wss/dashboard/");
		document.getElementById("wss-form").classList.add("d-none");
		document.getElementById("user-form").classList.remove("d-none");
		}
		 });
		 saveData.error(function() { console.log("Something went wrong"); });

	} else{
		document.getElementById("desc").classList.add("bg-danger");
		document.getElementById("desc").innerHTML=myJson.msg;
		var x = document.getElementById("toast")
         x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);

	}
	
	}


	function wss_auth(){
	//    var url = "ws://127.0.0.1:8000/socket-receive/chat_group_name/";

	 var ws_username =document.getElementById('ws-username').value;
	 var ws_password =document.getElementById('ws-password').value;
	 var ws_packet_id =document.getElementById('ws-packet').value;

	 if(ws_username ===""){
		document.getElementById('ws-username-error').classList.remove("d-none");
	 }
	 else{
		document.getElementById('ws-username-error').classList.add("d-none");
	 }
	  if(ws_password===""){
		document.getElementById('ws-password-error').classList.remove("d-none");
	 }
	 else{
		document.getElementById('ws-password-error').classList.add("d-none");
	 }

	 if(ws_packet_id===""){
		document.getElementById('ws-packet-error').classList.remove("d-none");
	 }
	 else{
		document.getElementById('ws-packet-error').classList.add("d-none");
	 }

	 if(ws_packet_id === "" || ws_password === "" || ws_username === ""){
		
		return false;
	 }
	 else{
		var form = document.getElementById("wss-form")
		form.submit();
		// wss_authenticate();
	 }

	
	}