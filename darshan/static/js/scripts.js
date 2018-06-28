jQuery(document).ready(function() {
	$('.launch-modal').on('click', function(e){
		e.preventDefault();
		$( '#' + $(this).data('modal-id') ).modal({backdrop: 'static'});
		
	});

});




function ValidateUsername(){
	var get_id= document.getElementById("username1");
	var get_span = document.getElementById("susername1");
	var exp = /^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$/;
	var exp1 = /^[0-9]+$/;

	if(!get_id.value.match(exp))
	{
        get_span.style = "display:block;color:red";
        
	}
	else if (get_id.value.match(exp1))
	{
		get_span.style = "display:block;color:red";
		
	}
	else
	{
		get_span.style = "display:none;";
	}
}






function ValidateEmail(){
	var get_id= document.getElementById("id_email1");
	var get_span = document.getElementById("semail1");
	var exp = /^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
	var exp1 = /^[0-9]+$/;

	if(!get_id.value.match(exp))
	{
        get_span.style = "display:block;color:red";
        
	}
	else
	{
		get_span.style = "display:none;";
		
	}
}

function Validatepassword1(){
	var get_id= document.getElementById("password1");
	var get_span = document.getElementById("spassword1");
	var len = get_id.value
	var exp1 = /^[0-9]+$/;
	

	if(len.length < 8 )
	{   get_span.innerHTML="Password is too weak.";
        get_span.style = "display:block;color:red";

	}
	else if(len==exp1)
	{
		get_span.innerHTML="Password can't be only numeric."
		get_span.style = "display:block;color:red";
	}
	else
	{
		 get_span.style = "display:none;"
	}
}

function Validatepassword2(){
	var get_id= document.getElementById("password2");
	var get_span = document.getElementById("spassword2");
	var get_id1 = document.getElementById("password1");
	
	if(!get_id.value.match(get_id1.value))
	{   
        get_span.style = "display:block;color:red";

	}
	else
	{
		 get_span.style = "display:none;"
	}

	
}

function Validatemobile(){
	var get_id= document.getElementById("mobile_number");
	var get_span = document.getElementById("smobile");
	var exp = /^[9|8|7|6][0-9]+$/
	
	if(!get_id.value.match(exp))
	{   
        get_span.style = "display:block;color:red";

	}
	else
	{
		 get_span.style = "display:none;"
	}

	
}

function DisplayMsg(){

 var get_class = document.getElementsById("msg");

 get_class.style = "display:block";	
}