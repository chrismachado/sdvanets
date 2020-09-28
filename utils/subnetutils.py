class SubnetUtils:

    def __init__(self, **kwargs):
        try:
            if 'netmask' not in kwargs:
                raise ValueError('Netmask not specified')
            if type(kwargs['netmask']) is not int:
                raise TypeError('Netmask should be integer current type %s' % type(kwargs['netmask']))

            self.netmask = kwargs.pop('netmask')

        finally:
            pass

    def int_to_dotted_string(self):
        binary = bin(self.netmask).split('0b')[1]
        aux = ''
        result = ''
        for i in range(len(binary)):
            if i == 8 or i == 16 or i == 24 or i == 31:
                result += str(int(aux, 2))
                if i != 31:
                    result += '.'
                aux = binary[i]
            else:
                aux += binary[i]
        return result
