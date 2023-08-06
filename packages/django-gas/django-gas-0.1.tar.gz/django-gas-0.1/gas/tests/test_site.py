from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.urls import reverse

from gas.sites import GASSite, site


class SiteTestCase(TestCase):
    def test_register_role(self):
        test_site = GASSite()

        # new role registered without error
        test_site.register_role('test', 'test role')

        # another new role registered without error
        test_site.register_role('test2', 'another test role')

        # repeated role raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_role('test', 'repeated test role')

    def test_register_urls(self):
        test_site = GASSite()

        # new prefix registered without error
        test_site.register_urls('test_prefix', 'gas.gas.urls')

        # another new prefix registered without error
        test_site.register_urls('test_prefix2', 'gas.gas.urls')

        # repeated prefix raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_urls('test_prefix', 'gas.gas.urls')

    def test_register_menu(self):
        test_site = GASSite()
        test_site.register_role('test_admins', 'test administrators')

        # Menu entry with non existent parent raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_menu(
                parent='nonexistent',
                name='test_roles',
                label="Roles",
                icon="",
                url="gas:role_list",
                roles=('test_admins',),
            )

        # new entry without parent without error
        test_site.register_menu(
            name='sample_app',
            label="Sample app",
            icon="",
            url=None,
            roles=('test_admins',),
        )

        # new entry with known parent without error
        test_site.register_menu(
            parent='sample_app',
            name='test_roles',
            label="Roles",
            icon="",
            url="gas:role_list",
            roles=('test_admins',),
        )
        # new entry with duplicated name raises error
        with self.assertRaises(ImproperlyConfigured):
            test_site.register_menu(
                name='sample_app',
                label="Sample app 2",
                icon="",
                url=None,
                roles=('test_admins',),
            )

        # new entry with no role
        test_site.register_menu(
            parent='sample_app',
            name='no_roles',
            label="No Roles",
            icon="",
            url="gas:role_list",
        )


class SampleAppIntegrationTest(TestCase):
    def test_gas_autodiscover(self):
        # urls registered
        reverse('gas:user_list')

        # menu registered
        self.assertIn(
            'users',
            site._registry['menu'],
        )

        # role registered
        self.assertIn(
            'admins',
            site._registry['roles'],
        )
