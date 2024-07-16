#!/usr/bin/env python3
"""Provide stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

def log_stats(mongo_collection):
    """Provide some stats about Nginx logs stored in MongoDB"""
    # Count total logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count methods
    print("Methods:")
    for method in METHODS:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count status check
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")

    # Count top 10 IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    log_stats(nginx_collection)

