define(['jquery'], function ($) {
        var sideBar_interface = {};
        var activeBar;

        function init_self() {
            $(".sidebar").children().each(function (i, ul) {
                $(ul).children().each(function (j, li) {
                    if ($(li).hasClass("active"))
                        activeBar = li;
                    $(li).unbind("click").click(function (e) {
                        clickBar(e);
                    });
                });
            });
        }
        function clickBar(e) {
            $(activeBar).removeClass("active");
            $(e.currentTarget).addClass("active");
            activeBar = e.currentTarget;
        };

        sideBar_interface.init = init_self;
        return sideBar_interface;
    }
);