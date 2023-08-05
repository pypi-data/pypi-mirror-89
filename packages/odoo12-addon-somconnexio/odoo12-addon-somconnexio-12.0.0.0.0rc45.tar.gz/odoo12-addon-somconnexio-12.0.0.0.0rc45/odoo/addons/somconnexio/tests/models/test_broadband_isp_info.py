from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class BroadbandISPInfoTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.broadband_isp_info_args = {
            'service_address': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'delivery_address': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'type': 'new'
        }

    def test_new_creation_ok(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()
        broadband_isp_info = self.env['broadband.isp.info'].create(
            broadband_isp_info_args_copy
        )
        self.assertTrue(broadband_isp_info.id)

    def test_portability_creation_ok(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        broadband_isp_info = self.env['broadband.isp.info'].create(
            broadband_isp_info_args_copy
        )
        self.assertTrue(broadband_isp_info.id)

    def test_portability_without_previous_provider(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': None,
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_owner_vat_number(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_owner_name(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': '',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_first_name(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': '',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_phone_number(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_service(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )
