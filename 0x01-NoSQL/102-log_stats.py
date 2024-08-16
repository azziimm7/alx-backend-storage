#!/usr/bin/env python3
"""A script that provides some stats about Nginx logs stored in MongoDB"""

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    num_docs = nginx.count_documents({})
    print(f'{num_docs} logs')
    print('Methods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for m in methods:
        count = nginx.count_documents({"method": m})
        print(f"\tmethod {m}: {count}")
    status = nginx.count_documents({"$and":
                                    [{"method": "GET"},
                                     {"path": "/status"}
                                     ]
                                    })
    print(f'{status} status check')
    ips = nginx.aggregate([
                {
                    "$group":
                        {
                            "_id": "$ip",
                            "count": {"$sum": 1}
                        }
                },
                {
                    "$sort":
                        {
                            "count": -1
                        }
                },
                {
                    "$limit": 10
                }
            ])
    print("IPs:")
    for ip in ips:
        count = ip['count']
        address = ip['_id']
        print(f'\t{address}: {count}')
