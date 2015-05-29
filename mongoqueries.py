#!/usr/bin/env python

# This program is to make queries to the MongoDB imported for the Open Street Map project

def get_db(db_name):
    # initialize DB
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # the aggregation pipeline
    pipeline = [
{"$match":{"address.city":{"$exists":1}}},
{"$group":{"_id":"$address.city", "count":{"$sum":1}}},
{"$sort":{"count":-1}},
{"$limit":10}


            #{"$match":{"amenity":{"$exists":1}, "$or":[{"amenity":"restaurant"}, {"amenity":"fast_food"}, {"amenity":"cafe"}]}},
            #{"$group":{"_id":"$name", "count":{"$sum":1}}},
            #{"$sort":{"count":-1}},
            #{"$limit":10}
        ]
    return pipeline

def aggregate(db, pipeline):
    # aggregate pipeline then return the result
    result = db.HongKong.aggregate(pipeline)
    return result

if __name__ == '__main__':
    # initialize DB
    db = get_db('OpenStreetMap')
    
    # starting from this line are the queries for the projects

    # number of records
    # print db.HongKong.find().count()

    # number of nodes
    # print db.HongKong.find({"type":"node"}).count()

    # number of nodes
    # print db.HongKong.find({"type":"way"}).count()
    
    # number of distinct users
    # print len(db.HongKong.distinct("created.user"))

    # top 10 contributing users
    # {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
    # {"$sort":{"count":-1}},
    # {"$limit":10}    
    
    # number of user contributing only once
    # {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
    # {"$group":{"_id":"$count", "num_user":{"$sum":1}}},
    # {"$sort":{"_id":1}},
    # {"$limit":1}
    
    # number of city if exists
    # {"$match":{"address.city":{"$exists":1}}},
    # {"$group":{"_id":"$address.city", "count":{"$sum":1}}},
    # {"$sort":{"count":-1}}
            
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    for doc in result:
        print doc
    #import pprint
    #pprint.pprint(result)
    