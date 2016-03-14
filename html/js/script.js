var Config = null;

function SendCommand(module_id, switch_id, status) {
    var host = window.location.host;
    host = host.replace(":8080", "")
    var url = "http://" + host + ":9999/switch?module_id=" + module_id + "&switch_id=" + switch_id + "&status=" + status;
    //var dataToBeSent = '[{"status": "1"}]';
    $.post(url, function(data, textStatus) {
        console.log(data);
        console.log(textStatus);
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
        //$("#" + module_id).append("<li data-icon='false'><a href='#'><img src='" + (switchObj.status == "1" ? "green.png" : "red.png") + "' class='ui-li-icon'>" + switchObj.switch_id + "</a></li>");

        $("#" + mId).append("<li data-icon='false'><label for='" + sId + "'>" + switchObj.switch_id + "</label><span class='ui-btn-right' style='margin-top:.25em;'><select id='" + sId + "' data-role='flipswitch'><option value='off'>off</option><option value='on'>on</option></select></span></li>");
        $('#' + mId + ' #' + sId).flipswitch();
        if (module_status == "1") {
            if (switchObj.status == "1")
                $('#' + mId + ' #' + sId).off('change').val('on').flipswitch("refresh");
            else
                $('#' + mId + ' #' + sId).off('change').val('off').flipswitch("refresh");
            
            $('#' + mId + ' #' + sId).on('change', SwitchClicked);/*function(e) {
                var id = this.id;
                console.log(id);
            });*/
        } else {
            $('#' + mId + ' #' + sId).flipswitch('option', 'disabled', true);
        }
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
                if (oldSwitchId[j].status != newSwitchId[i].status) {
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

function ConfigReceived( data ) {

    //console.log(jQuery.isEmptyObject(data.config.modules));
    //console.log(filter(Config, data.config));
    
    //console.log(isEqual(Config, data.config));
    //if (isEqual(Config, data.config)) {
    //    return;
    //}
    $.mobile.loading("hide");
    
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

$(document).ready(function() {

    $.mobile.loading("show");
    var host = window.location.host;
    host = host.replace(":8080", "")
    $.getJSON( "http://" + host + ":9999/config", ConfigReceived).error(ErrorReceivingConfig);

    setInterval(function() {
        var host = window.location.host;
        host = host.replace(":8080", "")
        $.getJSON( "http://" + host + ":9999/config", ConfigReceived).error(ErrorReceivingConfig);
    }, 5000);


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
