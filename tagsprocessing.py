import pandas as pd


class TAG():
    tagID = ''
    poinID = ''
    activationDate = ''
    expiriedDate = ''
    contractNumber = ''
    parnerID = ''
    cardNumber = ''
    carNumber = ''
    carCategory = ''
    blockStatus = ''



class PayCard():
    def __init__(self,  cardNumber = '', cardStatus = True):
        self.cardNumber = cardNumber
        self.cardStatus = cardStatus


class DfTags():

    def __init__(self, filename, sheetname=''):
        self.filename = filename
        self.sheetname = sheetname
        self.df = self._read_df_from_file()
        self._set_df_col()

    def _read_df_from_file(self):
        df = pd.read_excel(self.filename, sheet_name= self.sheetname, parse_dates=['ActivationData'])
        return df

    def _set_df_col(self):
        self.df_obu = self.df['OBU']
        self.df_act_point=self.df['ActivationPoint']
        self.df_act_date=self.df['ActivationData']
        self.df_num_contract=self.df['NumberOfContract']
        self.df_customer=self.df['CustomerName']
        self.df_card_number = self.df['CardNumber']
        self.df_car_number = self.df['CarNumber']
        self.df_category = self.df['CarСategory']

    def __getitem__(self, item):
        return self.df.iloc[item]


class DfTags1(DfTags):

    def _set_df_col(self):
        pass
    def _read_df_from_file(self):
        df = pd.read_excel(self.filename, engine='pyxlsb')
        return df


def remove_trash(df, indexlist):
    for indexname in indexlist:
        df = df.drop(['indexname'], axis=1)
    return df

def get_turkish_car(complex_tags, country = 'Турция'):
    pass


if __name__ == '__main__':
    import os
    import datetime
    tags_jex = DfTags('reference_books_1.xlsx','Sheet1' )
    tags_utd = DfTags1('OBUList_20200623_093024.xlsb')

    comlex_tags = pd.merge(tags_jex.df, tags_utd.df, how='inner', on = 'OBU')

    comlex_tags = comlex_tags.drop(['Activated'], axis=1)
    comlex_tags = comlex_tags.drop(['Expired'], axis=1)
    comlex_tags = comlex_tags.drop(['State'], axis=1)
    comlex_tags = comlex_tags.drop(['StateChanged'], axis=1)
    comlex_tags = comlex_tags.drop(['BlockState'], axis=1)
    comlex_tags = comlex_tags.drop(['BlockStateChanged'], axis=1)
    comlex_tags = comlex_tags.drop(['CardIssuer'], axis=1)
    comlex_tags = comlex_tags.drop(['PAN'], axis=1)
    comlex_tags = comlex_tags.drop(['PANHash'], axis=1)
    comlex_tags = comlex_tags.drop(['CardExpired'], axis=1)
    comlex_tags = comlex_tags.drop(['Category'], axis=1)
    comlex_tags = comlex_tags.drop(['VRN'], axis=1)
    comlex_tags = comlex_tags.drop(['BrojUgovora'], axis=1)
    comlex_tags = comlex_tags.drop(['CID'], axis=1)
    comlex_tags = comlex_tags.drop(['Merchant'], axis=1)
    comlex_tags = comlex_tags.drop(['OBUBlocked'], axis=1)
    comlex_tags = comlex_tags.drop(['Unnamed: 19'], axis=1)


    mask_tr_carnumber = ((comlex_tags['CarNumber'].str.contains("^[0-9]{2}[A-Z]{1}[0-9A-Z]{2}[0-9]{2,3}$",regex= True, na=False)))
    comlex_tags.loc[mask_tr_carnumber, 'Страна'] = 'Турция'

    mask_bl_carnumber = ((comlex_tags['CarNumber'].str.contains("^[A-Z]{1}[0-9A-Z]{1}[0-9]{3}[0-9A-Z]{1}([A-Z]{0,2})?$",regex= True, na=False))
                         &
                         (
                         (comlex_tags['CarNumber'].str.startswith('BH'))|
                         (comlex_tags['CarNumber'].str.startswith('BP'))|
                         (comlex_tags['CarNumber'].str.startswith('BT'))|
                         (comlex_tags['CarNumber'].str.startswith('EB'))|
                          (comlex_tags['CarNumber'].str.startswith('EH')) |
                          (comlex_tags['CarNumber'].str.startswith('KH')) |
                          (comlex_tags['CarNumber'].str.startswith('OB')) |
                          (comlex_tags['CarNumber'].str.startswith('PA')) |
                          (comlex_tags['CarNumber'].str.startswith('PB')) |
                          (comlex_tags['CarNumber'].str.startswith('PK')) |
                          (comlex_tags['CarNumber'].str.startswith('PP')) |
                          (comlex_tags['CarNumber'].str.startswith('CA')) |
                          (comlex_tags['CarNumber'].str.startswith('CB')) |
                          (comlex_tags['CarNumber'].str.startswith('CM')) |
                          (comlex_tags['CarNumber'].str.startswith('CH')) |
                          (comlex_tags['CarNumber'].str.startswith('CO')) |
                          (comlex_tags['CarNumber'].str.startswith('CC')) |
                          (comlex_tags['CarNumber'].str.startswith('CT')) |
                          (comlex_tags['CarNumber'].str.startswith('TX')) |
                          (comlex_tags['CarNumber'].str.startswith('Y')) |
                          (comlex_tags['CarNumber'].str.startswith('X'))

                          ))


    comlex_tags.loc[mask_bl_carnumber, 'Страна'] = 'Болгария'

    comlex_tags['ActivationData'] = pd.to_datetime(comlex_tags['ActivationData'].dt.strftime('%Y-%m-%d'))
    comlex_tags = comlex_tags.set_index(['ActivationData'])

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    firstday = datetime.datetime.today().replace(day=1).strftime("%Y-%m-%d")
    comlex_tagsD = comlex_tags.loc[firstday : today]
    comlex_tagsD = comlex_tagsD.reset_index()
    print(comlex_tagsD.info())
    df_pivotD = pd.pivot_table(comlex_tagsD, index = ['ActivationPoint'],
                              values=['OBU'],
                              columns= pd.Grouper(key='ActivationData', freq='D'),
                               aggfunc='count')

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    firstday = datetime.date(year,1,1).strftime("%Y-%m")
    comlex_tagsM = comlex_tags.loc[firstday: today]
    comlex_tagsM = comlex_tagsM.reset_index()
    comlex_tagsM = comlex_tagsM[comlex_tagsM.ActivationPoint != 'Return']
    df_pivotM = pd.pivot_table(comlex_tagsM, index = ['ActivationPoint'],
                              values=['OBU'],
                              columns= pd.Grouper(key='ActivationData', freq='M'),
                               aggfunc='count')

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    year = datetime.datetime.now().year
    firstday = datetime.date(year,1,1).strftime("%Y-%m")
    comlex_tagsY = comlex_tags.loc[: today]
    comlex_tagsY = comlex_tagsY.reset_index()
    comlex_tagsY = comlex_tagsY[comlex_tagsY.ActivationPoint != 'Return']
    df_pivotY = pd.pivot_table(comlex_tagsY, index = ['ActivationPoint'],
                              values=['OBU'],
                              columns= pd.Grouper(key='ActivationData', freq='Y'),
                               aggfunc='count')


    df_pivotD.to_excel('1111.xlsx')

    os.startfile('1111.xlsx')






