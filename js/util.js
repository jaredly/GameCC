
window.totitle = function(x){
    return x[0].toUpperCase()+x.slice(1);
};

window.hovertext = function(node,text){
  function mm(e){
    $('#hovertext').css('left',e.pageX+15+'px').css('top',e.pageY+15+'px').html(text).show();
  }
  function mo(e){
    $('#hovertext').hide();
  }
  $(node).mousemove(mm).mouseout(mo);
  return function(){
    $(node).unbind('mousemove',mm).unbind('mouseout',mo);
  }
}

function hovershow(text) {
  return function(e) {
    $('#hovertext').css('left',e.pageX+15+'px').css('top',e.pageY+15+'px').html(text).show();
  };
}

function hoverhide() {
  $('#hovertext').hide();
}

function killE(e){
  e.stopPropagation();
  e.preventDefault();
  return false;
}

function stopE(e){
  e.stopPropagation();
  return false;
}

function deepcopy(x){
	var ret = {};
	if (typeof(x) == 'object') {
		if (typeof(x.length) != 'undefined')
			var ret = [];
		for (var index in x) {	
		  if (index=='_tab')continue;
			if (typeof(x[index]) == 'object') {
				retObj[index] = deepcopy(x[index]);
			} else if (typeof(x[index]) == 'string') {
				retObj[index] = x[index];
			} else if (typeof(x[index]) == 'number') {
				retObj[index] = x[index];
			} else if (typeof(x[index]) == 'boolean') {
				((x[index] == true) ? ret[index] = true : ret[index] = false);
			}
		}
	}
	return ret;
}

function keyMenu(e,ondone) {
  var div = $('#contextmenu').show();
  div.html('<div class="menuitem>&lt;Any Key&gt; (press any key to change)</div>');
  var key = '';
  div.css('left',e.pageX+'px').css('top',e.pageY+'px');
  
  var kd = function(e){
    $('.menuitem',div).html(keynames[e.keyCode]);
    key = keynames[e.keyCode];
    e.stopPropagation();
    e.preventDefault();
    return false;
  };
  
  $('.menuitem').click(function(){
    ondone(key);
    ck();
  });
  
  var ck = function(){
    div.hide();
    $(document).unbind('click',ck).unbind('keydown',kd);
  };
  $(document).click(ck);
  $(document).keydown(kd);
  e.stopPropagation();
  e.preventDefault();
  return false;
}

function contextMenu(items, pos) {
  return function(e){
    pos = pos || [e.pageX,e.pageY];
    var div = $('#contextmenu').show();
    div.html('');
    div.css('left',pos[0]+'px').css('top',pos[1]+'px');
    for (var i=0;i<items.length;i++){
      var sub = $('<div class="menuitem">'+items[i][0]+'</div>').appendTo(div);
      if (items[i][2]){
        sub.addClass('selected');
        sub.mousedown(killE).click(killE);
      } else {
        $.data(sub[0],'click',items[i][1]);
        sub.mousedown(function(){
          $.data(this,'click')(e);
          div.hide();
        });
      }
    }
    var ck = function(){
      div.hide();
      $(document).unbind('click',ck);
    };
    $(document).click(ck);
    e.stopPropagation();
    e.preventDefault();
    return false;
  };
}

window.jsonify = function(obj){
  var text;
  if (typeof(obj)==='string'){
    return '"'+obj.replace(/"/g,'\\"')+'"';
  }else if (typeof(obj)==='number'){
    return obj+'';
  }else if (typeof(obj)==='boolean'){
    return (obj+'');//.replace(/^\w/g,function(x){return x.toUpperCase();});
  }else if (typeof(obj)==='object'){
    if (obj.length){
      text = '[';
      for (var i=0;i<obj.length-1;i++){
        text += jsonify(obj[i])+', ';
      }
      text += jsonify(obj[obj.length-1])+']';
      return text;
    }
    text = '{ '
    for (var key in obj){
      text += jsonify(key) + ':' + jsonify(obj[key]) + ',';
    }
    return text.slice(0,-1) + '}';
  }else if (typeof(obj)==='undefined'){
    return 'null';
  }
  console.error('failure converting',obj,typeof(obj));
  throw 'invalid type '+typeof(obj);
};

var openIframe = function(url, onclose, width, height){
  $('#back').show();
  var iframe = $('<iframe class="preview" src="'+url+'"></iframe>').appendTo('body');
  $('#back').one('click',function(){
    $('#back').hide();
    iframe.remove();
    onclose();
  });
  if (width)iframe.css('width',width+'px').css('margin-left',-width/2+'px');
  if (height)iframe.css('height',height+'px').css('margin-top',-height/2+'px');
};

function humanize(x){
  return x.replace(/_/g,' ').replace(/-/g,' ').replace(/(^| )\w/g, function(x){return x.toUpperCase();});
}

