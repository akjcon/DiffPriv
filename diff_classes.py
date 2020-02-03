import sys
import io




class ColumnType:
    ''' provides a container for each type of data (bool, int, and string)
        with methods to edit/change them '''

    def __init__(self,type,data):
        ''' creates a column instance with a type and a list '''
        self.type = type
        self.column = data

    def __repr__(self):
        return self.column

    def add_row(self,data):
        self.column.append(data)

    def __delitem__(self,index):
        del self.column[index]

    def __getitem__(self,index):
        return self.column[index]

    def __setitem__(self,index,item):
        self.column[index] = item 

    def len(self):
        return len(self.column)

class Database:

    def __init__(self,type,columns):
        # type can be either std or diff
        self.type = type
        self.db = columns

    def add_row(self,column):
        #column must be of type ColumnType
        self.db.append(column)

    def __delitem__(self,index):
        del self.db[index]

    def __getitem__(self,index):
        return self.db[index]

    def __setitem__(self,index,item):
        self.db[index] = item

    def len(self):
        return len(self.db)
