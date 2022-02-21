// Consultant - Renders the add member form async
$("#add-member").click(function () {
	$.ajax({
		url: '/consultant/members/add/',
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
			$("#modal-add").modal("show");
		},
		success: function (data) {
			$("#modal-add .modal-content").html(data.html_form);
		}
	});
});

// Submits the add member form async
$("#modal-add, #modal-add-employee").on("submit", "#add-member-form", function () {
	var form = $(this);
	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$("#members-table > tbody").html(data.html_member_list);  // <-- Replace the table body
				$("#modal-add, #modal-add-employee").modal("hide"); 
			}
			else {
				$("#modal-add .modal-content").html(data.html_form);
			}
		}
	});
	return false;
});
