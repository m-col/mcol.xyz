# -*- coding: utf-8 -*-
#
# fontawesome_roles
#
# Registers the :fas:/:far:/:fab: RST roles used in posts to embed inline
# Font Awesome icons, e.g. :fas:`envelope` -> <span class="fas fa-envelope">.
# The icon font/CSS itself is loaded separately (see EXTRAHEAD).

from docutils import nodes
from docutils.parsers.rst import roles


def rst_span(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return [nodes.raw("", f'<span class="{name} fa-{text}"></span>', format="html")], []


def register():
    roles.register_local_role("fas", rst_span)
    roles.register_local_role("far", rst_span)
    roles.register_local_role("fab", rst_span)
