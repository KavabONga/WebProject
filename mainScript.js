String.prototype.replaceAll = function(sub, nsub){
	return this.split(sub).join(nsub);
}
String.prototype.format = function() {
	var str = this;
	for (var i in arguments) {
		str = str.replaceAll('{' + i + '}', arguments[i]);
	}
	return str;
}
HTMLTextAreaElement.prototype.setLengthLimit = function(limit) {
	this.oninput = function(){
		this.value = this.value.slice(0, limit);
	}
}