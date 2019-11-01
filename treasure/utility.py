

class ConversionTableResolver:
    @staticmethod
    def createTable(difficulty_pk):
        conversionTable = ConversionTable()
        for i in range(0b1_0000_0000):
            conversionTable.data.append(
                {
                    'binary': format(i, '08b'),
                    'to_base': (
                        format(i, '08d') if difficulty_pk == 2
                        else format(i, '08x')
                    )
                }
            )
        return conversionTable


class ConversionTable:
    def __init__(self):
        self.data = []
