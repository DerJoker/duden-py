$(document).ready(function(){
	pos = 0;
	fronts = $(".front");
	count = fronts.length;
	for (i=0;i<count;i++) {
		fronts[i].id = 'id_' + i;
	}

	$("span.content").after('<button class="copytext">Copy Text</button>');
	$("dd.content").after('<button class="copytext">Copy Text</button>');


	$("button.copytext").click(function(){
		word = $(this).parents("div.definition-py").prev().text();
		bedeutung = $(this).parent().text();
		beispiel = $(this).parent().find("div").text();
		bedeutung = bedeutung.replace(beispiel,"").replace("Copy Text","");
		// wd = word + bedeutung;
		// alert(wd);
		tmpselect = document.createElement("input");
		tmpselect.value = word + ' : ' + bedeutung;
		$(this).after(tmpselect);
		$(this).next().focus();
		$(this).next().select();
	});
});

$(document).keydown(function(event){
	// alert(event.keyCode);
	switch(event.keyCode){
		case 74:
			// alert("j");
			if (pos + 1 < count) {
				pos += 1;
				$("body").scrollTop($("div#id_" + pos).position().top);
			}
			break;
		case 75:
			// alert("k");
			if (pos - 1 >= 0) {
				pos -= 1;
				$("body").scrollTop($("div#id_" + pos).position().top);
			}
			break;
	}
});