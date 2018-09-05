String.prototype.replaceAll = function(sub, nsub) {
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
    this.oninput = function() {
        this.value = this.value.slice(0, limit);
    }
}
function highlightText() {
    if (!$("#modeSelect").val()) {
        console.log("No mode specified");
        return;
    }
    console.log("Requesting highlight");
    $.ajax({
        url: "/highlightWithMode",
        //timeout: 5000,
        data: {
            mode: $("#modeSelect").val(),
            text: $("#textInput").val()
        },
        success: function(result) {
            console.log(result); // Just for debugging
            $("#highlighter").html(result.highlightedText);
            $("#highlighter").css("pointer-events", "auto");
        },
        error: function(xhr, message) {
            console.log("Error: " + message);
        }
    })
}
function placeHighlighter() {
    let h = $('#highlighter');
    let inp = $('#textInput');
    h.css('left', inp.offset().left + 'px');
    h.css('top', inp.offset().top + 'px');
    h.css('width', inp.width() + 'px');
    h.css('height', inp.height() + 'px');
}
function setupPage() {
    $("#sendButton").on("click", highlightText);
    placeHighlighter();
    $(window).resize(placeHighlighter);
}
