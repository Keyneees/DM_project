# World champion wins

## Topic: "number of wins of constructors champion along seasons"

db.races.aggregate([
  {
    $group: {
      _id: "$year",
      lastRound: { $max: "$round" }
    }
  },
  {
    $lookup: {
      from: "races",
      let: { year: "$_id", round: "$lastRound" },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [
                { $eq: ["$year", "$$year"] },
                { $eq: ["$round", "$$round"] }
              ]
            }
          }
        },
        {
          $project: {
            raceId: 1,
            year: 1
          }
        }
      ],
      as: "lastRace"
    }
  },
  {
    $unwind: "$lastRace"
  },
  {
    $lookup: {
      from: "constructor_standings",
      localField: "lastRace.raceId",
      foreignField: "raceId",
      as: "standing"
    }
  },
  {
    $unwind: "$standing"
  },
  {
    $match: {
      "standing.position": 1
    }
  },
  {
    $lookup: {
      from: "constructors",
      localField: "standing.constructorId",
      foreignField: "constructorId",
      as: "constructor"
    }
  },
  {
    $unwind: "$constructor"
  },
  {
    $project: {
      _id: 0,
      year: "$_id",
      constructorId: "$standing.constructorId",
      wins: "$standing.wins",
      name: "$constructor.name"
    }
  },
  {
    $sort: {
      year: 1
    }
  }
]);

## Topic: "number of wins of drivers champion during years"

db.races.aggregate([
  {
    $group: {
      _id: "$year",
      lastRound: { $max: "$round" }
    }
  },
  {
    $lookup: {
      from: "races",
      let: { year: "$_id", round: "$lastRound" },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [
                { $eq: ["$year", "$$year"] },
                { $eq: ["$round", "$$round"] }
              ]
            }
          }
        },
        {
          $project: {
            raceId: 1,
            year: 1
          }
        }
      ],
      as: "lastRace"
    }
  },
  {
    $unwind: "$lastRace"
  },
  {
    $lookup: {
      from: "driver_standings",
      localField: "lastRace.raceId",
      foreignField: "raceId",
      as: "standing"
    }
  },
  {
    $unwind: "$standing"
  },
  {
    $match: {
      "standing.position": 1
    }
  },
  {
    $lookup: {
      from: "drivers",
      localField: "standing.driverId",
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
      year: "$_id",
      driverId: "$standing.driverId",
      wins: "$standing.wins",
      name: "$driver.forename",
      surname: "$driver.surname"
    }
  },
  {
    $sort: {
      year: 1
    }
  }
]);
