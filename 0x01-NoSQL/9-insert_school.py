#!/usr/bin/env python3
"""A module that uses PyMongo to insert a documents in a collection"""


def insert_school(mongo_collection, **kwargs):
    """Insert a documents in a collection"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
