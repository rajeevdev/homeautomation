var Config = null;
var ConfigTimer = null;

function SendCommand(module_id, switch_id, status) {
    clearInterval(ConfigTimer);
    ConfigTimer = null;
    
    $("body").append('<div class="modalWindow"/>');
    $.mobile.loading("show");
    
    var host = window.location.host;
    host = host.replace(":8080", "")
    var url = "http://" + host + ":9999/switch?module_id=" + module_id + "&switch_id=" + switch_id + "&status=" + status;
    //var dataToBeSent = '[{"status": "1"}]';
    $.post(url, function(data, textStatus) {
        //$.mobile.loading("hide");
        //console.log(data);
        //console.log(textStatus);
        GetConfig();
        //console.log(module_id);
        //data contains the JSON object
        //textStatus contains the status: success, error, etc
    }, "json");
    
    /*$.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(dataToBeSent),//'{"name":"jonas"}', // or JSON.stringify ({name: 'jonas'}),
        success: function(data) { alert('data: ' + data); },
        contentType: "application/json",
        dataType: 'json'
    });*/
}

function SwitchClicked(e) {
    var id = this.id;
    var value = this.value;
    
    var index = id.search("_");
    var module_id = id.substring(0, index);
    var switch_id = id.substring(index + 1, id.length);
    var status = ((value == "on") ? "1" : "0");
    console.log(module_id);
    console.log(switch_id);
    console.log(status);
    SendCommand(module_id, switch_id, status);
}

function AddModule(module_id, module_status, switchList) {
    //console.log(module_id);
    //console.log(status);
    //console.log(switchList);
    
    var mId = module_id;

    $("#resultArea").append("<ul data-role='listview' data-inset='true' id='" + mId + "'></ul>");
    $("#" + mId).append("<li data-role='list-divider'><p><b>Module ID : </b><i>" + mId + "</i></p><p><b>Status : </b><i>" + (module_status == "1" ? "Connected" : "Disconnected") + "</i></p></li>");
    for (var i = 0; i < switchList.length; ++i) {
        var switchObj = switchList[i];
        //console.log(switchObj.switch_id);
        //console.log(switchObj.status);
        
        var sId = module_id + '_' + switchObj.switch_id;
        $("#" + mId).append("<li data-icon='false' id='" + sId + "'><a href='#'><img src='" + (switchObj.status == "1" ? "images/green.png" : "images/red.png") + "' class='ui-li-icon'>" + switchObj.switch_id + "</a></li>");

        if (module_status == "0") {
            $("#" + sId).addClass("ui-state-disabled");
        }
        
        /*$("#" + mId).append("<li data-icon='false'><label>" + switchObj.switch_id + "</label><span class='ui-btn-right' style='margin-top:.25em;'><select id='" + sId + "' data-role='flipswitch'><option value='off'>off</option><option value='on'>on</option></select></span></li>");
        $('#' + mId + ' #' + sId).flipswitch();
        if (module_status == "1") {
            if (switchObj.status == "1")
                $('#' + mId + ' #' + sId).off('change').val('on').flipswitch("refresh");
            else
                $('#' + mId + ' #' + sId).off('change').val('off').flipswitch("refresh");
            
            $('#' + mId + ' #' + sId).on('change', SwitchClicked);
        } else {
            $('#' + mId + ' #' + sId).flipswitch('option', 'disabled', true);
        }*/
    }
    
    $('#' + mId).listview().listview('refresh');
    
}

function IsSwitchsEqual(newSwitches, oldSwitches) {
    for (var i = 0; i < newSwitches.length; ++i) {
        var newSwitchId = newSwitches[i].switch_id;
        
        var switchFound = false;
        for (var j = 0; j < oldSwitches.length; ++j) {
            var oldSwitchId = oldSwitches[j].switch_id;
            if (oldSwitchId == newSwitchId) {
                switchFound = true;
                if (oldSwitches[j].status != newSwitches[i].status) {
                    return false;
                }
                break;
            }
        }
        
        if (switchFound == false) {
            return false;
        }        
    }
    return true;
}

function IsConfigEqual(newModules) {
    if (Config == null)
        return false;

    var oldModules = Config.modules.module;
    for (var i = 0; i < newModules.length; ++i) {
        var newModuleId = newModules[i].module_id;
        
        var moduleFound = false;
        for (var j = 0; j < oldModules.length; ++j) {
            var oldModuleId = oldModules[j].module_id;
            
            if (oldModuleId == newModuleId) {
                moduleFound = true;
                if (oldModules[j].status == newModules[i].status) {
                    
                    newSwitches = newModules[i].switch;
                    oldSwitches = oldModules[j].switch;
                    
                    if (IsSwitchsEqual(newSwitches, oldSwitches) == false)
                        return false;
                        
                } else {
                    return false;
                }
                break;
            }
        }
        
        if (moduleFound == false) {
            return false;
        }
    }
    
    return true;
}

function ConfigReceived( data , res, xhr ) {

    $(".modalWindow").remove();
    $.mobile.loading("hide");
    
    connected = xhr.getResponseHeader("Connected");
    if (connected == "0") {
        $("#resultArea").empty();
        $("#resultArea").append("<div id='alertdiv'>NOT CONNECTED</div>");
        Config = null;
        return;
    }

    var modules = data.config.modules.module;    
    if (IsConfigEqual(modules) == false) {
        console.log("Config not equal");
        $("#resultArea").empty();
        for (var i = 0; i < modules.length; ++i) {
            var module = modules[i];
            AddModule(module.module_id, module.status, module.switch)
        }
    } else {
        console.log("Config equal");
    }
    Config = data.config;
}

function ErrorReceivingConfig() {
    $("#resultArea").empty();
    Config = null;
}

function GetConfig() {
    var host = window.location.host;
    host = host.replace(":8080", "")
    host = host.replace(":80", "")
    host = host.replace(":9999", "")
    $.getJSON( "http://" + host + "/php/api.php?request=get_config&system_id=94a596f0-e83c-11e5-b8cb-5c260a2f8a10", ConfigReceived).error(ErrorReceivingConfig);
    
    if (ConfigTimer == null) {
        ConfigTimer = setInterval(GetConfig, 5000);
    }
}

$(document).ready(function() {
    $("body").append('<div class="modalWindow"/>');
    $.mobile.loading("show");
    //setTimeout('hideModal()', 2000);
  
    //$.mobile.loading("show");
    GetConfig();


/*

var data =     
    {
      "config": {
        "modules": {
          "module": [
            {
              "module_id": "11-11-11-11-11-11",
              "status": "1",
              "switch": [
                {
                  "status": "1",
                  "switch_id": "relay1"
                },
                {
                  "status": "0",
                  "switch_id": "relay2"
                }
              ]
            },
            {
              "module_id": "22-22-22-22-22-22",
              "status": "0",
              "switch": [
                {
                  "status": "1",
                  "switch_id": "relay1"
                },
                {
                  "status": "1",
                  "switch_id": "relay2"
                }
              ]
            }
          ]
        },
        "system_id": "eb409d70-e03f-11e5-8387-80000b819f1a"
      }
    }

    //console.log(jQuery.isEmptyObject(data.config.modules));
    
    var modules = data.config.modules.module;
    for (var i = 0; i < data.config.modules.module.length; ++i) {
        var module = data.config.modules.module[i];
        //console.log(data.config.modules.module[i]);
        AddModule(module.module_id, module.status, module.switch)
    }*/
});
