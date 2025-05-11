# CONSTRUCTORS' PERFORMANCES

## Topic: "leaderboard evolution during a season"
> The following query is used inside ***scoreboard_season.py*** with "season" as input

    db.races.aggregate([
        { $match: {
            year: < season >
            }
        },
        { $lookup: {
            from: "constructor_standings",
            localField: "raceId",
            foreignField: "raceId",
            as: "constructor_standings"
            }
        },
        { $unwind: "$constructor_standings"},
        { $lookup:{
            from: "constructors",
            localField: "constructor_standings.constructorId",
            foreignField: "constructorId",
            as: "constructor_info"    
            }
        },
        { $project: {
            _id: 0,
            round: 1,
            name: 1,
            constructor_name: "$constructor_info.name",
            constructor_points: "$constructor_standings.points"
            }
        },
        { $group: {
            _id: "$round",
            standings: {
                $push: {
                    name: {"$first": "$constructor_name"},
                    points: "$constructor_points"
                    }
                }
            }
        }, 
        { $sort: {"_id": 1}}
    ])


## Topic: "points-pit stops comparison of constructors during weekends"
>  The following query is used inside ***pit_stops.py*** with "season" as the input inserted by the user

    db.results.aggregate([
        { $lookup: {
            from: "races", 
            foreignField: "raceId", 
            localField: "raceId", 
            as: < season >
        }},
        { $unwind: "$season" },
        { $match: { "season.year": < season >} },
        { $lookup: {
            from: "pit_stops",
            let: { driver: "$driverId", race: "$raceId" },
            pipeline: [
                { $match: { "$expr": { "$and": [
                    { "$eq": [ "$$driver", "$driverId" ] },
                    { "$eq": [ "$$race", "$raceId" ] }
                ]}}},
                { $count: "num_pitstops" }
            ],
            as: "pit_stop"
        }},
        { $lookup: {
            from: "constructors", 
            foreignField: "constructorId", 
            localField: "constructorId", 
            as: "constructorInfo"
        }},
        { $project: {
            _id: 0,
            constructorName: "$constructorInfo.name",
            round: "$season.round",
            gp: "$season.name",
            pitStops: { 
                $cond: { 
                    if: { $gt: [ { $size: "$pit_stop" }, 0 ] },
                    then: { $arrayElemAt: [ "$pit_stop.num_pitstops", 0 ] },
                    else: 0
                }
            },
            points: 1
        }},
        { $group: {
            _id: { constructor: "$constructorName", round: "$round" },
            totalPitStop: { $sum: "$pitStops" },
            totalPoints: { $sum: "$points" },
            gp: { $first: "$gp" }
        }},
        { $project: {
            _id: 0,
            constructor: { $first: "$_id.constructor" },
            round: "$_id.round",
            totalPitStop: 1,
            totalPoints: 1,
            gp: 1
        }},
        { $sort: {
            round: 1,
            constructor: 1
        }}
    ])

## Topic: "team points trend of a team along seasons"
> The following query is used inside the file ***season_points.py***, where "constructor" is the name of the team given as input by the user

    db.results.aggregate([
        { $lookup: {
            from: "constructor_standings",
            localField: "raceId",
            foreignField: "raceId",
            as: "constructor_standings"
        }},
        { $unwind: "$constructor_standings" },
        { $lookup: {
            from: "constructors",
            foreignField: "constructorId",
            localField: "constructor_standings.constructorId",
            as: "constructor_info"
        }},
        { $match: {
            "constructor_info.name": < constructor >
        }},
        { $project: {
            _id: 0,
            raceId: 1,
            year: 1,
            round: 1,
            "constructor_standings.points": 1,
            "constructor_info.name": 1,
            "constructor_info.constructorId": 1
        }},
        { $group: {
            _id: {
                year: "$year",
                name: "$constructor_info.name"
            },
            standings: {
                $push: {
                    round: "$round",
                    points: "$constructor_standings.points"
                }
            }
        }},
        { $project: {
            _id: 0,
            year: "$_id.year",
            points: { $max: "$standings.points" }
        }},
        { $sort: { year: 1 }}
    ])
