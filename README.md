#Scrapy CA Unclaimed Crawler
Requires Python, MongoDB and Scrapy

####Initalize project:
```
scrapy startproject unclaimed
```

####Run the crawler:
```
scrapy crawl casearch -a start=3430000 -a end=3430010
```

####Mongo Database Commands:
Use the `unclaimed` table 
```
use unclaimed
```

Find the people with the most money owed
```
db.items.find().sort( { cash: -1 } ).limit(100).toArray()
```

Find the most recently added
```
db.items.find().sort( { recid: -1 } ).limit(1).toArray()
```

Total results
```
db.items.count()
```

Find results in different ranges of cash owed
```
db.items.find({ cash: {$gte: 50000} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gte: 5000, $lt: 50000} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gte: 500, $lt: 5000} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gte: 100, $lt: 500} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gte: 50, $lt: 100} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gte: 5, $lt: 50} }).sort( { cash: 1 } ).count()
db.items.find({ cash: {$gt: 0, $lt: 5} }).sort( { cash: 1 } ).count()
db.items.find({ cash: 0 }).sort( { cash: 1 } ).count()
```

Find people not owed any cash (typically owed bonds or some other non-cash property)
```
db.items.find({ cash: {$exists: false} }).sort( { cash: 1 } ).count()
```

Find the people owed the most over $50k
```
db.items.find({ cash: {$gt: 50000} }).sort( { cash: 1 } ).toArray()
```

Create a unique index
```
db.items.createIndex( { recid: 1 }, { unique: true } )
db.items.getIndexes()
```

Export collection to csv
```
mongoexport -h localhost -d unclaimed -c items --csv --fields name,reportedby,cash,source,recid,address,date,type,id --out unclaimed.csv
```

Find the total amount in a range
```
db.items.aggregate({ $match: { cash: {$gte: 50000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 5000, $lt: 50000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 500, $lt: 5000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 100, $lt: 500} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 50, $lt: 100} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 5, $lt: 50} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gt: 0, $lt: 5} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
```

Duplicate a collection
```
db.items.aggregate([ { $out: "items2" } ]);
db.items.aggregate([ { $out: "items3" } ]);
```

Cast `recid` to `int`
```
db.items3.find().forEach(function(data) {
    db.items3.update( { _id: data._id }, { $set: { recid: parseFloat(data.recid) } } );
});

typeof db.items3.find( { recid: 3427563 } )[0].recid
```