# -*- coding: utf-8 -*-
"""Define tables and columns."""

from Products.CMFPlone import PloneMessageFactory as PMF
from Products.CMFPlone.utils import safe_unicode, normalizeString
from collective.documentgenerator import _
from plone import api
from z3c.table.column import Column, LinkColumn
from z3c.table.table import Table
from zope.cachedescriptors.property import CachedProperty
from zope.i18n import translate


class TemplatesTable(Table):

    """Table that displays templates info."""

    cssClassEven = u'even'
    cssClassOdd = u'odd'
    cssClasses = {'table': 'listing templates-listing'}

    batchSize = 30
    startBatchingAt = 35
    sortOn = None
    results = []

    def __init__(self, context, request):
        super(TemplatesTable, self).__init__(context, request)
        self.context_path_len = len(self.context.absolute_url_path())
        self.paths = {'': '-'}

    @CachedProperty
    def translation_service(self):
        return api.portal.get_tool('translation_service')

    @CachedProperty
    def wtool(self):
        return api.portal.get_tool('portal_workflow')

    @CachedProperty
    def portal_url(self):
        return api.portal.get().absolute_url()

    @CachedProperty
    def values(self):
        return self.results


class TitleColumn(LinkColumn):

    """Column that displays title."""

    header = PMF("Title")
    weight = 10

    def getLinkCSS(self, item):
        return ' class="state-%s icons-on contenttype-%s"' % (api.content.get_state(obj=item),
                                                              normalizeString(item.portal_type))

    def getLinkContent(self, item):
        return safe_unicode(item.title)


class PathColumn(Column):

    """Column that displays path."""

    header = _("Path")
    weight = 20

    def renderCell(self, value):
        path = value.absolute_url_path()[self.table.context_path_len:-(len(value.id)) - 1]
        if path not in self.table.paths:
            parent_path = '/'.join(path.split('/')[:-1])
            if parent_path:
                self.table.paths[path] = '%s / %s' % (self.table.paths[parent_path], value.__parent__.title)
            else:
                self.table.paths[path] = value.__parent__.title
        return self.table.paths[path]


class ReviewStateColumn(Column):

    """Column that displays review state."""

    header = PMF("Review state")
    weight = 60

    def renderCell(self, value):
        state = api.content.get_state(value)
        if state:
            state_title = self.table.wtool.getTitleForStateOnType(state, value.portal_type)
            return translate(PMF(state_title), context=self.request)
        return ''