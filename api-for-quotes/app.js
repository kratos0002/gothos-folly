const Express = require("express");
const BodyParser = require("body-parser");
const MongoClient = require("mongodb").MongoClient;
const ObjectId = require("mongodb").ObjectID;


const CONNECTION_URL = "mongodb+srv://kratos0002:Mongodbsucks.123@cluster0.u5ocxsz.mongodb.net/?retryWrites=true&w=majority";
const DATABASE_NAME = "quotesdb";



const app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: true }));
var database, collection;


app.listen(4000, () => {
    MongoClient.connect(CONNECTION_URL, { useNewUrlParser: true }, (error, client) => {
        if(error) {
            throw error;
        }
        database = client.db(DATABASE_NAME);
        collection = database.collection("malazanq");
        console.log("Connected to `" + DATABASE_NAME + "`!");
    })

});

app.get("/all", (req, res) => {
    collection.find({}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.get("/all/book1", (req, res) => {
    collection.find({title: 'Gardens of the Moon'}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.get("/all/book2", (req, res) => {
    collection.find({title: 'Deadhouse Gates'}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.get("/all/book3", (req, res) => {
    collection.find({title: 'Memories of Ice'}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.get("/all/book4", (req, res) => {
    collection.find({title: 'House of Chains'}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.get("/all/book5", (req, res) => {
    collection.find({title: 'Midnight Tides'}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }cd
        res.send(result);
    });
});

app.get("/random", (req, res) => {
    collection.find({}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        const item = result[Math.floor(Math.random()*result.length-1)];
        res.send(item);
    });
});


app.get("/authors", (req, res) => {
    collection.distinct(("author"), (error, result) => {
       if(error) {
           return res.status(500).send(error);
       }
       res.send(result);
   })});


app.get("/titles", (req, res) => {
       collection.distinct(("title"), (error, result) => {
          if(error) {
              return res.status(500).send(error);
          }
          res.send(result);
      })});
