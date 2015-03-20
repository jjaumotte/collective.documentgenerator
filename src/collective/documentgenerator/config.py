# -*- coding: utf-8 -*-

from collective.documentgenerator.content.pod_template import ConfigurablePODTemplate
from collective.documentgenerator.content.pod_template import PODTemplate
from collective.documentgenerator.content.pod_template import SubTemplate
from collective.documentgenerator.content.style_template import StyleTemplate

from plone import api


POD_TEMPLATE_TYPES = [
    PODTemplate.__name__,
    ConfigurablePODTemplate.__name__,
    SubTemplate.__name__,
    StyleTemplate.__name__,
]

POD_TEMPLATE_TYPES


def get_uno_path():
    return api.portal.get_registry_record(
        "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.uno_path"
    )


def get_oo_port():
    return api.portal.get_registry_record(
        "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.oo_port"
    )