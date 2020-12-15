# -*- coding: utf-8 -*-
import re

from odoo import models, fields, api


class Manufacturer(models.Model):
    _name = 'vehicle.manufacturer'

    name = fields.Char(required=True)
    logo = fields.Image(max_width=200, max_height=200)


class Brand(models.Model):
    _name = 'vehicle.brand'

    name = fields.Char(required=True)
    manufacturer = fields.Many2one('vehicle.manufacturer', required=True)


class Group(models.Model):
    _name = 'vehicle.group'

    name = fields.Char()
    parent_group = fields.Many2one('vehicle.group')


class OeNumber(models.Model):
    _name = 'vehicle.oe_number'
    _rec_name = 'number'

    number = fields.Char()
    product = fields.Many2one('product.template')


class VehicleType(models.Model):
    _name = 'vehicle.type'

    name = fields.Char(string="Display Name", required=True)
    brand = fields.Many2one('vehicle.brand', required=True)


class BodyStyle(models.Model):
    _name = 'vehicle.body_style'

    name = fields.Char()


class DriverCab(models.Model):
    _name = 'vehicle.driver_cab'

    name = fields.Char(string="Value")
    product = fields.Many2one('product.template')


class Description(models.Model):
    _name = 'vehicle.description'

    name = fields.Text(string="Description Text", required=True)


class Performance(models.Model):
    _name = 'vehicle.performance'

    name = fields.Char(string="Value", required=True)


class EngineCode(models.Model):
    _name = 'vehicle.engine_code'

    name = fields.Char(required=True, string="Code")


class Configuration(models.Model):
    _name = 'vehicle.config'

    name = fields.Char(required=True, string="Value")


class Tonnage(models.Model):
    _name = 'vehicle.tonnage'

    name = fields.Float(required=True, string="Value")


class Vehicle(models.Model):
    _name = 'vehicle.vehicle'

    name = fields.Char(required=True)


class Capacity(models.Model):
    _name = 'vehicle.capacity'

    name = fields.Float(string="Value")


def _cleaned(s):
    s = str(s)
    return re.sub('[,-.]', '', s).replace(' ', '')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    v_code = fields.Char(string="Code", required=True, unique=True)
    v_description1 = fields.Many2one('vehicle.description', string="Description 1")
    v_description2 = fields.Many2one('vehicle.description', string="Description 2")
    v_description3 = fields.Many2one('vehicle.description', string="Description 3")
    v_oe_num = fields.One2many('vehicle.oe_number', 'product', string="Oe numbers")
    v_alt_num = fields.Char(string="Alternative number")
    v_commercial_type = fields.Selection([('passenger', 'Passenger Car'), ('commercial', 'Commercial Vehicle')],
                                         'Select commercial vehicle', default='commercial')
    v_type = fields.Many2one('vehicle.type', string="Vehicle Type", default=False)
    v_brand = fields.Char("Brand", related="v_type.brand.name", store=True)
    v_manufacturer = fields.Char("Manufacturer", related="v_type.brand.manufacturer.name", store=True)
    v_performance = fields.Many2one('vehicle.performance', string="Perfomance")
    v_capacity = fields.Many2one('vehicle.capacity', string="Capacity")
    v_body_style = fields.Many2one('vehicle.body_style', string="Body style")
    v_config = fields.Many2one('vehicle.config', string="Configuration")
    v_tonnage = fields.Many2one('vehicle.tonnage', string="Tonnage")
    v_engine_type = fields.Selection([('petrol', 'Petrol'), ('diesel', 'Diesel')], 'Engine type', default='diesel')
    v_engine_codes = fields.Many2one('vehicle.engine_code', string="Engine codes")
    v_driver_cabs = fields.One2many('vehicle.driver_cab', 'product', string="Driver cabs")
    v_group = fields.Many2one("vehicle.group", string="Group")
    v_parent_group = fields.Many2one(related="v_group.parent_group", store=True)
    v_vehicle = fields.Many2one('vehicle.vehicle', string="Vehicle")
    v_supplier = fields.Many2one('res.partner', string="Supplier")

    # Separate search fields to help disregard special characters
    code_search = fields.Char(compute='compute_code_search', store=True)

    name_search = fields.Char(compute='compute_name_search', store=True)
    description_search = fields.Char(compute='compute_description_search', store=True)
    oe_num_search = fields.Char(compute='compute_oe_num_search', store=True)
    alt_num_search = fields.Char(compute='compute_alt_num_search', store=True)
    commercial_type_search = fields.Char(compute='compute_commercial_type_search', store=True)
    type_search = fields.Char(compute='compute_type_search', store=True)
    brand_search = fields.Char(compute='compute_brand_search', store=True)
    manufacturer_search = fields.Char(compute='compute_manufacturer_search', store=True)
    performance_search = fields.Char(compute='compute_performance_search', store=True)
    capacity_search = fields.Char(compute='compute_capacity_search', store=True)
    body_style_search = fields.Char(compute='compute_body_style_search', store=True)
    engine_codes_search = fields.Char(compute='compute_engine_codes_search', store=True)
    engine_type_search = fields.Char(compute='compute_engine_type_search', store=True)
    driver_cabs_search = fields.Char(compute='compute_driver_cabs_search', store=True)
    group_search = fields.Char(compute='compute_group_search', store=True)
    parent_group_search = fields.Char(compute='compute_parent_group_search', store=True)
    vehicle_search = fields.Char(compute='compute_vehicle_search', store=True)
    supplier_search = fields.Char(compute='compute_supplier_search', store=True)
    tonnage_search = fields.Char(compute='compute_tonnage_search', store=True)

    @api.depends('v_code')
    def compute_code_search(self):
        for product in self:
            product.code_search = _cleaned(product.v_code)

    @api.depends('v_description1', 'v_description2', 'v_description3')
    def compute_description_search(self):
        for product in self:
            product.description_search = _cleaned(
                product.v_description1.name + product.v_description2.name + product.v_description3.name)

    @api.depends('v_oe_num')
    def compute_oe_num_search(self):
        for product in self:
            product.oe_num_search = _cleaned(product.v_oe_num.number)

    @api.depends('v_alt_num')
    def compute_alt_num_search(self):
        for product in self:
            product.alt_num_search = _cleaned(product.v_alt_num)

    @api.depends('v_commercial_type')
    def compute_commercial_type_search(self):
        for product in self:
            product.commercial_type_search = _cleaned(product.v_commercial_type)

    @api.depends('v_type')
    def compute_type_search(self):
        for product in self:
            product.type_search = _cleaned(product.v_type.name)

    @api.depends('v_brand')
    def compute_brand_search(self):
        for product in self:
            product.brand_search = _cleaned(product.v_brand)

    @api.depends('v_manufacturer')
    def compute_manufacturer_search(self):
        for product in self:
            product.manufacturer_search = _cleaned(product.v_manufacturer)

    @api.depends('v_body_style')
    def compute_body_style_search(self):
        for product in self:
            product.body_style_search = _cleaned(product.v_body_style.name)

    @api.depends('v_engine_codes')
    def compute_engine_codes_search(self):
        for product in self:
            product.engine_codes_search = _cleaned(product.v_engine_codes.name)

    @api.depends('v_engine_type')
    def compute_engine_type_search(self):
        for product in self:
            product.engine_type_search = _cleaned(product.v_engine_type)

    @api.depends('v_performance')
    def compute_performance_search(self):
        for product in self:
            product.performance_search = _cleaned(product.v_performance.name)

    @api.depends('v_capacity')
    def compute_capacity_search(self):
        for product in self:
            product.capacity_search = _cleaned(product.v_capacity.name)

    @api.depends('v_driver_cabs')
    def compute_driver_cabs_search(self):
        for product in self:
            product.driver_cabs_search = _cleaned(product.v_driver_cabs.name)

    @api.depends('v_group')
    def compute_group_search(self):
        for product in self:
            product.group_search = _cleaned(product.v_group.name)

    @api.depends('v_parent_group')
    def compute_parent_group_search(self):
        for product in self:
            product.parent_group_search = _cleaned(product.v_parent_group.name)

    @api.depends('v_vehicle')
    def compute_vehicle_search(self):
        for product in self:
            product.vehicle_search = _cleaned(product.v_vehicle.name)

    @api.depends('v_supplier')
    def compute_supplier_search(self):
        for product in self:
            product.supplier_search = _cleaned(product.v_supplier.name)

    @api.depends('v_tonnage')
    def compute_tonnage_search(self):
        for product in self:
            product.tonnage_search = _cleaned(product.v_tonnage.name)

    @api.depends('description_search', 'oe_num_search', 'alt_num_search', 'commercial_type_search', 'type_search',
                 'brand_search', 'manufacturer_search', 'performance_search', 'capacity_search', 'body_style_search',
                 'engine_codes_search', 'engine_type_search', 'driver_cabs_search', 'group_search',
                 'parent_group_search', 'vehicle_search', 'vehicle_search', 'supplier_search', 'tonnage_search')
    def compute_name_search(self):
        for product in self:
            product.name_search = _cleaned(product.code_search + product.name + product.description_search + product.oe_num_search + product.alt_num_search + product.commercial_type_search + product.type_search + product.brand_search + product.brand_search + product.manufacturer_search + product.performance_search + product.capacity_search + product.body_style_search + product.engine_codes_search + product.engine_type_search + product.driver_cabs_search + product.group_search + product.parent_group_search + product.vehicle_search + product.supplier_search + product.tonnage_search)
