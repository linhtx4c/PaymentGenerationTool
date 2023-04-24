define([
    'uiComponent',
    'Magento_Checkout/js/model/payment/renderer-list'
], function (
    Component,
    rendererList
) {
    'use strict';

    rendererList.push(
        {
            type: 'payment_code',
            component: 'ComponentName/js/view/payment/method-renderer/payment_code'
        }
    );
    return Component.extend({});
});
