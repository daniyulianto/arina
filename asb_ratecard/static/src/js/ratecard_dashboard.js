odoo.define('asb_ratecard.ratecard_dashboard', function(require) {
    'use strict';
    
    var ListController = require('web.ListController');
    var ListRenderer = require('web.ListRenderer');
    var ListModel = require('web.ListModel');
    var ListView = require('web.ListView');
    const view_registry = require('web.view_registry');
    const core = require('web.core');
    const Qweb = core.qweb;

    var RatecardListDashboardController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .sd_open_action': '_OnClickOpenRatecard',
        }),
        _OnClickOpenRatecard: function(event) {
            event.preventDefault();
            var $action =  $(event.currentTarget);
            var context =  $action.attr('context') ||  '{}';
            return this.do_action($action.attr('action'), {
                additional_context: JSON.parse(context)
            })
        }
    });

    var RatecardListDashboardRenderer = ListRenderer.extend({
        async _render(){
            await this._super(...arguments);
            var result = this.state.ratecardDasboardData;
            this.$el.parent().find('.sd_container').remove();
            const ratecardDasboard = $(Qweb.render('Ratecard.Dashboard', {
                draft: result.draft,
                quotation: result.quotation,
                approved: result.approved
            }));
            this.$el.before(ratecardDasboard);
        }
    });

    var RatecardListDashboardModel = ListModel.extend({
        init: function(){
            this.ratecardDasboardData = {};
            this._super.apply(this, arguments);
        },
        __get: function(Id){
            var result = this._super.apply(this, arguments);
            if(_.isObject(result)){
                result.ratecardDasboardData = this.ratecardDasboardData[Id];
            }
            return result;
        },
        __load: function(){
            return this._loadRatecardDashboard(this._super.apply(this,arguments));
        },
        __reload: function(){
            return this._loadRatecardDashboard(this._super.apply(this,arguments));
        },
        _loadRatecardDashboard: function(prom){
            const ratecardPromise = this._rpc({
                model: "rate.card",
                method: "retrieve_ratecard_dashboard",
            });
            return Promise.all([prom, ratecardPromise]).then((results) => {
                let [dataPointId, ratecardResult] = results;
                this.ratecardDasboardData[dataPointId] = ratecardResult;
                return dataPointId;
            })
        }
    });

    var RatecardListDashboardView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Model: RatecardListDashboardModel,
            Renderer: RatecardListDashboardRenderer,
            Controller: RatecardListDashboardController,
        }),
    });

    view_registry.add('ratecard_list_dashboard', RatecardListDashboardView);
});