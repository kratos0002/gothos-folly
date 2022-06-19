const Express = require("express");
const BodyParser = require("body-parser");
const MongoClient = require("mongodb").MongoClient;
const ObjectId = require("mongodb").ObjectID;


const CONNECTION_URL = "mongodb+srv://kratos0002:Mongodbsucks.123@cluster0.u5ocxsz.mongodb.net/?retryWrites=true&w=majority";
const DATABASE_NAME = "musicdb";



const app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: true }));
var database, collection;


app.listen(6000, () => {
    MongoClient.connect(CONNECTION_URL, { useNewUrlParser: true }, (error, client) => {
        if(error) {
            throw error;
        }
        database = client.db(DATABASE_NAME);
        collection = database.collection("music_c");
        console.log("Connected to `" + DATABASE_NAME + "`!");
    })

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


