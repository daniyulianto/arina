odoo.define('asb_quota.quota_dashboard', function(require) {
    'use strict';
    
    var ListController = require('web.ListController');
    var ListRenderer = require('web.ListRenderer');
    var ListModel = require('web.ListModel');
    var ListView = require('web.ListView');
    const view_registry = require('web.view_registry');
    const core = require('web.core');
    const Qweb = core.qweb;

    var QuotaListDashboardController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .qd_open_action': '_OnClickOpenQuota'
        }),
        _OnClickOpenQuota: function(event) {
            event.preventDefault();
            var $action =  $(event.currentTarget);
            var context =  $action.attr('context') ||  '{}';
            return this.do_action($action.attr('action'), {
                additional_context: JSON.parse(context)
            })
        }
    });

    var QuotaListDashboardRenderer = ListRenderer.extend({
        async _render(){
            await this._super(...arguments);
            var result = this.state.quotaDasboardData;
            this.$el.parent().find('.qd_container').remove();
            const quotaDasboard = $(Qweb.render('Quota.Dashboard', {
                active: result.active,
                hold: result.hold,
                done: result.done
            }));
            this.$el.before(quotaDasboard);
        }
    });

    var QuotaListDashboardModel = ListModel.extend({
        init: function(){
            this.quotaDasboardData = {};
            this._super.apply(this, arguments);
        },
        __get: function(Id){
            var result = this._super.apply(this, arguments);
            if(_.isObject(result)){
                result.quotaDasboardData = this.quotaDasboardData[Id];
            }
            return result;
        },
        __load: function(){
            return this._loadQuotaDashboard(this._super.apply(this,arguments));
        },
        __reload: function(){
            return this._loadQuotaDashboard(this._super.apply(this,arguments));
        },
        _loadQuotaDashboard: function(prom){
            const quotaPromise = this._rpc({
                model: "quota.quota",
                method: "retrieve_quota_dashboard",
            });
            return Promise.all([prom, quotaPromise]).then((results) => {
                let [dataPointId, quotaResult] = results;
                this.quotaDasboardData[dataPointId] = quotaResult;
                return dataPointId;
            })
        }
    });

    var QuotaListDashboardView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Model: QuotaListDashboardModel,
            Renderer: QuotaListDashboardRenderer,
            Controller: QuotaListDashboardController,
        }),
    });

    view_registry.add('quota_list_dashboard', QuotaListDashboardView);
});