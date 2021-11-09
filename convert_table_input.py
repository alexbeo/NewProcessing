import pandas as pd

PATH_TO_SAVE = r'C:\Users\Александр Козлов\Desktop\PYTHON_EDUCATION\Processing\input_reports\TAGs_Processing\InterReport\reference_books.xlsx'


def read_file(filename):
    df = pd.read_excel(filename, sheet_name='Основной', skiprows=1,  engine='openpyxl')
    return df


def convert_file(df):
    df1 = pd.DataFrame()
    df1['OBU'] = df['№ Тага по Ш/К']
    df1['ActivationPoint'] = df['Кому передан']
    df1['ActivationData'] = pd.to_datetime(df['дата выдачи']).dt.date
    df1['ExpirationDate'] = '01/01/2020'
    df1['NumberOfContract'] = df['№ Договора']
    df1['CustomerName'] = df['Название клиента']
    df1['CardNumber'] = df['№ Карты (для ДКВ)']
    df1['CarNumber'] = df['№ Авто']
    df1['CarСategory'] = df['Категория']

    df1.loc[df1['ActivationPoint'] == '0. Офис', 'ActivationPoint'] = 'OfficeBG'
    df1.loc[df1['ActivationPoint'] == '1. Градина П/Т', 'ActivationPoint'] = 'Gradina'
    df1.loc[df1['ActivationPoint'] == '2.Хоргош П/Т', 'ActivationPoint'] = 'Horgosh'
    df1.loc[df1['ActivationPoint'] == '3. Батровцы П/Т', 'ActivationPoint'] = 'Batrovci'
    df1.loc[df1['ActivationPoint'] == '4. Прешево П/Т', 'ActivationPoint'] = 'Presovo'
    df1.loc[df1['ActivationPoint'] == '5. Келебия П/Т', 'ActivationPoint'] = 'Kelebija'
    df1.loc[df1['ActivationPoint'] == 'Возврат/Брак', 'ActivationPoint'] = 'Return'

    df1.loc[df1['CustomerName'] == '0_Автолайн', 'CustomerName'] = 'Autoline'
    df1.loc[df1['CustomerName'] == '0_ЮГОЕКСИМ', 'CustomerName'] = 'Jugoexsim'
    df1.loc[df1['CustomerName'] == '0_KEMIS d.o.o.', 'CustomerName'] = 'Kemis'
    df1.loc[df1['CustomerName'] == '0_NIGOS-El', 'CustomerName'] = 'Nigos'


    df1.to_excel(PATH_TO_SAVE, index=False)


if __name__ == '__main__':
    df = read_file(r'C:\Users\Александр Козлов\Desktop\PYTHON_EDUCATION\NewProcessing\ТАГИ 2021_11_08.xlsx')
    print(df.info())
    convert_file(df)
