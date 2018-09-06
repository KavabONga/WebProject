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
            $("#highlighter").scroll(textAreaScrollUpdate);
            textAreaScrollUpdate();
            window.highlightActivated = true;
        },
        error: function(xhr, message) {
            console.log("Error: " + message);
        }
    })
}
function placeHighlighter() {
    let h = $('#highlighter');
    let inp = $('#textInput');
    h.offset(inp.offset());
    h.width(inp.width());
    h.height(inp.height());
    h.scrollTop(inp.scrollTop());
}

function textAreaScrollUpdate() {
    $("#textInput").scrollTop($("#highlighter").scrollTop())
}

function setupPage() {
    window.highlightActivated = false
    $("#sendButton").on("click", highlightText);
    $("#sendButton").on("click", placeHighlighter);
    placeHighlighter();
    $(window).resize(placeHighlighter);
}
