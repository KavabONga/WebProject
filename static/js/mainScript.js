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
function textAreaScrollUpdate() {
    $("#textInput").scrollTop($("#highlighter").scrollTop())
}

function status(value) {
    $("#status").html(value);
}
function activateHighlight(highlightedText) {
    $("#highlighter").html(highlightedText);
    $("#highlighter").css("pointer-events", "auto");
    textAreaScrollUpdate();
    window.highlightActivated = true;
    $("#highlightUndoer").prop("disabled", false);
}

function highlightText() {
    if (!$("#modeSelect").val()) {
        status("No mode specified");
        return;
    }
    window.timer = 0;
    window.loadAnimationId = setInterval(function() {
        status("Requesting highlight" + ".".repeat(window.timer + 1));
        window.timer = (window.timer + 1) % 3;
    }, 500)
    $.ajax({
        url: "/highlightWithMode",
        timeout: 5000,
        data: {
            mode: $("#modeSelect").val(),
            text: $("#textInput").val()
        },
        success: function(result) {
            console.log(result); // Just for debugging
            activateHighlight(result.highlightedText);
            clearInterval(window.loadAnimationId);
            status("Done");
        },
        error: function(xhr, message) {
            clearInterval(window.loadAnimationId);
            status("Error: " + message);
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

function undoHighlight() {
    if (!window.highlightActivated)
        return;
    window.highlightActivated = false;
    $("#highlighter").html("");
    $("#highlighter").css("pointer-events", "none");
    $("#highlightUndoer").prop("disabled", true);
}

function setupPage() {
    window.highlightActivated = false;
    $("#sendButton").on("click", highlightText);
    $("#sendButton").on("click", placeHighlighter);
    $("#highlighter").scroll(textAreaScrollUpdate);
    placeHighlighter();
    $(window).resize(placeHighlighter);
    $("#highlightUndoer").click(undoHighlight);
}
