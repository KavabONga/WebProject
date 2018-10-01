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
    this.on("input", function() {
        this.value = this.value.slice(0, limit);
    })
}
function textAreaScrollUpdate() {
    $("#textInput").scrollTop($("#highlighter").scrollTop())
}

function status(value) {
    $("#status").html(value);
}
function statusColor(color) {
    $("#status").css("color", color);
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
        statusColor("rgb(246, 155, 48)")
        return;
    }
    window.timer = 0;
    window.loadAnimationId = setInterval(function() {
        status("Requesting highlight" + ".".repeat(window.timer + 1));
        window.timer = (window.timer + 1) % 3;
    }, 500)
    $("#sendButton").prop("disabled", true);
    var reqTimeout = 5000;
    if ($("#modeSelect").val() == "Wiki")
        reqTimeout = 0;
    $.ajax({
        url: "/highlightWithMode",
        timeout: reqTimeout,
        data: {
            mode: $("#modeSelect").val(),
            text: $("#textInput").val()
        },
        success: function(result) {
            console.log(result); // Just for debugging
            activateHighlight(result.highlightedText);
            clearInterval(window.loadAnimationId);
            status("Done");
            statusColor("rgb(94, 228, 11)");
            $("#sendButton").prop("disabled", false);
        },
        error: function(xhr, message) {
            clearInterval(window.loadAnimationId);
            status("Error: " + message);
            statusColor("red");
            $("#sendButton").prop("disabled", false);
        }
    })
}
function placeHighlighter() {
    let h = $('#highlighter');
    let inp = $('#textInput');
    h.offset(inp.offset());
    h.innerWidth(inp.innerWidth());
    h.innerHeight(inp.innerHeight());
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
    $("#sendButton").click(highlightText);
    $("#sendButton").click(placeHighlighter);
    $("#highlighter").scroll(textAreaScrollUpdate);
    placeHighlighter();
    $(window).resize(placeHighlighter);
    $("#highlightUndoer").click(undoHighlight);
}

function addDefinitionBox(width, height, text) {
    box = $(document.body.appendChild(document.createElement("div")));
}
