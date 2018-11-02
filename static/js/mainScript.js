redStatus = "red"
yellowStatus = "rgb(246, 155, 48)"
greenStatus = "rgb(94, 228, 11)"
highlightActive = false
function status(value, color) {
    $("#status").html(value);
    $("#status").css("color", color);
}
function activateHighlight(highlightedText) {
    $("#highlighter").html(highlightedText);
    $(".termlink").filter(function(){
        return this.hasAttribute('definition');
    }).each(function(){
        $(this).balloon({
            contents: this.getAttribute("definition"),
            css: {
                fontSize: ".5rem",
                pointerEvents: "none"
            }
        });
    });
}

function highlightText() {
    if (!$("#modeSelect").val()) {
        status("No mode specified", yellowStatus);
        return;
    }
    window.timer = 0;
    window.loadAnimationId = setInterval(function() {
        status("Requesting highlight" + ".".repeat(window.timer + 1), greenStatus);
        window.timer = (window.timer + 1) % 3;
    }, 500)
    $("#sendButton").prop("disabled", true);
    var reqTimeout = 0;
    $.ajax({
        url: "/highlightWithMode",
        timeout: reqTimeout,
        data: {
            mode: $("#modeSelect").val(),
            text: $("#highlighter").text()
        },
        success: function(result) {
            console.log(result); // Just for debugging
            highlightActive = true;
            activateHighlight(result.highlightedText);
            clearInterval(window.loadAnimationId);
            status("Done", greenStatus);
            $("#sendButton").prop("disabled", false);
            if ($(".termlink").length == 0) {
		    	status("Nothing to highlight", yellowStatus);
                highlightActive = false;
                return;
		    }
            $("#highlighter").prop("contenteditable", false);
        },
        error: function(xhr, message) {
            clearInterval(window.loadAnimationId);
            status("Error: " + message, redStatus);
            $("#sendButton").prop("disabled", false);
        }
    })
}
function undoHighlight() {
    $("#highlighter").html($("#highlighter").text());
    $("#highlighter").prop("contenteditable", true);
    highlightActive = false;
}

function clearHTML() {
    console.log($("#highlighter > *").length);
    if ($("#highlighter > *").length > 0) {
        console.log($("#highlighter > *"));
        $("#highlighter").html($("#highlighter").text());
    }
}

$(function(){
    $("#sendButton").click(highlightText);
    $("#highlightUndoer").click(undoHighlight);
    $("#highlighter").on("paste", function(){setTimeout(clearHTML, 0)});
    new ClipboardJS('#htmler', {
        text : function() {
            console.log($("#highlighter").html());
            status("Copied!", greenStatus);
            return $("#highlighter").html();
        }
    })
});


