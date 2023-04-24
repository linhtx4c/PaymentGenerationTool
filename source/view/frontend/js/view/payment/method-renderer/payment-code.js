define([
    'ko',
    'jquery',
    'mage/url',
    'Magento_Checkout/js/view/payment/default',
    'uiLayout'
], function (
    ko,
    $,
    url,
    Component,
    layout
) {
    'use strict';
    return Component.extend({
        defaults: {
            template: 'ComponentName/payment/payment_code',
        },

        /**
         * initialize function
         */
        initialize: function () {
            this._super();
        }
    });
});
