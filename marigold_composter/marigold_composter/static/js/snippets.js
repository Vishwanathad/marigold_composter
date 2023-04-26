odoo.define('marigold_composter.dynamic', function (require) {
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var ajax = require("web.ajax");

    var Dynamic = PublicWidget.Widget.extend({
        selector: '.marigold_numbers',
        start: function () {
            var self = this;
            rpc.query({
                route: '/total_waste_count',
                params: {},
            }).then(function (result) {
                self.$('#span_no_of_homes_count').text(result.no_of_homes);
                self.$('#span_collected_waste_count').text(result.collected_waste);
                self.$('#span_proceesed_cocopeat_count').text(result.proceesed_cocopeat);
                self.$('#span_proceesed_compost_count').text(result.proceesed_compost);
                self.$('#span_sieved_compost_count').text(result.sieved_compost);
            });
        },
    });
    PublicWidget.registry.marigold_composter = Dynamic;
    return Dynamic;


});