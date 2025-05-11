# FAILURES AND RETIREMENTS 
## Topic: "most frequent failures during all the seasons"
### Step 1: creation of a new collection containing only useful statuses for the purposes of the topic
> For semplicity, documents not interesting are removed by GUI (MongoDB Compass)

    db.status.aggregate({$out: "bad_status"})

### Step 2: < TODO >


## Topic: "most frequent failures for each grand prix"

    db.results.aggregate([
        {
            $lookup: {
                from: "races",
                localField: "raceId",
                foreignField: "raceId",
                as: "races"
            }
        },
        {
            $unwind: "$races"
        },
        {
            $match: {
                "fastestLapSpeed": { $ne: "\\N" }
            }
        },
        {
            $group: {
                _id: {
                    "circuit_id": "$races.circuitId",
                    "name": "$races.name"
                },
                fastest_lap_speeds: { $avg: "$fastestLapSpeed" }
            }
        },
        {
            $lookup: {
                from: "most_frequent_failure_grand_prix",
                foreignField: "_id",
                localField: "_id.name",
                as: "most_frequent_failure"
            }
        },
        {
            $lookup: {
                from: "circuits",
                localField: "_id.circuit_id",
                foreignField: "circuitId",
                as: "circuit_info"
            }
        },
        {
            $project: {
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
        {
            $sort: {
                "avg_fastest_lap_speed": -1
            }
        }
    ])
