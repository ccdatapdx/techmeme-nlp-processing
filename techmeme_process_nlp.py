import pandas as pd
import spacy

class SpacyProcessing:

    def __init__(self) -> None:
        self.nlp = spacy.load('en_core_web_lg')
        self.list_df_rows = []

    def df_by_row(self,df:pd.DataFrame):
        df_row = pd.DataFrame()
        for row in df.index:
            df_row = df.iloc[[row]]
            self.list_df_rows.append(df_row)
        return self.list_df_rows    
    
    def to_ner(self,data_headlines:pd.Series):
        list_ner_headlines = []
        list_ner_types = []
        ner_headlines = self.nlp(''.join(data_headlines))
        for ent in ner_headlines.ents:
            list_ner_headlines.append(ent.text)
            list_ner_types.append(ent.label_)
        data = {'ner_headlines':list_ner_headlines,'ner_type':list_ner_types}
        data = pd.DataFrame(data)
        return data
    
    def process_headlines_nlp(self,df_rows:list[pd.DataFrame]):
        list_df_headlines = []
        for row in df_rows:
            headline_ner = self.to_ner(row['headline'])
            headline_ner = row.merge(headline_ner,how='cross')
            list_df_headlines.append(headline_ner)
        df_headlines = pd.concat(list_df_headlines).reset_index(drop=True)
        df_headlines['news_date'] = pd.to_datetime(df_headlines['news_date'])
        return df_headlines


        