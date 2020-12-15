odoo.define('vehicle_details.AutoComplete', function (require) {
    "use strict";
    let auto_complete = require('web.AutoComplete');
    auto_complete.include({
        remove_special:function(string){
            return string.replace(/[&\/\\#,~%.'":*?<>-]/g, '').replace(/ /g,'')
        },
        _updateSearch: function () {
            var search_string = this.remove_special(this.get_search_string());
            if (this.search_string !== search_string) {
                if (search_string.length) {
                    this.search_string = search_string;
                    this.initiate_search(search_string);
                } else {
                    this.close();
                }
            }
        },
        expand: function () {
            var self = this;
            var current_result = this.current_result;
            current_result.expand(this.remove_special(this.get_search_string())).then(function (results) {
                (results || [{label: '(no result)'}]).reverse().forEach(function (result) {
                    result.indent = true;
                    var $li = self.make_list_item(result);
                    current_result.$el.after($li);
                });
                self.current_result.expanded = true;
                self.current_result.$el.find('a.o-expand').removeClass('o-expand').addClass('o-expanded');
            });
        },
    })
})