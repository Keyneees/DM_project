# DRIVERS' PERFORMANCES

## Topic: "average point scored in a weekend"

### Step 1

db.createView(
  "driver_detailed",
  "drivers",
  [
    {
      $lookup: {
        from: "driver_standings",
        localField: "driverId",
        foreignField: "driverId",
        as: "standings"
      }
    },
    {
      $project: {
        _id: 0,
        driverId: 1,
        number: 1,
        code: 1,
        forename: 1,
        surname: 1,
        dob: 1,
        nationality: 1,
        "standings.raceId": 1,
        "standings.points": 1,
        "standings.position": 1,
        "standings.wins": 1
      }
    }
  ]
);

### Step 2

db.driver_detailed.aggregate([
  {
    $lookup: {
      from: "races",
      localField: "standings.raceId",
      foreignField: "raceId",
      as: "races_info"
    }
  },
  {
    $addFields: {
      standings: {
        $map: {
          input: "$standings",
          as: "s",
          in: {
            raceId: "$$s.raceId",
            points: "$$s.points",
            position: "$$s.position",
            wins: "$$s.wins",
            name: {
              $first: {
                $map: {
                  input: {
                    $filter: {
                      input: "$races_info",
                      as: "r",
                      cond: {
                        $eq: ["$$r.raceId", "$$s.raceId"]
                      }
                    }
                  },
                  as: "race",
                  in: "$$race.name"
                }
              }
            },
            year: {
              $first: {
                $map: {
                  input: {
                    $filter: {
                      input: "$races_info",
                      as: "r",
                      cond: {
                        $eq: ["$$r.raceId", "$$s.raceId"]
                      }
                    }
                  },
                  as: "race",
                  in: "$$race.year"
                }
              }
            },
            round: {
              $first: {
                $map: {
                  input: {
                    $filter: {
                      input: "$races_info",
                      as: "r",
                      cond: {
                        $eq: ["$$r.raceId", "$$s.raceId"]
                      }
                    }
                  },
                  as: "race",
                  in: "$$race.round"
                }
              }
            }
          }
        }
      }
    }
  },
  {
    $project: {
      races_info: 0
    }
  }
]);


### Step 3

db.createView(
  "drivers_detailed",
  "driver_detailed",
  [
    {
      $lookup: {
        from: "races",
        localField: "standings.raceId",
        foreignField: "raceId",
        as: "races_info"
      }
    },
    {
      $addFields: {
        standings: {
          $map: {
            input: "$standings",
            as: "s",
            in: {
              raceId: "$$s.raceId",
              points: "$$s.points",
              position: "$$s.position",
              wins: "$$s.wins",
              name: {
                $first: {
                  $map: {
                    input: {
                      $filter: {
                        input: "$races_info",
                        as: "r",
                        cond: { $eq: ["$$r.raceId", "$$s.raceId"] }
                      }
                    },
                    as: "race",
                    in: "$$race.name"
                  }
                }
              },
              year: {
                $first: {
                  $map: {
                    input: {
                      $filter: {
                        input: "$races_info",
                        as: "r",
                        cond: { $eq: ["$$r.raceId", "$$s.raceId"] }
                      }
                    },
                    as: "race",
                    in: "$$race.year"
                  }
                }
              },
              round: {
                $first: {
                  $map: {
                    input: {
                      $filter: {
                        input: "$races_info",
                        as: "r",
                        cond: { $eq: ["$$r.raceId", "$$s.raceId"] }
                      }
                    },
                    as: "race",
                    in: "$$race.round"
                  }
                }
              }
            }
          }
        }
      }
    },
    {
      $project: {
        races_info: 0
      }
    }
  ]
);


### Step 4

db.drivers_detailed.aggregate([
  {
    $unwind: "$standings"
  },
  {
    $group: {
      _id: {
        driverId: "$driverId",
        surname: "$surname",
        forename: "$forename",
        year: "$standings.year"
      },
      max_points: { $max: "$standings.points" },
      rounds: { $max: "$standings.round" }
    }
  },
  {
    $group: {
      _id: {
        driverId: "$_id.driverId",
        surname: "$_id.surname",
        forename: "$_id.forename"
      },
      seasons: {
        $push: {
          year: "$_id.year",
          points: "$max_points",
          races: "$rounds",
          average_points: {
            $divide: ["$max_points", "$rounds"]
          }
        }
      }
    }
  }
]);


### Step 5

db.createView(
  "drivers_standings_during_weekend",
  "drivers_detailed",
  [
    {
      $unwind: "$standings"
    },
    {
      $group: {
        _id: {
          driverId: "$driverId",
          surname: "$surname",
          year: "$standings.year"
        },
        max_points: { $max: "$standings.points" },
        rounds: { $max: "$standings.round" }
      }
    },
    {
      $group: {
        _id: {
          driverId: "$_id.driverId",
          surname: "$_id.surname"
        },
        seasons: {
          $push: {
            year: "$_id.year",
            points: "$max_points",
            races: "$rounds",
            average_points: {
              $divide: ["$max_points", "$rounds"]
            }
          }
        }
      }
    }
  ]
);


### Step 6

db.createView(
  "restricted_weekend_standings",
  "drivers_standings_during_weekend",
  [
    {
      $match: {
        $or: [
          { "_id.surname": "Ricciardo" },
          {
            "_id.surname": "Verstappen",
            "_id.forename": "Max"
          }
        ]
      }
    }
  ]
);

## Topic: "average points scored in a weekend per constructors"

db.drivers.aggregate([
  {
    $match: {
      forename: "Max",
      surname: "Verstappen"
    }
  },
  {
    $lookup: {
      from: "results",
      localField: "driverId",
      foreignField: "driverId",
      as: "results"
    }
  },
  {
    $unwind: "$results"
  },
  {
    $project: {
      _id: 0,
      driverId: 1,
      forename: 1,
      surname: 1,
      constructorId: "$results.constructorId",
      points: { $toDouble: "$results.points" }
    }
  },
  {
    $group: {
      _id: {
        driverId: "$driverId",
        constructorId: "$constructorId"
      },
      name: { $first: "$forename" },
      surname: { $first: "$surname" },
      avgPoints: { $avg: "$points" }
    }
  },
  {
    $lookup: {
      from: "constructors",
      let: { cid: "$_id.constructorId" },
      pipeline: [
        {
          $match: {
            $expr: { $eq: ["$constructorId", "$$cid"] }
          }
        },
        {
          $project: {
            _id: 0,
            name: 1
          }
        }
      ],
      as: "constructor"
    }
  },
  {
    $project: {
      name: 1,
      surname: 1,
      constructor: { $arrayElemAt: ["$constructor.name", 0] },
      avgPoints: 1
    }
  }
]);

## Topic: "teammates comparison in a season"

db.constructors.aggregate([
  {
    $match: {
      name: "RedBull"
    }
  },
  {
    $lookup: {
      from: "results",
      let: { constructorId: "$constructorId" },
      pipeline: [
        {
          $match: {
            $expr: {
              $eq: ["$constructorId", "$$constructorId"]
            }
          }
        },
        {
          $lookup: {
            from: "races",
            localField: "raceId",
            foreignField: "raceId",
            as: "race"
          }
        },
        {
          $unwind: "$race"
        },
        {
          $match: {
            "race.year": 2018
          }
        },
        {
          $lookup: {
            from: "drivers",
            localField: "driverId",
            foreignField: "driverId",
            as: "driver"
          }
        },
        {
          $unwind: "$driver"
        },
        {
          $project: {
            _id: 0,
            raceName: "$race.name",
            round: "$race.round",
            driver: {
              $concat: ["$driver.forename", " ", "$driver.surname"]
            },
            position: "$positionOrder",
            points: "$points"
          }
        }
      ],
      as: "driver_results"
    }
  },
  {
    $project: {
      _id: 0,
      name: 1,
      driver_results: 1
    }
  }
]);

### Topic: "final position vs average position in a season"

db.drivers.aggregate([
  {
    $lookup: {
      from: "driver_standings",
      let: { driverId: "$driverId" },
      pipeline: [
        {
          $match: {
            $expr: {
              $eq: ["$driverId", "$$driverId"]
            }
          }
        },
        {
          $lookup: {
            from: "races",
            foreignField: "raceId",
            localField: "raceId",
            as: "race"
          }
        },
        {
          $unwind: "$race"
        },
        {
          $match: {
            "race.year": 2018
          }
        },
        {
          $sort: {
            "race.round": -1
          }
        },
        {
          $limit: 1
        }
      ],
      as: "final_result"
    }
  },
  {
    $lookup: {
      from: "results",
      let: { driverId: "$driverId" },
      pipeline: [
        {
          $match: {
            $expr: {
              $eq: ["$driverId", "$$driverId"]
            }
          }
        },
        {
          $lookup: {
            from: "races",
            localField: "raceId",
            foreignField: "raceId",
            as: "race"
          }
        },
        {
          $unwind: "$race"
        },
        {
          $match: {
            "race.year": 2018
          }
        }
      ],
      as: "season_results"
    }
  },
  {
    $match: {
      "season_results.0": { $exists: true },
      "final_result.0": { $exists: true }
    }
  },
  {
    $project: {
      _id: 0,
      surname: 1,
      forename: 1,
      avgPosition: {
        $avg: {
          $map: {
            input: "$season_results",
            as: "results",
            in: { $toInt: "$$results.positionOrder" }
          }
        }
      },
      finalPosition: {
        $arrayElemAt: ["$final_result.position", 0]
      }
    }
  }
]);
