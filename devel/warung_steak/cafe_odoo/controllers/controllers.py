from odoo import http, tools, _
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class WebsiteArkana(http.Controller):
    model_fields = {
        'cafe.order': ['id', 'name', 'note', 'state']
    }

    @http.route('/api/<model>/get', type='json', methods=['GET'], auth="none")
    def get_values_model(self, model, *args, **kwargs):
        url_parameter = http.request.httprequest.args
        # 1. Panggil Tablenya, self.env = http.request.env
        Model = http.request.env[model].sudo()
        # 2. Search All
        rows = Model.search([], limit=(int(url_parameter.get('limit', 5))))
        # 3. Read fields agar jadi
        value_rows = rows.read(self.model_fields[model] if model in self.model_fields else ['id', 'name'])
        return {
            'data': value_rows,
            'code': 200,
        }