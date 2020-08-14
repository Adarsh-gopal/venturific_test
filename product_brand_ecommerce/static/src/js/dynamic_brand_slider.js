odoo.define('product_brand_ecommerce.dynamic_brand_slider', function (require) {

var concurrency = require('web.concurrency');
var config = require('web.config');
var core = require('web.core');
var publicWidget = require('web.public.widget');
var utils = require('web.utils');
var wSaleUtils = require('website_sale.utils');

var qweb = core.qweb;

publicWidget.registry.DynamicBrandSliderSnippet = publicWidget.Widget.extend({
    selector: '.s_wsale_dynamic_brand_slider',
    xmlDependencies: ['/product_brand_ecommerce/static/src/xml/dynamic_brand_slider.xml'],
    disabledInEditableMode: false,

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        this._dp = new concurrency.DropPrevious();
        this.uniqueId = _.uniqueId('o_carousel_brand_slider');
        this._onResizeChange = _.debounce(this._addCarousel, 100);
    },
    /**
     * @override
     */
    start: function () {
        this._dp.add(this._fetch()).then(this._render.bind(this));
        $(window).resize(() => {
            this._onResizeChange();
        });
        return this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    destroy: function () {
        this._super(...arguments);
        this.$el.addClass('d-none');
        this.$el.find('.slider').html('');
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _fetch: function () {
        return this._rpc({
            route: '/dynamic/brand/carousel',
        }).then(res => {
            var brands = res['brands'];
            console.log(brands);

            return res;
        });
    },
    /**
     * @private
     */
    _render: function (res) {
        var brands = res['brands'];
        var mobileBrands = [], webBrands = [], brandTemp = [];
        _.each(brands, function (brand) {
            if (brandTemp.length === 6) {
                webBrands.push(brandTemp);
                brandTemp = [];
            }
            brandTemp.push(brand);
            mobileBrands.push([brand]);
        });
        if (brandTemp.length) {
            webBrands.push(brandTemp);
        }

        this.mobileCarousel = $(qweb.render('product_brand_ecommerce.dynamicBrandSlider', {
            uniqueId: this.uniqueId,
            brandFrame: 1,
            brandsGroups: mobileBrands,
        }));
        this.webCarousel = $(qweb.render('product_brand_ecommerce.dynamicBrandSlider', {
            uniqueId: this.uniqueId,
            brandFrame: 6,
            brandsGroups: webBrands,
        }));
        this._addCarousel();
        this.$el.toggleClass('d-none', !(brands && brands.length));
    },
    /**
     * Add the right carousel depending on screen size.
     * @private
     */
    _addCarousel: function () {
        var carousel = config.device.size_class <= config.device.SIZES.SM ? this.mobileCarousel : this.webCarousel;
        this.$('.slider').html(carousel).css('display', ''); // TODO removing the style is useless in master
    },




});


});
