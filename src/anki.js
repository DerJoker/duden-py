$(document).ready(function(){
	pos = 0;
	fronts = $(".front");
	count = fronts.length;
	for (i=0;i<count;i++) {
		fronts[i].id = 'id_' + i;
	}

	// for (i=0;i<fronts.length;i++) {
	// 	$("div#id_"+i).removeClass("front");
	// }

	// alert($("div#id_5").scrollTop());
	
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