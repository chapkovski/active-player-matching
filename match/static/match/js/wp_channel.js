$(function () {
    $status_span = $('span.status');
    $timer_span = $('span.timer');

    $timer_span.html(seconds_to_passive);
    wp_socket.onmessage = function (event) {
        var obj = jQuery.parseJSON(event.data);
        console.log(obj);
    };

    var idleTime = 0,
        active = true;

    function send_status(status) {
        if (status !== active) {
            var status_string = status === true ? 'active' : 'passive';
            $status_span.html(status_string);
            active = status;
            var msg = {
                'status': status,

            };
            if (wp_socket.readyState === WebSocket.OPEN) {
                wp_socket.send(JSON.stringify(msg));
            }
            ;

        }
    };


    //Increment the idle time counter every second.
    var idleInterval = setInterval(timerIncrement, 1000); // 1 second

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        idleTime = 0;
        send_status(true);
    });
    $(this).keypress(function (e) {
        idleTime = 0;
        send_status(true);
    });


    function timerIncrement() {
        idleTime = idleTime + 1;
        var time_left = seconds_to_passive - idleTime;
        var time_show = time_left >= 0 ? time_left : 0;
        $timer_span.html(time_show);
        if (idleTime > seconds_to_passive) {
            send_status(false);

            window.location.reload();
        }
    }
});