#!/usr/bin/env python3
""" 12-log_stats """

from pymongo import MongoClient


def log_stats(mongo_collection):
    """Provides some stats about Nginx logs stored in MongoDB"""
    # Total logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Method stats
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Status check stats
    status_check_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    mongo_collection = db.nginx
    log_stats(mongo_collection)
