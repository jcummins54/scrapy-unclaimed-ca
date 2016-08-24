To initalize project:
-----------
```
scrapy startproject unclaimed
```

To run the crawler:
-----------
```
scrapy crawl casearch -a start=3430000 -a end=3430010
```

Database Commands
-----------
```
ln -sfv /usr/local/opt/mongodb/*.plist ~/Library/LaunchAgents
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist
```
```
use unclaimed
db.users.save( {username:"uncle"} )
```
```
db.items.insert({
   id: '987654321',
   recid: '12345678',
   date: '07/27/2016',
   source: 'test',
   name: 'Test Name',
   address: '123 Test Ave.',
   type: 'test',
   cash: '22.50',
   reportedby: 'test'
})
```
```
db.items.find().sort( { cash: -1 } ).limit(100).toArray()
```
```
db.items.find().sort( { recid: -1 } ).limit(1).toArray()
```
```
db.items.count()
```
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
```
db.items.find({ cash: {$exists: false} }).sort( { cash: 1 } ).count()
```
```
db.items.find({ cash: {$gt: 50000} }).sort( { cash: 1 } ).toArray()
```

Create a unique index:
```
db.items.createIndex( { recid: 1 }, { unique: true } )
db.items.getIndexes()
```

Export collection to csv:
```
mongoexport -h localhost -d unclaimed -c items --csv --fields name,reportedby,cash,source,recid,address,date,type,id --out unclaimed.csv
```

```
db.items.aggregate({ $match: { cash: {$gte: 50000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 5000, $lt: 50000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 500, $lt: 5000} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 100, $lt: 500} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 50, $lt: 100} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gte: 5, $lt: 50} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
db.items.aggregate({ $match: { cash: {$gt: 0, $lt: 5} } }, { $group: { _id : null, sum : { $sum: "$cash" } } });
```

Duplicate collection:
```
db.items.aggregate([ { $out: "items2" } ]);
db.items.aggregate([ { $out: "items3" } ]);
```

Find items in a range:
```
db.items.find({ recid: { $lt: "29100000" } }).sort( { recid: -1 } ).limit(1).toArray()
```

Cast recid to int
```
db.items3.find().forEach(function(data) {
    db.items3.update( { _id: data._id }, { $set: { recid: parseFloat(data.recid) } } );
});

typeof db.items3.find( { recid: 3427563 } )[0].recid
```