# Differential Privacy: A Short Study

### Introduction

Differential Privacy is is a concept that, when applied correctly, can allow user data to be analyzed and computed upon without compromising any privacy. This is especially important with sensitive data such as medical records or income statements, which can be valuable data to researchers, but requires strict privacy guarantees before it can be used.
[expand this]

##### A simple example:

Differential Privacy can be achieved relatively easily in simple data with a concept called *randomized response*. This works by creating a user response that has a *p* probability of being a random response, and a *1-p* probability of being a true response. For example, if the creator of a particular system deployed a new feature, they might want to collect data from each user to see at what frequency they used the new feature. However, this would effectively create a database that links this information to each user. "What about anonymizing the database?" you might say. "Wouldn't that be a much easier way to keep the data private?" Unfortunately, the identifying information in databases like this is quite literally the information we are trying to anonymize. 

>  A vast majority of records in a database of size n can be reconstructed when n log(n)2 queries are answered by a statistical database ... even if each answer has been arbitrarily altered to have up to o(√n) error [Sigmod 2017, Machanavajjhala et al](http://sigmod2017.org/wp-content/uploads/2017/03/04-Differential-Privacy-in-the-wild-1.pdf).

To fix this problem, we can employ our randomized response technique so that even if an attacker were able to deanonymize our database, they would not know whether the data attached to each user was real or randomly generated. Below is a Python code snippet demonstrating this technique.
