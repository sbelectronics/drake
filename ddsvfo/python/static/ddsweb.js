function ddsweb() {
    // navigation
    onOpenTab = function(evt, tabName) {
        // Declare all variables
        var i, tabcontent, tablinks;

        // Get all elements with class="tabcontent" and hide them
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
        }
      
        // Get all elements with class="tablinks" and remove the class "active"
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
      
        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
      }

    // vfo
    onVfoSetFreq = function() {
        freq =  $('#vfo-freq').val();
        this.setFrequency(freq);
    }

    setFrequency = function(freq) {
        $.ajax({
            url: "/setfreq?freq="+freq,
            dataType : 'json',
            type : 'GET',
            success: function(newData) {
            },
            error: function() {
            }
        });
    }  

    // status

    sendStatusRequest = function() {
        $.ajax({
            url: "/status",
            dataType : 'json',
            type : 'GET',
            success: function(newData) {
                curLocalChange = newData["localChange"];
                localChange = (curLocalChange != ddsweb.lastLocalChange);
                ddsweb.lastLocalChange = curLocalChange;

                if ((newData["curBand"]!=undefined) && (newData["curBand"]!=null)) {
                    $('#band-name').text(newData["curBand"]["name"]);
                    $('#band-start').text(newData["curBand"]["start"]);
                    $("#band-span").text(newData["curBand"]["span"]);

                    ddsweb.createDial(newData["curBand"]["start"] / ddsweb.dialStep,
                                      (newData["curBand"]["start"] + newData["curBand"]["span"]) / ddsweb.dialStep);
                }
                if (localChange) {
                    console.log("setfreq %s", newData["frequency"]);
                    $('#vfo-freq').val(newData["frequency"]);
                    ddsweb.lastFreq = newData["frequency"];
;
                    //ddsweb.dial.value = newData["frequency"] / this.dialStep;
                }
                console.log(newData);
            },
            error: function() {
                $('#band-name').text("unreachable");
                $('#band-start').text("unreachable");
                $('#band-span').text("unreachable");
            }
        });
        // Keep polling for info. Useful on errors to poll until we get a result.
        // Also useful on success to ensure we're still connected.
        setTimeout(ddsweb.sendStatusRequest, 1000);
    }

    onUpdateDial = function( e ) {
        var val = e.newVal;
        if ( isNaN( val ) ) {
            // Not a valid number.
            return;
        }
        $('#vfo-freq').val(val * 10);

        // Schedule a timer, prevent piling up a bunch of SetFrequency calls.
        if (ddsweb.timeoutAutoUpdate != undefined) {
            clearTimeout(ddsweb.timeoutAutoUpdate);
        }
        ddsweb.timeoutAutoUpdate = setTimeout(ddsweb.onVfoSetFreq, 25)
    }

    createDial = function( minVal, maxVal) {
        if ((minVal == this.lastMinDialVal) && (maxVal == this.lastMaxDialVal)) {
            return;
        }
        if (this.dial != undefined) {
            this.dial.destroy();
            this.dial = undefined;
        }
        YUI().use('dial', function(Y) {
            console.log(minVal);
            console.log(maxVal);
            var dial = new Y.Dial({
                min: minVal,
                max: maxVal,
                minorStep: 1,
                majorStep: 10,
                stepsPerRevolution:100,
                value: minVal
            });
            dial.render('#vfo-dial');
            dial.on( "valueChange", ddsweb.onUpdateDial);
            this.dial = dial;

            this.lastMinDialVal = minVal;
            this.lastMaxDialVal = maxVal;
        });
    }
          
    initButtons = function() {
        // navigation
        $("#nav-vfo").click(function(event) { ddsweb.onOpenTab(event, "tab-vfo"); })

        // buttons
        $("#vfo-freq-set").click(function() { ddsweb.onVfoSetFreq(); });

        // Frequency dial
        this.createDial(700000, 707400);

        // default tab
        $("#nav-vfo").click();

        // start requesting info
        ddsweb.sendStatusRequest();
    }

    startup = function() {
        this.dialStep = 10;
        this.postUI = true;
        this.lastFreq = 0;
        this.initButtons();
   }

   return this;
}

$(document).ready(function(){
    ddsweb = ddsweb();
    ddsweb.startup();
});
