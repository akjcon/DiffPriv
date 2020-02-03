# Differential Privacy: A Short Study

### Introduction

Differential Privacy is is a concept that, when applied correctly, can allow user data to be analyzed and computed upon without compromising any privacy. This is especially important with sensitive data such as medical records or income statements, which can be valuable data to researchers, but requires strict privacy guarantees before it can be used.
[expand this]

##### A simple example:

Differential Privacy can be achieved relatively easily in simple data with a concept called *randomized response*. This works by creating a user response that has a *p* probability of being a random response, and a *1-p* probability of being a true response. For example, if the creator of a particular system deployed a new feature, they might want to collect data from each user to see at what frequency they used the new feature. However, this would effectively create a database that links this information to each user. "What about anonymizing the database?" you might say. "Wouldn't that be a much easier way to keep the data private?" Unfortunately, the identifying information in databases like this is quite literally the information we are trying to anonymize.

>  A vast majority of records in a database of size n can be reconstructed when n log(n)2 queries are answered by a statistical database ... even if each answer has been arbitrarily altered to have up to o(√n) error ([Sigmod 2017, Machanavajjhala et al](http://sigmod2017.org/wp-content/uploads/2017/03/04-Differential-Privacy-in-the-wild-1.pdf)).

To fix this problem, we can employ our randomized response technique so that even if an attacker were able to deanonymize our database, they would not know whether the data attached to each user was real or randomly generated. This becomes a bit harder when the data is more complex than a boolean value, but with the use of Bloom filters we can employ this technique to integers and even strings. Below is a full implementation of how a database containing booleans, strings, and integers can be queried to return data that satisfies differential privacy guarantees.

### Python Code Example:

First we create classes to make our database handling a bit easier. The first class, ColumnType, is essentially just an array with a few other attributes that makes identifying the type easier.

```python
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
```

The second class we created is the Database class, to hold these ColumnType objects. It's a bit superfluous, but in the interest of containing the entire database within a class it's necessary and can add functionality in the future.

```python
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
```

Now that we have established our data structures and created a template for how the database will be laid out, it is time to populate our database. For the boolean column, this is just 10 pseudo-randomly generated boolean values. The int column is a little more complex, 10,000 pseudorandom ints with a normal distribution are generated to populate this column. This is the easiest data type to compare distributions between databases, so it was important to have this be large and semi-deterministic. The string column is similar to the boolean column, just 10 fruits picked randomly from the author's brain.

```python
booldata = ColumnType('bool',[True,False,True,True,
                              True,True,False,False,True,False])
intdata = ColumnType('int',[int(round(np.random.normal(50,4))) for _ in range(10000)])
stringdata = ColumnType('string',['peach','pear','apple','orange','grape',
                                  'banana','kiwi','mango','guava','nectarine'])
std_db = Database('std',[booldata,intdata,stringdata]) #new normal database
```

Since we have a populated database to work with, we can now begin to walk through the process of querying it to get differentially private data. Below is the full function for querying, but lets step through it slowly.

```python
def query_db(database,column,hash_num):
    # column is column index, hash_num is number of hashes you want to perform
    datacol = database[column] #should be ColumnType object
    type = datacol.type
    ret_col = []
    if type == 'bool':
        # do the simple randomized response thing
        for data in datacol:
            c = random.randint(0,1)
            if c == 0:
                ret_col.append(data)
            else: ret_col.append(bool(random.randint(0,1)))
        return ColumnType(type,ret_col)
    elif type == 'int' or type == 'string':
        # do the bloom filter
        for data in datacol:
            ret_col.append(to_bloom_filter(data,hash_num))
        return ColumnType(type,ret_col)
    else: return 'data not in correct format'
```
In this function, we first need to determine which type of data we are looking at, and this is where our ColumnType class comes in handy since it specifies the type.
##### If it's a Boolean:
If the data is a simple boolean type, we don't need to do anything complicated. All we must do is flip a coin, and if the coin is heads we return the real data. However, if the coin is tails, we flip the coin again and return the result of that coin flip. Since any observer of the new data does not know the result of the first coin flip, they cannot ever be sure if the data point they are viewing is randomly generated or real. However, since the generated data is in fact random, it does not skew the descriptive statistics of the database.
## If it's an Int or String
One of the nice properties of integers is that they can be very easily represented as strings by adding a ''. It is for this reason that we treat them similarly in this example. Unfortunately they are a bit trickier to deal with than simple booleans. To get data that satisfies differential privacy here, we must use a Bloom filter. A Bloom filter is a simple data structure, represented here as a bit vector, that will tell you with high confidence if it contains a certain value and with reasonable confidence if it does not contain a value.
To learn more about them, go [here](https://llimllib.github.io/bloomfilter-tutorial/)
