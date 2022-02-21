// Loads the password change form async
$("#change-password").click(function () {
	console.log("change-password");
	$.ajax({
		url: '/accounts/password/',
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal").modal("show");
		},
		success: function (data) {
			console.log(data);
			$("#modal .modal-content").html(data.html_form);
		}
	});
});

// Submits the change password form async
$("#modal").on("submit", "#change-password-form", function () {
	var form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$("#messages").html(data.message);
				$("#modal").modal("hide"); 
			}
			else {
				$("#modal .modal-content").html(data.html_form);
			}
		}
	});
	return false;
});

// OTP verification send sms
$("#send-otp").click(function(event){
	event.preventDefault();
	console.log("Send otp clicked");
	var phone_no = $("#id_phone_no").val();
	var country_code = $("#id_country_code").val();
	var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
	$("#send-otp").html("Resend OTP");
	console.log(csrfmiddlewaretoken);
	$.ajax({
		type : "POST",
		url : "/accounts/send_otp/",
		data : {
			'csrfmiddlewaretoken' : csrfmiddlewaretoken,
			'country_code' : country_code,
			'phone_no' : phone_no,
		},
		dataType : 'json',
		success : function(data){
			if(data['otp_sent'] == true){
				$("#messages").html("<div class='alert alert-success' role='alert'>OTP has been sent to " + data['phone_no'] + "</div>");
			}else{
				$("#messages").html("<div class='alert alert-danger' role='alert'>Could not send the OTP, Check the phone number</div>");
			}
		}
	});
});
