#!/usr/bin/env python3
"""A module that returns all students sorted by average score"""


def top_students(mongo_collection):
    """Sort the students by their average score"""
    pipeline = [
        {
            "$project":
            {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
            {"averageScore": -1}
        }
    ]
    return mongo_collection.aggregate(pipeline)
