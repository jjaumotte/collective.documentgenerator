from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.documentgenerator.content.pod_template import IPODTemplate

from plone import api
from plone.app.layout.viewlets import ViewletBase


class DocumentGeneratorLinksViewlet(ViewletBase):
    """This viewlet displays available documents to generate."""

    render = ViewPageTemplateFile('./generationlinks.pt')

    def available(self):
        return True

    def get_all_pod_templates(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(object_provides=IPODTemplate.__identifier__)
        pod_templates = [brain.getObject() for brain in brains]

        return pod_templates

    def get_generable_templates(self):
        pod_templates = self.get_all_pod_templates()
        generable_templates = [pt for pt in pod_templates if pt.can_be_generated(self.context)]

        return generable_templates

    def get_links_info(self):
        base_url = self.context.absolute_url()
        generable_templates = self.get_generable_templates()
        links = []
        for template in generable_templates:
            title = template.Title()
            uid = template.UID()
            link = '{base_url}/document-generation?doc_uid={uid}'.format(
                base_url=base_url,
                uid=uid,
            )
            links.append({'link': link, 'title': title})
        return links
