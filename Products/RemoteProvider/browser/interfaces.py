from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer."""


class IVocabularyHelper(Interface):
    """Interface that holds verious methods for working with vocaularies"""

    def getDisplayListFor(vocabularyName=''):
        """ Return DisplayList for given vocabulary"""

    def getSubjectList():
        """Return a display list of Subject entries"""
