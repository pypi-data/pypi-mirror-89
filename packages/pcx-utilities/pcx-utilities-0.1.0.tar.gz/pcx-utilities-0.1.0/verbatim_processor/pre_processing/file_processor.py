from os import rename
from pandas.io.parsers import ParserBase
from ..enrichment.sentencizer import CustomSentencizer
from ..kairntech import Annotator, KairntechClient
import pandas as pd
import numpy as np
import uuid
import json
from typing import Any, Callable, Dict, List, Union
from .meta_column import MetaColumn
from ..processors import processors
from ..pipeline.task import Task
from pathlib import Path
from datetime import datetime


class FileFormater(Task):

    def __init__(self,
                name,
                 verbatim_column:str,
                 date_column:str,
                 id_column:str,
                 meta_columns:List[MetaColumn],
                 drop_empty_verbatim:bool=True,
                 encoding:str='utf-8',
                 generate_id=False, 
                 csv_separator=","):
        super().__init__(name)
        self.verbatim_column = verbatim_column
        self.date_column = date_column
        self.id_column = id_column
        self.meta_columns = meta_columns
        self.drop_empty_verbatim = drop_empty_verbatim
        self.encoding = encoding
        self.generate_id = generate_id
        self.csv_separator = csv_separator
        self.output_extension = ".json"

    def __rename_columns(self, original_columns):
        columns = []
        for c in original_columns:
            if c==self.id_column:
                columns.append("id")
            if c==self.date_column:
                columns.append("dateInterview")
            if c==self.verbatim_column:
                columns.append("text")
            elif c in [m.column_name for m in self.meta_columns]:
                meta_column = list(filter(lambda x: x.column_name==c,self.meta_columns))[0]
                if meta_column.rename_column:
                    columns.append(meta_column.new_column_name)
                else:
                    columns.append(meta_column.column_name)
        return columns
        
    def __generate_id(self):
        return str(uuid.uuid4())

    @property
    def __columns_to_keep(self):
        return [self.id_column, self.date_column, self.verbatim_column] + [m.column_name for m in self.meta_columns]


    def __get_dataframe_from_path(self,filepath:Path)->pd.DataFrame:
        if filepath.suffix == ".xlsx":
            data = pd.read_excel(filepath, parse_dates=[self.date_column], encoding=self.encoding)
        elif filepath.suffix== ".csv":
            data = pd.read_csv(filepath, parse_dates=[self.date_column], encoding=self.encoding, sep=self.csv_separator)
        else :
            raise Exception("only csv and xlsx format are supported. Extension is " + filepath.suffix)
        if self.generate_id:
            data[self.id_column] = data[data.columns[0]].apply(lambda x: self.__generate_id())
        return data

    def __list_of_filters(self):
        meta_columns = [m.new_column_name if m.rename_column else m.column_name for m in self.meta_columns]
        return meta_columns

    def __format_pcx(self, data):
        formatted_data = []
        filters = self.__list_of_filters()
        for row in data:
            formatted_row = {
                "id": row["id"],
                "dateInterview": row["dateInterview"].strftime("%Y-%m-%d %H:%M:%S"),
                "text": row["text"],
                "data": {f:row[f] for f in filters}
            }
            formatted_data.append(formatted_row)
        return formatted_data
            

    def run(self, *input)->str:
        """
        Format the given file to json format
        """
        data = self.__get_dataframe_from_path(input[0])
        # keep only the good columns
        data = data[self.__columns_to_keep]
        # drop empty verbatim if needed
        if self.drop_empty_verbatim:
            data[self.verbatim_column].replace('', np.nan,inplace=True)
            data.dropna(subset=[self.verbatim_column],inplace=True)
        # fill na if needed
        for meta in self.meta_columns:
            if meta.fill_na:
                data[meta.column_name].fillna(meta.na_filler)
        # rename columns if needed
        data.columns = self.__rename_columns(data.columns)
        pcx_formatted_data = self.__format_pcx(data.to_dict(orient="records"))
        return json.dumps(pcx_formatted_data)
