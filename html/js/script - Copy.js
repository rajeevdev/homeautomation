var searchKey;

var BASE_URL = "http://kartsearch.zz.mu";
//var BASE_URL = "http://localhost";
function getAllProductCategoryXML(xml) {
	$("#resultArea").empty();
	
	var elements = xml.getElementsByTagName("get")
	for (var i = 0; i < 5; ++i) {
		var url = elements[i].textContent;
		$("#resultArea").append("<div style='border: 1px solid grey;width:calc(100% - 4px);height:auto;'><a id='linkContainer' href='#'>" + url + "<a><div>");
	}
	
	$("#linkContainer").click( function() {
		
		var param = $(this).text().replace("&", "??");
		var url = "http://kartsearch.zz.mu/api.php?url=" + param;
		$.get(url, getProductListXML, "xml");
	});
}

function getAllProductCategoryJSON(json) {
	$.each(json.apiGroups.affiliate.apiListings, function(i, v) {
		var url = v.availableVariants["v0.1.0"].get;
		var id = v.availableVariants["v0.1.0"].resourceName;
		$("#resultArea").append("<div style='border: 1px solid grey;width:calc(100% - 4px);height:auto;'><a id='" + id + "' href='#'>" + url + "<a><div>");
	});
	
	$("#resultArea a").click( function() {
		
		var param = $(this).text().replace("&", "@@@@@");
		var url = "http://kartsearch.zz.mu/api.php?url=" + param;
		$.get(url, getProductListJSON, "json");
	});	
}

function getProductListXML(xml) {
	var xmlText = new XMLSerializer().serializeToString(xml);
}

function getProductListJSON(json) {
	console.log(json);
}

function searchProduct() {
	//searchKey = $("#searchKey").val();
	//var url = "http://kartsearch.zz.mu/api.php?" + key;
	
	//var url = "http://kartsearch.zz.mu/api.php?url=https://affiliate-api.flipkart.net/affiliate/api/rajeevdev.xml";
	//$.get(url, getAllProductCategoryXML, "xml");
	
	//var url = "http://kartsearch.zz.mu/api.php?url=https://affiliate-api.flipkart.net/affiliate/api/rajeevdev.json";
	//$.get(url, getAllProductCategoryJSON, "json");
	
	var url = BASE_URL + "/flipkartapi.php?key=" + searchKey;
	$.get(url, searchProductList, "json").fail(function() {
		$.mobile.loading("hide");
		$("body").removeClass('ui-disabled');	
		$( "#errorPopup" ).popup( "open" );
	});
	
	$('#search').blur();
	$("body").addClass('ui-disabled');
	$.mobile.loading( 'show', {
		text: 'Searhing. Please wait...',
		textVisible: true,
		theme: 'z',
		html: ""
	});
}

function searchProductList(json) {

	$("#item-container").empty();

	$.each(json.productInfoList, function(i, v) {
		var imageUrl = v.productBaseInfo.productAttributes.imageUrls["200x200"];
		var productUrl = v.productBaseInfo.productAttributes.productUrl;
		var price = v.productBaseInfo.productAttributes.sellingPrice["amount"];
		var maximumPrice = v.productBaseInfo.productAttributes.maximumRetailPrice["amount"];
		var title = v.productBaseInfo.productAttributes.title;

		$("#item-container").append("<li class='ui-li-has-thumb ui-first-child' url='" + productUrl + "'><a href='#' class='ui-btn ui-btn-icon-right ui-icon-carat-r'>" +
            	"<img src='" + imageUrl + "' class='ui-li-thumb'>" +
				"<h2>" + title + "</h2>" +
                "<p>MRP Rs. " + maximumPrice + "</p>" +
				"<p>Offer Price Rs. " + price + "</p>" +
				"</a></li>");
	});
	
	$.mobile.loading("hide");
	$("body").removeClass('ui-disabled');	
	
	$('#item-container li').click('click', function(e) {
		e.preventDefault();
		var targetURL = $(this).attr("url");
		window.open(targetURL, "_system");
    });
}

var counter = 1;
function AddModule(module_id, status, switchList) {
    console.log(module_id);
    console.log(status);
    console.log(switchList);
    
    //var element = "<p>" + module_id + "</p>";
    //element += "<p>" + (status == "1" ? "Connected" : "Disconnected") + "</p>";
    //$("#resultArea").append(element);

    var template = $('#template').clone();
    templateId = "template" + counter.toString();
    newModuleId = "module-id" + counter.toString();
    newStatusId = "module-status" + counter.toString();
    newSliderId = "template-slider" + counter.toString();
    template.show();
    template.find("ul").attr("data-role", "listview");
    template.find("ul").attr("data-inset", "true");
    template.find("ul li").attr("data-role", "fieldcontain");
    template.find('#module-id').text(module_id);
    template.find('#module-status').text((status == "1" ? "Connected" : "Disconnected"));
    template.find('#module-id').attr("id", newModuleId);
    template.find('#module-status').attr("id", newStatusId);
    template.find('label').attr("for", newSliderId);
    template.find('select').attr("id", newSliderId);
    template.find('select').attr("data-role", "slider");
    template.find('select').attr("name", "testslider");
    template.attr("id", templateId)
    template.appendTo("#resultArea")
    template.trigger("refresh");
    counter++;
    //$('#test-slider').slider('refresh');
    //$("#template").trigger('create');
    //$("#template").listview('refresh');
    
    //$("#resultArea").append(element);
    //var element1 =
        //"<ul data-role='listview' data-inset='true' id='" + module_id + "-ul'>";
    /*
    for (var i = 0; i < switchList.length; ++i) {
        var switchObj = switchList[i];
        console.log(switchObj.switch_id);
        console.log(switchObj.status);
        element1 += "<li data-role='fieldcontain'>";
        element1 += "<label for='" + module_id + "-slider'>" + switchObj.switch_id + "</label>";
        element1 += "<select id='" + module_id + "-slider' data-role='slider' name='testslider'>";
        element1 += "<option value='off'>off</option>";
        element1 += "<option value='on'>on</option>";
        element1 += "</select>";
        element1 += "</li>";
    }
    element1 += "</ul>";
    $("#resultArea").append(element1);
    
    //$( "#resultArea" ).pagecontainer( "load" );

    
    $('#' + module_id + '-ul').listview().listview('refresh');
    $('#' + module_id + '-slider').slider('refresh');
    */
}

$(document).ready(function() {

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
                  "status": "1",
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
    }
});
/*
(function( $, window, undefined ) {
	$.widget( "mobile.listview", $.mobile.listview, {
		options: {
			childPages: true,
			page: "<div data-role='page'></div>",
			header: "<div data-role='header'><a href='#' data-rel='back'>Back</a><h1></h1></div>",
			content: "<div class='ui-content'></div>"
		},
		_create: function(){
			this._super();
			if( this.options.childPages ) {
				this._setupChildren();
			}
		},
		_setupChildren: function() {
			this._attachBindings();
			this.element.find( "ul" )
				.css( "display","none" )
				.parent()
				.addClass("ui-btn ui-btn-icon-right ui-icon-carat-r");
		},
		_attachBindings: function() {
			this._on({
				"click": "_handleSubpageClick"
			});
			this._on( "body", {
				"pagechange": function(){
					if ( this.opening === true ) {
						this.open = true;
						this.opening = false;
					} else if ( this.open === true ) {
						this.newPage.remove();
						this.open = false;
					}
				}
			});
		},
		_handleSubpageClick: function( event ) {
			if( $(event.target).closest( "li" ).children( "ul" ).length == 0 ) {
				return;
			}
			this.opening = true;
			this.newPage = $( this.options.page ).uniqueId();
			this.nestedList  = $( event.target ).children( "ul" )
				.clone().attr( "data-" + $.mobile.ns + "role", "listview" )
				.css( "display", "block" );
			this.pageName = (
				$( event.target.childNodes[0] ).text().replace(/^\s+|\s+$/g, '').length > 0 )?
				$( event.target.childNodes[0] ).text() : $( event.target.childNodes[1] ).text();
			this.pageID = this.newPage.attr( "id" );

			// Build new page
			this.newPage.append(
				$( this.options.header ).find( "h1" ).text( this.pageName ).end()
			).append(
				$( this.options.content )
			).find( "div.ui-content" ).append( this.nestedList );

			$( "body" ).append( this.newPage );

			$( "body" ).pagecontainer( "change", "#" + this.pageID );
		}
	});
})( jQuery, this );*/