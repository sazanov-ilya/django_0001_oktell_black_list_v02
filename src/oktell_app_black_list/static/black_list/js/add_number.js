// После загрузки страницы
$(document).ready(function(){

	console.log('Страница загружена');
	//get_timezone_str();
	
	
	// Маска ввода для телефона
	$("#input_number").mask("+7(999)999-9999", {placeholder:"-"}, {autoclear: false});
	//$("#input_number").mask("(999) 999-9999");


	// подключаем select2 на списки
	$('#select_type').select2({
		theme: "bootstrap-5",
		//containerCssClass: "select2--small", // For Select2 v4.0
		selectionCssClass: "select2--small", // For Select2 v4.1
		//dropdownCssClass: "select2--small",
		//placeholder: 'Выберите продукт',
		allowClear: true
	});

});