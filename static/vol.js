$(document).ready(function(){
    function updateVol() {
        $.get("/vol/get", function(data, st) {
            console.log("Volume is " + data);
            $("#vol-current").html(data);
        });
    }

    updateVol();

    $('.scbt').click(function() {
        $path = $(this).attr('scbta')
        $.get($path, function(data, st){
            console.log(data+'\n'+st)
        });

        updateVol();
    });

    $.get('/vol/getuser', function(data, st) {
        console.log("Setting select bot to user " + data);
        $('#account-select').val(data)
    });

    $('#account-select').change(function() {
        $sel_user = $(this).find(":selected").attr('value');
        $.get('/vol/getuser', function(data, st) {
            $current_user = data;
            console.log('current ' + $current_user + ' sel ' + $sel_user);
            if ($current_user !== $sel_user) {
                console.log("switching to " + $sel_user);
                $.get('/vol/setuser/' + $sel_user, function(data, st) {
                    console.log(data+'\n'+st);
                    alert("Changing user, will reload in 10s");
                    setTimeout(function() {
                        location.reload();
                    }, 10000);
                });
            } else {
                console.log("User " + $sel_user + " is already selected");
            }
        });
    })
});
