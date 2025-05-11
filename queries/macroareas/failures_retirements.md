# FAILURES AND RETIREMENTS 
## Topic: "most frequent failures during all the seasons"
### Step 1: creation of a new collection containing only useful statuses for the purposes of the topic
> For semplicity, documents not interesting are removed by GUI (MongoDB Compass)

    db.status.aggregate({$out: "bad_status"})

### Step 2: creation of view based on "bad_status" collection for computing most frequent cause of retirement during each season
    db.results.aggregate([
        { $lookup: {
                from: "bad_status",
                foreignField: "statusId",
                localField: "statusId",
                as: "status_details"
            }
        },
        { $lookup: {
                from: "races",
                localField: "raceId",
                foreignField: "raceId",
                as: "race_details"
            }
        },
        { $project: {
                "_id": 0,
                "resultId": 1,
                "raceId": 1,
                "driverId": 1,
                "constructorId": 1,
                "positionOrder": 1,
                "statusId": 1,
                "status": "$status_details.status",
                "race_details.round": 1,
                "race_details.name": 1,
                "race_details.year": 1
            }
        },
        { $group: {
                _id: {
                    "year": "$race_details.year",
                    "status": "$status"
                },
                counter: { $sum: 1 }
            }
        },
        { $sort: {
                "_id.year": 1,
                "counter": -1
            }
        },
        { $match: {
                "_id.status": { $ne: [] }
            }
        },
        { $group: {
                _id: "$_id.year",
                most_frequent_failure: { $first: "$_id.status" },
                count: { $first: "$counter" }
            }
        },
        { $sort: { "_id": 1 }}
    ])



## Topic: "most frequent failures for each grand prix"

    db.results.aggregate([
        { $lookup: {
                from: "races",
                localField: "raceId",
                foreignField: "raceId",
                as: "races"
            }
        },
        { $unwind: "$races"},
        { $match: {
             "fastestLapSpeed": { $ne: "\\N" }
            }
        },
        { $group: {
                _id: {
                    "circuit_id": "$races.circuitId",
                    "name": "$races.name"
                },
                fastest_lap_speeds: { $avg: "$fastestLapSpeed" }
            }
        },
        { $lookup: {
                from: "most_frequent_failure_grand_prix",
                foreignField: "_id",
                localField: "_id.name",
                as: "most_frequent_failure"
            }
        },
        { $lookup: {
                from: "circuits",
                localField: "_id.circuit_id",
                foreignField: "circuitId",
                as: "circuit_info"
            }
        },
        { $project: {
                "_id": 0,
                "gp": "$_id.name",
                "name": "$circuit_info.name",
                "country": "$circuit_info.country",
                "alt": "$circuit_info.alt",
                "latitude": "$circuit_info.lat",
                "longitude": "$circuit_info.lng",
                "most_frequent_failure": { $first: "$most_frequent_failure.most_frequent_failure" },
                "avg_fastest_lap_speed": "$fastest_lap_speeds"
            }
        },
        { $sort: { "avg_fastest_lap_speed": -1}}
    ])
