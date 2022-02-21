// Client  - Renders the add job form asyn
$("#add-job").click(function () {
	$.ajax({
		url: '/client/job/add/',
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal-add-job").modal("show");
		},
		success: function (data) {
			$("#modal-add-job .modal-content").html(data.html_form);
		}
	});
});

// Client - Renders the add employee form asyn
$("#add-employee").click(function () {
	$.ajax({
		url: '/client/employees/add/',
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal-add-employee").modal("show");
		},
		success: function (data) {
			$("#modal-add-employee .modal-content").html(data.html_form);
		}
	});
});

// Submits the add job form async
$("#modal-add-job").on("submit", "#add-job-form", function () {
	var form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$("#jobs-table > tbody").html(data.html_member_list);  // <-- Replace the table body
				$("#modal-add-job").modal("hide"); 
			}
			else {
				$("#modal-add-job .modal-content").html(data.html_form);
			}
		}
	});
	return false;
});
// Submits the add employee form async
$("#modal-add-employee").on("submit", "#add-employee-form", function () {
	var form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$("#employees-table > tbody").html(data.html_member_list);  // <-- Replace the table body
				$("#modal-add-employee").modal("hide"); 
			}
			else {
				$("#modal-add .modal-content").html(data.html_form);
			}
		}
	});
	return false;
});

// Enabling the schedule update form
$("#schedule-status-cards #update-schedule").on("click", function(){
	//$("#schedule-update-form :input").prop("disabled", false);
	var progress = $(this).data("progress");
	var html = "<button type='button' id='close' class='btn btn-default btn-sm'>Cancel</button><button type='submit' class='btn btn-primary btn-sm'>Save</button>";
	if(progress == 0){
		$("#schedule-update-form  #id_screening_status").prop("disabled", false);
	}else if(progress == 25){
		$("#schedule-update-form  #id_interview_date").prop("disabled", false);
	}else if(progress == 50){
		$("#schedule-update-form  #id_interview_status").prop("disabled", false);
	}else if(progress == 75){
		$("#schedule-update-form  #id_date_joined").prop("disabled", false);
	}else{
		html = "No more changes allowed, since candidate have joined!   <button type='button' id='close' class='btn btn-default btn-sm'>Cancel</button>";
	}
	$("#button-space").html(html);
})

// Disabling the schedule update form
$("#schedule-status-cards").on("click", "#close", function(){
	$("#schedule-update-form :input").prop("disabled", true);
	var html = "";
	$("#button-space").html(html);
});

// Saving the updates to the schedule form
$("#schedule-update-form").on("submit", function(){
	$("#schedule-update-form :input").prop("disabled", false);
	$("#schedule-update-form #id_progress").val(function(){
		var p = "0";
		if($("#schedule-update-form  #id_date-joined").val() != "Not Done"){
			p = "100";
		}
		if($("#schedule-update-form  #id_interview_status").val() != "Not Done"){
			p = "75";
		}
		if($("#schedule-update-form  #id_interview_date").val() != ""){
			p = "50";
		}
		if($("#schedule-update-form  #id_screening_status").val() != "Not Screened"){
			p = "25";
		}
		return p;
	});
	$.ajax({
		url: $(this).attr("action"),
		data: $(this).serialize(),
		type: $(this).attr("method"),
		dataType: 'json',
		success: function (data) {
			$("#schedule-status-cards").html(data.html_form);
			var html = "";
			$("#button-space").html(html);
			$("#schedule-update-form :input").prop("disabled", true);
		}
	});
	return false;
});

function listStatusWise(progress){
	$.ajax({
		url : '/client/list/' + progress +'/',// 0 is the progress value for new applicants
		type: 'get',
		dataType: 'html',
		success: function(html) {
			console.log("Success");
			console.log(html);
			$("#list-applicants-statuswise").html(html);
		}
	});
};
// On ready of the client dashboard load status new candidates
$("#list-applicants-statuswise").ready(function(){
	listStatusWise(0);
});
// On Click status new card load status new candidates
$("#new-count").click(function(){
	listStatusWise(0);
});
// On Click status screened card load status screened candidates
$("#screened-count").click(function(){
	listStatusWise(50);
});
// On Click status interviewed card load status interviewed candidates
$("#interviewed-count").click(function(){
	listStatusWise(75);
});
// On Click status joined card load status joined candidates
$("#joined-count").click(function(){
	listStatusWise(100);
});

// On navbar load add the search field
$("#nav-search").ready(function(){
	$.ajax({
		url : '/client/search/',
		dataType: 'html',
		success : function(html){
			$("#nav-search").html(html);
		}
	});
});

// Activates the profile update form
$("#update-client").click(function(){
	$("#client-profile-form :input").prop("disabled", false);
	var html = "<button type='button' id='close' class='btn btn-default'>Cancel</button><button type='submit' class='btn btn-primary'>Save</button>";
	$("#client-update-action").html(html);
});

// Deactivates the client profile update form
$("#client-update-action").on("click", "#close", function(){
	$("#client-profile-form :input").prop("disabled", true);
	var html = "";
	$("#client-update-action").html(html);
});
// Deactivates the client profile form on page ready
$('#client-profile-form').ready(function(){
	$("#client-profile-form :input").prop("disabled", true);
})

// Activates the client profile update form
$("#update-employee").click(function(){
	$("#employee-profile-form :input").prop("disabled", false);
	var html = "<button type='button' id='close' class='btn btn-default'>Cancel</button><button type='submit' class='btn btn-primary'>Save</button>";
	$("#employee-update-action").html(html);
});

// Deactivates the Employee profile update form
$("#employee-update-action").on("click", "#close", function(){
	$("#employee-profile-form :input").prop("disabled", true);
	var html = "";
	$("#employee-update-action").html(html);
});
// Deactivates the profile form on page ready
$('#employee-profile-form').ready(function(){
	$("#employee-profile-form :input").prop("disabled", true);
})

// Datetimepicker
flatpickr('.datetimepicker', {
  enableTime: true,
  dateFormat: "Y-m-d H:i",
});
