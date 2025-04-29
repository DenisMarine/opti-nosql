db.offers.insertMany([
  {
    from: "PAR",
    to: "TYO",
    departDate: ISODate("2025-05-10T10:00:00Z"),
    returnDate: ISODate("2025-05-20T10:00:00Z"),
    provider: "AirZen",
    price: 750.0,
    currency: "EUR",
    legs: [
      { flightNum: "AF123", dep: "PAR", arr: "TYO", duration: 12 },
      { flightNum: "AF124", dep: "TYO", arr: "PAR", duration: 12 },
    ],
    hotel: {
      name: "Hotel Tokyo",
      nights: 10,
      price: 1000.0,
    },
    activity: {
      title: "Sightseeing Tour",
      price: 150.0,
    },
  },
  {
    from: "LON",
    to: "NYC",
    departDate: ISODate("2025-06-15T15:00:00Z"),
    returnDate: ISODate("2025-06-25T15:00:00Z"),
    provider: "SkyTravel",
    price: 900.0,
    currency: "USD",
    legs: [
      { flightNum: "BA567", dep: "LON", arr: "NYC", duration: 8 },
      { flightNum: "BA568", dep: "NYC", arr: "LON", duration: 8 },
    ],
    hotel: null,
    activity: null,
  },
]);
