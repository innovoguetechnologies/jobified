// Company - Renders the add poc form asyn
$("#add-poc").click(function () {
	$.ajax({
		url: '/company/poc/add/',
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal").modal("show");
		},
		success: function (data) {
			$("#modal .modal-content").html(data.html_form);
		}
	});
});

// Submits the add poc form async
$("#modal").on("submit", "#add-poc-form", function () {
	var form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$("#poc-table > tbody").html(data.html_member_list);  // <-- Replace the table body
				$("#modal").modal("hide"); 
			}
			else {
				$("#modal .modal-content").html(data.html_form);
			}
		}
	});
	return false;
});
