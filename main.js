// 解析 url 参数
function requestParameter(paras) {
    var url = window.parent.location.href;
    var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
    var paraObj = {}
    for (i = 0; j = paraString[i]; i++) {
        paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
    }
    var returnValue = paraObj[paras.toLowerCase()];
    if (typeof (returnValue) == "undefined") {
        return "";
    } else {
        return returnValue;
    }
}

$(document).ready(function() {
    // :hover patch for IE
    var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    var isOpera = userAgent.indexOf("Opera") > -1; //判断是否Opera浏览器
    var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera; //判断是否IE浏览器
    var enable = false;
    
    if (isIE) {
        var reIE = new RegExp(/MSIE (\d+\.\d+);/);
        reIE.test(userAgent);
        var IEVersion = parseFloat(RegExp["$1"]);

        // IE < 8 doesn't support :hover
        if (IEVersion < 8.0) {
            enable = true;
        }
    }
    // Debugging
    //enable = true;
    
    if (enable) {
        $(".MenuNav > li").hover(function() {
            $(this).find(".MenuItem").css("visibility", "visible");
        }, function() {
            $(this).find(".MenuItem").css("visibility", "hidden");
        });
        
        $(".MenuItem li").hover(function() {
            $(this).css("background", "#eee");
        }, function() {
            $(this).css("background", "#fff");
        });
        
        $(".boxRightBorder").hover(function() {
            $(this).css("background-position", "-143px 0px");
        }, function() {
            $(this).css("background-position", "-31px 0px");
        });
        
        $(".boxRightBorder").mousedown(function() {
            $(this).css("background-position", "-255px 0px");
        });
        
        $(".boxRightBorder").mouseup(function() {
            $(this).css("background-position", "-143px 0px");
        });
    } else {
        //console.log("CSS3 patch bypassed");
    }
    
    // If searchResultTable is present, hide the logo
    if ($("#searchResultTable").length != 0) {
        $("#lg").hide();
    } else {
    	$("#keyword").select();
    }
    
    // Copy parameter keyword to the input box
    var keyword = requestParameter("keyword");
    if (keyword) {
        $("#keyword").val(keyword);
    }
    
});
