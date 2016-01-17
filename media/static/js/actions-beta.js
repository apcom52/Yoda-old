function sendAjax(method, url, data, success, error) {
	csrf_object = {
		'csrfmiddlewaretoken': getCookie("csrftoken"),
        'X-CSRFToken': getCookie("csrftoken"),
	}
	result_data = json_merge(csrf_object, data)
	console.log(result_data)
	$.ajax({
        type: method,
        url: url,
        processData: false,
        contentType: "application/json",
        data: result_data,
        headers: {
            'csrfmiddlewaretoken': getCookie("csrftoken"),
            'X-CSRFToken': getCookie("csrftoken"),
        },
        success: success,
        error: error,
    });
}

function getCookie(name) {
 	var matches = document.cookie.match(new RegExp(
    	"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  	));
  	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function json_merge(json1, json2){
    var out = {};
    for(var k1 in json1){
        if (json1.hasOwnProperty(k1)) out[k1] = json1[k1];
    }
    for(var k2 in json2){
        if (json2.hasOwnProperty(k2)) {
            if(!out.hasOwnProperty(k2)) out[k2] = json2[k2];
            else if(
                (typeof out[k2] === 'object') && (out[k2].constructor === Object) && 
                (typeof json2[k2] === 'object') && (json2[k2].constructor === Object)
            ) out[k2] = json_merge_recursive(out[k2], json2[k2]);
        }
    }
    return out;
}

function humanFileSize(bytes) {
    var thresh = 1024;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' б';
    }
    var units = ['Кб','Мб','Гб','Тб','Пб','Еб','Зб','Йб']
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1)+' '+units[u];
}