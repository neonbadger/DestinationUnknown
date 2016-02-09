$(document).ready(function() {
    $("#user-login").click(function() {
        location.href = "/authenticate"
    });


    $("#newride").click(function() {
        alert("What is this!?");
    });

    $("#submit_ride").click(function() {
        var time = $("#reminder_time").val();
        var phone_number = $("#phone_number").val();
        var event_name = $("#event_name").val();
        var event_location = $("#event_location").val();

        params = {
          "reminder_time": time,
          "phone_number": phone_number,
          "event_name": event_name,
          "event_location": event_location
        }

        $.ajax({
            url: "/dashboard_webservice",
            type: "post",
            data: params,
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if (!("message" in data)) {
                    $("#reminder_time").val("");
                    $("#phone_number").val("");
                    $("#event_name").val("");
                    $("#event_location").val("");
                    $("#noshow").show()
                } else {
                    $("#noshow").text(data['message'])
                    $("#noshow").show()
                }
            }
        });
    });
})