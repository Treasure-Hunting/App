from django.test import TestCase

from app.utility import ConversionTableResolver


class UtilityTest(TestCase):
    def setUp(self):
        pass

    def test_conversion_table(self):
        table_data = ConversionTableResolver.createTable(2).data

        # 変換表(10進)が表示されているか
        self.assertIn(
            {
                'binary': '00000000',
                'to_base': '00000000'
            },
            table_data
        )

        self.assertIn(
            {
                'binary': '11111111',
                'to_base': '00000255'
            },
            table_data
        )

        table_data = ConversionTableResolver.createTable(3).data

        # 変換表(16進)が表示されているか
        self.assertIn(
            {
                'binary': '00000000',
                'to_base': '00000000'
            },
            table_data
        )

        self.assertIn(
            {
                'binary': '11111111',
                'to_base': '000000ff'
            },
            table_data
        )
