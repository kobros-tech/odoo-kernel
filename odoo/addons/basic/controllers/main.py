# -*- coding: utf-8 -*-
# Part of kobros-tech. See LICENSE file for full copyright and licensing details.

import re
import werkzeug.exceptions
import werkzeug.urls
from odoo import http, _
from odoo.http import request, route, Controller
from odoo import http, tools, _, SUPERUSER_ID, release
from odoo.addons.web_editor.controllers.main import Web_Editor
    

class Custom_Editor(Web_Editor):

    def _update_svg_colors(self, options, svg):
        user_colors = []
        svg_options = {}
        default_palette = {
            '1': '#3AADAA',
            '2': '#7C6576',
            '3': '#F6F6F6',
            '4': '#FFFFFF',
            '5': '#383E45',
        }
        bundle_css = None
        regex_hex = r'#[0-9A-F]{6,8}'
        regex_rgba = r'rgba?\(\d{1,3}, ?\d{1,3}, ?\d{1,3}(?:, ?[0-9.]{1,4})?\)'
        for key, value in options.items():
            colorMatch = re.match('^c([1-5])$', key)
            if colorMatch:
                css_color_value = value
                user_colors.append([tools.html_escape(css_color_value), colorMatch.group(1)])
            else:
                svg_options[key] = value

        color_mapping = {default_palette[palette_number]: color for color, palette_number in user_colors}
        # create a case-insensitive regex to match all the colors to replace, eg: '(?i)(#3AADAA)|(#7C6576)'
        regex = '(?i)%s' % '|'.join('(%s)' % color for color in color_mapping.keys())

        def subber(match):
            key = match.group().upper()
            return color_mapping[key] if key in color_mapping else key
        return re.sub(regex, subber, svg), svg_options
    