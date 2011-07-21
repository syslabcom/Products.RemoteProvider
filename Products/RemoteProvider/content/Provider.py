# -*- coding: utf-8 -*-
#
# File: Provider.py
#
# Copyright (c) 2008 by [syslab.com]
#
# GNU General Public License (GPL)
#

__author__ = """Syslab.com GmbH <info@syslab.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.RemoteProvider.config import *

from Products.Archetypes.utils import DisplayList
from Products.RemoteProvider.config import *
from Products.ATCountryWidget.Widget import CountryWidget, MultiCountryWidget
from Products.CMFCore.utils import getToolByName

from zope.i18n import translate

from Products.RemoteProvider import RemoteProviderMessageFactory as _

schema = Schema((

    StringField(
        name='title',
        required=True,
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_title_label', default=u"Title"),
            description=_(u'remoteprovider_title_description', default=u"The Title of the Organisation as it should show up in the search results."),
        ),
        accessor="Title",
        searchable=True,
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label=_(u'remoteprovider_description_label', default=u"Description"),
            description=_(u'remoteprovider_description_description', default=u"A short descriptive text which describes this provider."),
            rows=5,
        ),
        schemata="default",
        validators=("python:('isTidyHtmlWithCleanup'", ')', ''),
        default_output_type='text/x-html-safe',
        accessor="Description",
        searchable=True,
    ),
    StringField(
        name='remoteUrl',
        required=True,
        widget=StringField._properties['widget'](
            macro="urlwidget",
            label=_(u'remoteprovider_remoteUrl_label', default=u"Web Address (URL)"),
            description=_(u'remoteprovider_remoteUrl_description', default=u"The web address where you can reach the providers homepage."),
        ),
        searchable=True,
    ),
    StringField(
        name='providerCategory',
        languageIndependent=True,
        widget=SelectionWidget(
            label=_(u'remoteprovider_providerCategory_label', default=u"Provider Category"),
            description=_(u'remoteprovider_providerCategory_description', default=u"Specify the category this provider belongs to"),
            condition="python:len(object.getAvailableCategories())",
        ),
        required=True,
        default='nocat',
        accessor="getProvider_category",
        vocabulary="getAvailableCategories",
    ),
    StringField(
        name='contact_name',
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_contact_name_label', default=u"Contact Name"),
            description=_(u'remoteprovider_contact_name_description', default=u"The name of the person which people can contact."),
        ),
        schemata="Contact",
    ),
    LinesField(
        name='address',
        schemata="Contact",
        widget=LinesWidget(
            rows=5,
            cols=50,
            label=_(u'remoteprovider_address_label', default=u"Address"),
            description=_(u'remoteprovider_address_description', default=u"The contact persons postal address."),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
    ),
    StringField(
        name='phone',
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_phone_label', default=u"Phone"),
            description=_(u'remoteprovider_phone_description', default=u"The contact persons phone number."),
        ),
        schemata="Contact",
    ),
    StringField(
        name='fax',
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_fax_label', default=u"Fax"),
            description=_(u'remoteprovider_fax_description', default=u"The contact persons fax number."),
        ),
        schemata="Contact",
    ),
    StringField(
        name='email',
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_email_label', default=u"Contact Email"),
            description=_(u'remoteprovider_email_description', default=u"Contact this address for further information"),
            macro="emailwidget",
        ),
        schemata="Contact",
    ),
    StringField(
        name='contact_url',
        widget=StringField._properties['widget'](
            label=_(u'remoteprovider_contact_url_label', default=u"Contact Url"),
            description=_(u'remoteprovider_contact_url_description', default=u"This URL can be used for contacting the provider."),
            macro="urlwidget",
        ),
        schemata="Contact",
    ),
    LinesField(
        name='remoteLanguage',
        widget=MultiSelectionWidget(
            label=_(u'remoteprovider_remoteLanguage_label', u"Remote Language"),
            description=_(u'remoteprovider_remoteLanguage_description', default=u"The language of the linked contents"),
            rows=5,
        ),
        enforceVocabulary=True,
        schemata="Other",
        multiValued=True,
        vocabulary='getFilteredLanguages',
    ),

),
)


Provider_schema = BaseSchema.copy() + \
    schema.copy()


class Provider(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IProvider)

    meta_type = 'Provider'
    _at_rename_after_creation = True

    schema = Provider_schema


    security.declarePublic('getAvailableCountries')
    def getAvailableCountries(self):
        """
        """
        dl = DisplayList()
        for k,v in AVAILABLE_COUNTRIES:
            dl.add(k,v)
        return dl

    security.declarePublic('getAvailableCategories')
    def getAvailableCategories(self):
        """
        """
        pv = getToolByName(self, 'portal_vocabularies')
        VOCAB = pv.get('provider_category')
        if VOCAB:
            dl = VOCAB.getDisplayList(self)
        else:
            dl = DisplayList()
            dl.add('nocat', 'No specific category')
        return dl

    security.declarePublic('getProvider_categoryName')
    def getProvider_categoryName(self):
        """
        """
        pv = getToolByName(self, 'portal_vocabularies')
        VOCAB = pv.get('provider_category')
        category = self.getProvider_category()
        name = VOCAB.get(category)
        return name and name.title or category

    def getFilteredLanguages(self):
        """ return the languages supported in the site """
        plt = getToolByName(self, 'portal_languages')
        langs = plt.listSupportedLanguages()
        L = []
        for l in langs:
            L.append((l[0], translate(l[1]) ))
        L.sort()
        return DisplayList(L)

    security.declarePublic('getProviderDefault')
    def getProviderDefault(self):
        """ tries to find a default value from the site settings
        """
        portal_url = getToolByName(self, 'portal_url')
        portal = portal_url.getPortalObject()
        provider = portal.getProperty('provider', None) or \
                    portal.portal_properties.site_properties.getProperty('provider', None) or \
                    DEFAULT_PROVIDER
        return provider



registerType(Provider, PROJECTNAME)
# end of class Provider




