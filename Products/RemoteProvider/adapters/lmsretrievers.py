"""CMF link checker tool - link retriever functions"""

import Products.RemoteProvider.content.Provider
try:
    from gocept.linkchecker.interfaces import IRetriever
    import gocept.linkchecker.utils
except ImportError:
    from zope.interface import Interface
    class IRetriever(Interface):
        """ empty marker interface """
import zope.component
import zope.interface


class RemoteProviderRetriever(object):
    """Retriever for RemoteProvider objects"""

    zope.component.adapts(Products.RemoteProvider.content.Provider.Provider)
    zope.interface.implements(IRetriever)

    def __init__(self, context):
        self.context = context

    def retrieveLinks(self):
        """Finds all links from the object and return them."""
        links = []
        if self.context.getRemoteUrl():
            links.append(self.context.getRemoteUrl())
        for link in gocept.linkchecker.utils.retrieveAllRichTextFields(
                self.context):
            links.append(link)
        return links

    def updateLink(self, oldurl, newurl):
        """Replace all occurances of <oldurl> on object with <newurl>."""
        if self.context.getRemoteUrl() == oldurl:
            self.context.setRemoteUrl(newurl)
        gocept.linkchecker.utils.updateAllRichTextFields(
            oldurl, newurl, self.context)

