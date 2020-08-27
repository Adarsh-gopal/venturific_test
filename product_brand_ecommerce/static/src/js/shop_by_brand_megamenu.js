odoo.define('product_brand_ecommerce.brand_megamenu', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    var concurrency = require('web.concurrency');
    var config = require('web.config');
    var core = require('web.core');
    var utils = require('web.utils');
    var wSaleUtils = require('website_sale.utils');
    var qweb = core.qweb;

    publicWidget.registry.shop_by_brand_megamenu = publicWidget.Widget.extend({
        selector: ".shop_by_brand_megamenu",
        xmlDependencies: ['/product_brand_ecommerce/static/src/xml/shop_by_brand_megamenu.xml'],

         init: function () {
            this._super.apply(this, arguments);
            this._dp = new concurrency.DropPrevious();
        },

        start: function () {
            this._dp.add(this._fetch()).then(this._render.bind(this));
            return this._super.apply(this, arguments);
        },

        _fetch: function(){

        return this._rpc({
            route: '/dynamic/brand/megamenu',
            }).then(res => {
                var brands = res['brands'];
                  return res;
            });
        },

        _render: function (res) {
            var brands = res['brands'];

            var brandlist = [];
            _.each(brands, function (brnd) {
                brandlist.push([brnd]);
            });

            this.brandslist = $(qweb.render('product_brand_ecommerce.shopbybrand', {
                brandsGroupsNew: brandlist,
            }));

            this.$('.brand-megamenu').html(this.brandslist);
        },

    });
});