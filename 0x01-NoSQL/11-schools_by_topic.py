#!/usr/bin/env python3
"""A module that uses PyMongo to find documents based on a filter"""


def schools_by_topic(mongo_collection, topic):
    """Find documents in a collection by applying a filter"""
    return mongo_collection.find({"topics": topic})
