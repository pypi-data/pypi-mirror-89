from pandalchemy.pandalchemy_utils import list_of_tables, primary_key, get_col_types, to_sql_k
from pandalchemy.pandalchemy_utils import from_sql_keyindex, to_sql_indexkey, copy_table
from pandalchemy.magration_functions import to_sql
from pandalchemy.interfaces import IDataBase, ITable

from pandas import read_sql_table, DataFrame
from sqlalchemy.engine.base import Engine


class DataBase(IDataBase):
    """Holds the different database tables as DataFrames
       Needs to connect to a database to push changes
       push method changes database with sql
    """
    def __init__(self, engine):
        self.engine = engine
        self.db = {name: Table(name,
                               engine=engine,
                               db=self
                               )
                   for name in engine.table_names()
                   }

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value

    def __len__(self):
        return len(self.db)

    @property
    def table_names(self):
        return self.db.keys()

    def __repr__(self):
        return f'DataBase({", ".join(repr(tbl) for tbl in self.db.values())})'

    def push(self):
        # Push each table to the database
        for tbl in self.db.values():
            tbl.push(self.engine)
        self.__init__(self.engine)

    def pull(self):
        # updates DataBase object with current database data
        self.__init__(self.engine)

    # TODO add_table method
    # TODO drop_table method
    def add_table(self, table):
        self.db[table.name] = table
        table.db = self
        table.engine = self.engine


class Table(ITable):
    """Pandas DataFrame used to change database tables
    """
    def __init__(self, name, data=None, key=None, f_keys=[], types=dict(), engine=None, db=None):
        self.name = name
        self.key = key
        self.f_keys = f_keys
        self.types = types
        self.engine = engine
        self.data = data
        self.db = db

        if isinstance(self.data, Engine):
            self.engine = self.data
            self.data = None
        
        if isinstance(self.engine, Engine):
            # If engine provided and no key: set key to existing table key
            if self.key is None:
                if self.name in self.engine.table_names():
                    self.key = primary_key(self.name, self.engine)
            else:
                pass # 
            # If engine and data provided: 
            if self.data is not None:
                pass # table probably doesn't already exist?
            else:
                # pull data down from table
                self.data = from_sql_keyindex(self.name,
                                              self.engine
                                              )
        # If no engine provided but data is:
        elif self.data is not None:
            
            if isinstance(self.data, dict):
                self.data = DataFrame(data)

            if isinstance(self.data, DataFrame):
                self.key = self.data.index.name
            else:
                raise TypeError('data can only be DataFrame or dict')


    def __repr__(self):
        return f"""Table(name={self.name}, key={self.key},
        {repr(self.data)})"""

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        if type(key) == int:
            self.data.iloc[key] = value
        else:
            self.data[key] = value

    def push(self, engine=None):
        if engine is not None:
            self.engine = engine

        if self.name in self.engine.table_names():
            to_sql(self.data,
                   self.name,
                   self.engine,
                   )
        else:
            self.key = self.data.index.name
            if self.key is None:
                to_sql_k(self.data, self.name, engine, keys='index')
            else:
                to_sql_k(self.data, self.name, engine, keys=self.key)

        self.__init__(self.name, engine=self.engine)
            
    @property
    def column_names(self):
        return self.data.columns

    def __getitem__(self, key):
        if type(key) == int:
            return self.data.iloc[key]
        else:
            return self.data[key]

    def drop(self, *args, **kwargs):
        self.data.drop(*args, **kwargs)

    # TODO: add/delete primary key
    # TODO: add/delete foreign key

    def copy_push(self, new_name, new_engine=None):
        if new_engine is None:
            new_engine = self.engine
        copy_table(self.engine, self.name, new_name, new_engine)

    def copy(self, new_name):
        self.copy_push(new_name)
        return Table(new_name, engine=self.engine)


if __name__ == '__main__':
    import pandas as pd
    import sqlalchemy as sa
    engine = sa.create_engine('sqlite:///tests/table_test.db')
    df = pd.DataFrame({'name':['Josh', 'Odos', 'Alec', 'Olivia', 'Max'], 'id':[1, 2, 3, 4, 5]})
    to_sql_k(df, 'people', engine, index=False, if_exists='replace', keys='id')
    tbl = Table('people', engine)
    tbl['name'] = [x+'_' for x in tbl['name']]
    tbl.push()
    print(Table('people', engine=engine))