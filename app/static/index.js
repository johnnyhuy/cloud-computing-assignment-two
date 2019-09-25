$(document).ready(function(){
    $("#suburbInputForm a").click(function(event) {
        $('#suburbInput').val($(this).html())
        event.preventDefault()
    })
})