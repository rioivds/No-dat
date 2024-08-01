class Common:
    @staticmethod
    def parse_fecha(fecha_str):
        if fecha_str is None:
            return None

        meses = {
            'enero': '01',
            'febrero': '02',
            'marzo': '03',
            'abril': '04',
            'mayo': '05',
            'junio': '06',
            'julio': '07',
            'agosto': '08',
            'septiembre': '09',
            'octubre': '10',
            'noviembre': '11',
            'diciembre': '12'
        }

        partes = fecha_str.split(' ')
        dia = partes[0]
        mes = meses[partes[2]]
        anio = partes[4]

        return f'{anio}-{mes}-{dia}'

    @staticmethod
    def email_check(email):
        email = email.split('@')
        return email[0] == 'escuelasproa.edu.ar'
