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
function status(value) {
    $("#status").html(value);
}
function activateHighlight(highlightedText) {
    $("#highlighter").html(highlightedText);
    $("#highlighter").css("pointer-events", "auto");
    $("#highlighter").scroll(textAreaScrollUpdate);
    textAreaScrollUpdate();
    window.highlightActivated = true;
}

function highlightText() {
    window.timer = 0;
    window.loadAnimationId = setInterval(function() {
        status("Requesting highlight" + ".".repeat(window.timer + 1));
        window.timer = (window.timer + 1) % 3;
    }, 500)
    if (!$("#modeSelect").val()) {
        status("No mode specified");
        return;
    }
    $.ajax({
        url: "/highlightWithMode",
        //timeout: 5000,
        data: {
            mode: $("#modeSelect").val(),
            text: $("#textInput").val()
        },
        success: function(result) {
            console.log(result); // Just for debugging
            activateHighlight(result.highlightedText);
            status("Done");
        },
        error: function(xhr, message) {
            status("Error: " + message);
        },
        complete: function() {
            clearInterval(window.loadAnimationId);
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
    $("#sendButton").on("click", highlightText);
    $("#sendButton").on("click", placeHighlighter);
    placeHighlighter();
    $(window).resize(placeHighlighter);
}
