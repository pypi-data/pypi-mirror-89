from odoo import fields, models


class ServiceSupplier(models.Model):
    _name = 'service.supplier'
    name = fields.Char('Name')


class ServiceTechnologyServiceSuplier(models.Model):
    _name = 'service.technology.service.supplier'
    service_supplier_id = fields.Many2one('service.supplier', 'Supplier')
    service_technology_id = fields.Many2one(
        'service.technology',
        'Technology')
