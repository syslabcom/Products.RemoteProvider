from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class RemoteProvider(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.ATVocabularyManager
        self.loadZCML('configure.zcml', package=Products.ATVocabularyManager)
        import Products.RemoteProvider
        self.loadZCML('configure.zcml', package=Products.RemoteProvider)

        z2.installProduct(app, 'Products.ATVocabularyManager')
        z2.installProduct(app, 'Products.RemoteProvider')

    def setUpPloneSite(self, portal):
        # Needed to make skins work
        applyProfile(portal, 'Products.CMFPlone:plone')

        applyProfile(portal, 'Products.ATVocabularyManager:default')
        applyProfile(portal, 'Products.RemoteProvider:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.ATVocabularyManager')
        z2.uninstallProduct(app, 'Products.RemoteProvider')


REMOTEPROVIDER_FIXTURE = RemoteProvider()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(REMOTEPROVIDER_FIXTURE,),
    name="RemoteProvider:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REMOTEPROVIDER_FIXTURE,),
    name="RemoteProvider:Functional")
