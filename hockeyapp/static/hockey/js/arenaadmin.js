$(document).ready(function(){
    $('#id_coords').on('paste', function() {
        setTimeout(function () {
            var str = $('#id_coords').val();
            var res = str.match(/@[0-9]+.[0-9]+,[0-9]+.[0-9]+/);
            if (res.length > 0) {
                res = res[0].slice(1);
                $('#id_coords').val(res);
            }
        }, 100);

    });
});