// Checks if applicant is fresher and updates the experience section
$("#is-fresher").change(function() {
	if(this.checked) {
		$("#id_work_exp_year, #id_work_exp_month, #id_salary").val(0);
		$("#id_job_title, #id_company, #id_dept").val("Nil");
		$("#experience").hide();
	}else{
		$("#experience").show();
	}
});

// View Job Description
$("tr").on("click", function(){
	$.ajax({
		url: '/candidate/jobs/view/' + $(this).attr("data-id"),
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal-view-job").modal("show");
		},
		success: function (data) {
			console.log(data.job_desc);
			$("#modal-view-job .modal-content").html(data.job_desc);
		}
	});
	
});

// Apply for Job
$("#modal-view-job").on("click", "#apply-job", function(){
	$.ajax({
		url: '/candidate/jobs/apply/' + $(this).attr("data-id"),
		type: 'get',
		dataType: 'json',
		success: function (data) {
			$("#modal-view-job").modal("hide");
			$("#messages").html(data.message);
		}
	});
});
