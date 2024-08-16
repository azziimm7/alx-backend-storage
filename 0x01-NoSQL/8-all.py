#!/usr/bin/env python3
"""A module that uses PyMongo to list all documents in a collection"""


def list_all(mongo_collection):
    """Lis all documents in a collection"""
    return mongo_collection.find()
