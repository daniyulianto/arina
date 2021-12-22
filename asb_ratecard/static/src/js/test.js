odoo.define('asb_ratecard.ratecard_form', function(require) {
    'use strict';

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    const view_registry = require('web.view_registry');

    var RateCardFormController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'keyup .click_partner': '_OnClickPartner',
        }),
        _OnClickPartner: function(event) {
            var id = document.getElementById(event.currentTarget.id)
            var id_class = document.getElementsByClassName('o_form_button_save')
            var toast = document.getElementById("snackbar");
            if (isNaN(id.value)) {
                toast.className = "show";
                setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 3000);
                id_class[0].setAttribute('disabled', 'disabled');
                id.classList.add('border-danger');
            } else {
                id_class[0].removeAttribute('disabled');
                id.classList.remove('border-danger');
            }
        }
    });

    var RateCardFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: RateCardFormController,
        }),
    });

    view_registry.add('rate_card_form_view', RateCardFormView);
});