function scroll() {
    $("body").scrollTop($("body").height() + 10000);
}

function write(msg) {
    $("#box").append( msg + '\n');
    scroll();
}

$(function () {
      // Focus on page load.
      $("#input").focus();

      // On click, anywhere, focus input box.
      $("html").click(function(){
                          scroll();
                          $("#input").focus();
                          return false;
                      });
});

$(function () {
      var opts = {debug: true};
      var conn = new SockJS(sockjs_url, undefined, opts);

      var to = null;
      var ping = function() {
          conn.send("\x00");
          to = setTimeout(ping, 14000);
      };

      conn.onopen = function() {
          conn.egress_buffer = [];
          to = setTimeout(ping, 14000);
          conn.send('hello');
      };
      conn.onclose = function() {
          clearTimeout(to);
          to = null;
          write("Disconnected.");
      };

      // When user presses enter.
      $("#form").submit(function() {
                            var val = $("#input").val();
                            $("#input").val('');
                            conn.send(val);
                            scroll();
                            clearTimeout(to);
                            to = setTimeout(ping, 14000);
                            return false;
                        });

      conn.onmessage = function(e) {
          if (e.data != "\x00") {
              write(e.data);
          }
      };
  });

