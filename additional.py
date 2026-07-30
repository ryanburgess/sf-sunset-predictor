# Remove the existing Brooklyn entry, then append these:

cities.extend([
    # United States — Pacific Northwest
    {
        "slug": "seattle",
        "name": "Seattle",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo(
            "Seattle", "USA", "America/Los_Angeles",
            47.6062, -122.3321
        ).observer
    },
    {
        "slug": "portland",
        "name": "Portland",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo(
            "Portland", "USA", "America/Los_Angeles",
            45.5152, -122.6784
        ).observer
    },

    # United States — Mountain and Southwest
    {
        "slug": "las-vegas",
        "name": "Las Vegas",
        "timezone": "America/Los_Angeles",
        "observer": LocationInfo(
            "Las Vegas", "USA", "America/Los_Angeles",
            36.1699, -115.1398
        ).observer
    },
    {
        "slug": "phoenix",
        "name": "Phoenix",
        "timezone": "America/Phoenix",
        "observer": LocationInfo(
            "Phoenix", "USA", "America/Phoenix",
            33.4484, -112.0740
        ).observer
    },
    {
        "slug": "denver",
        "name": "Denver",
        "timezone": "America/Denver",
        "observer": LocationInfo(
            "Denver", "USA", "America/Denver",
            39.7392, -104.9903
        ).observer
    },
    {
        "slug": "salt-lake-city",
        "name": "Salt Lake City",
        "timezone": "America/Denver",
        "observer": LocationInfo(
            "Salt Lake City", "USA", "America/Denver",
            40.7608, -111.8910
        ).observer
    },

    # United States — Texas and Central
    {
        "slug": "dallas",
        "name": "Dallas",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Dallas", "USA", "America/Chicago",
            32.7767, -96.7970
        ).observer
    },
    {
        "slug": "houston",
        "name": "Houston",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Houston", "USA", "America/Chicago",
            29.7604, -95.3698
        ).observer
    },
    {
        "slug": "austin",
        "name": "Austin",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Austin", "USA", "America/Chicago",
            30.2672, -97.7431
        ).observer
    },
    {
        "slug": "san-antonio",
        "name": "San Antonio",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "San Antonio", "USA", "America/Chicago",
            29.4241, -98.4936
        ).observer
    },
    {
        "slug": "minneapolis",
        "name": "Minneapolis",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Minneapolis", "USA", "America/Chicago",
            44.9778, -93.2650
        ).observer
    },
    {
        "slug": "kansas-city",
        "name": "Kansas City",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Kansas City", "USA", "America/Chicago",
            39.0997, -94.5786
        ).observer
    },
    {
        "slug": "nashville",
        "name": "Nashville",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "Nashville", "USA", "America/Chicago",
            36.1627, -86.7816
        ).observer
    },
    {
        "slug": "new-orleans",
        "name": "New Orleans",
        "timezone": "America/Chicago",
        "observer": LocationInfo(
            "New Orleans", "USA", "America/Chicago",
            29.9511, -90.0715
        ).observer
    },

    # United States — East and Southeast
    {
        "slug": "miami",
        "name": "Miami",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Miami", "USA", "America/New_York",
            25.7617, -80.1918
        ).observer
    },
    {
        "slug": "orlando",
        "name": "Orlando",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Orlando", "USA", "America/New_York",
            28.5383, -81.3792
        ).observer
    },
    {
        "slug": "atlanta",
        "name": "Atlanta",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Atlanta", "USA", "America/New_York",
            33.7490, -84.3880
        ).observer
    },
    {
        "slug": "washington-dc",
        "name": "Washington, D.C.",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Washington, D.C.", "USA", "America/New_York",
            38.9072, -77.0369
        ).observer
    },
    {
        "slug": "philadelphia",
        "name": "Philadelphia",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Philadelphia", "USA", "America/New_York",
            39.9526, -75.1652
        ).observer
    },
    {
        "slug": "boston",
        "name": "Boston",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Boston", "USA", "America/New_York",
            42.3601, -71.0589
        ).observer
    },
    {
        "slug": "charleston",
        "name": "Charleston",
        "timezone": "America/New_York",
        "observer": LocationInfo(
            "Charleston", "USA", "America/New_York",
            32.7765, -79.9311
        ).observer
    },

    # United States — Alaska and Hawaii
    {
        "slug": "anchorage",
        "name": "Anchorage",
        "timezone": "America/Anchorage",
        "observer": LocationInfo(
            "Anchorage", "USA", "America/Anchorage",
            61.2181, -149.9003
        ).observer
    },
    {
        "slug": "honolulu",
        "name": "Honolulu",
        "timezone": "Pacific/Honolulu",
        "observer": LocationInfo(
            "Honolulu", "USA", "Pacific/Honolulu",
            21.3099, -157.8581
        ).observer
    },

    # Canada
    {
        "slug": "edmonton",
        "name": "Edmonton",
        "timezone": "America/Edmonton",
        "observer": LocationInfo(
            "Edmonton", "Canada", "America/Edmonton",
            53.5461, -113.4938
        ).observer
    },
    {
        "slug": "winnipeg",
        "name": "Winnipeg",
        "timezone": "America/Winnipeg",
        "observer": LocationInfo(
            "Winnipeg", "Canada", "America/Winnipeg",
            49.8951, -97.1384
        ).observer
    },
    {
        "slug": "ottawa",
        "name": "Ottawa",
        "timezone": "America/Toronto",
        "observer": LocationInfo(
            "Ottawa", "Canada", "America/Toronto",
            45.4215, -75.6972
        ).observer
    },
    {
        "slug": "quebec-city",
        "name": "Quebec City",
        "timezone": "America/Toronto",
        "observer": LocationInfo(
            "Quebec City", "Canada", "America/Toronto",
            46.8139, -71.2080
        ).observer
    },
    {
        "slug": "halifax",
        "name": "Halifax",
        "timezone": "America/Halifax",
        "observer": LocationInfo(
            "Halifax", "Canada", "America/Halifax",
            44.6488, -63.5752
        ).observer
    },
    {
        "slug": "st-johns",
        "name": "St. John's",
        "timezone": "America/St_Johns",
        "observer": LocationInfo(
            "St. John's", "Canada", "America/St_Johns",
            47.5615, -52.7126
        ).observer
    },

    # Mexico and Latin America
    {
        "slug": "mexico-city",
        "name": "Mexico City",
        "timezone": "America/Mexico_City",
        "observer": LocationInfo(
            "Mexico City", "Mexico", "America/Mexico_City",
            19.4326, -99.1332
        ).observer
    },
    {
        "slug": "cabo-san-lucas",
        "name": "Cabo San Lucas",
        "timezone": "America/Mazatlan",
        "observer": LocationInfo(
            "Cabo San Lucas", "Mexico", "America/Mazatlan",
            22.8905, -109.9167
        ).observer
    },
    {
        "slug": "rio-de-janeiro",
        "name": "Rio de Janeiro",
        "timezone": "America/Sao_Paulo",
        "observer": LocationInfo(
            "Rio de Janeiro", "Brazil", "America/Sao_Paulo",
            -22.9068, -43.1729
        ).observer
    },
    {
        "slug": "buenos-aires",
        "name": "Buenos Aires",
        "timezone": "America/Argentina/Buenos_Aires",
        "observer": LocationInfo(
            "Buenos Aires", "Argentina",
            "America/Argentina/Buenos_Aires",
            -34.6037, -58.3816
        ).observer
    },

    # Europe
    {
        "slug": "amsterdam",
        "name": "Amsterdam",
        "timezone": "Europe/Amsterdam",
        "observer": LocationInfo(
            "Amsterdam", "Netherlands", "Europe/Amsterdam",
            52.3676, 4.9041
        ).observer
    },
    {
        "slug": "barcelona",
        "name": "Barcelona",
        "timezone": "Europe/Madrid",
        "observer": LocationInfo(
            "Barcelona", "Spain", "Europe/Madrid",
            41.3874, 2.1686
        ).observer
    },
    {
        "slug": "madrid",
        "name": "Madrid",
        "timezone": "Europe/Madrid",
        "observer": LocationInfo(
            "Madrid", "Spain", "Europe/Madrid",
            40.4168, -3.7038
        ).observer
    },
    {
        "slug": "lisbon",
        "name": "Lisbon",
        "timezone": "Europe/Lisbon",
        "observer": LocationInfo(
            "Lisbon", "Portugal", "Europe/Lisbon",
            38.7223, -9.1393
        ).observer
    },
    {
        "slug": "berlin",
        "name": "Berlin",
        "timezone": "Europe/Berlin",
        "observer": LocationInfo(
            "Berlin", "Germany", "Europe/Berlin",
            52.5200, 13.4050
        ).observer
    },
    {
        "slug": "copenhagen",
        "name": "Copenhagen",
        "timezone": "Europe/Copenhagen",
        "observer": LocationInfo(
            "Copenhagen", "Denmark", "Europe/Copenhagen",
            55.6761, 12.5683
        ).observer
    },
    {
        "slug": "dublin",
        "name": "Dublin",
        "timezone": "Europe/Dublin",
        "observer": LocationInfo(
            "Dublin", "Ireland", "Europe/Dublin",
            53.3498, -6.2603
        ).observer
    },
    {
        "slug": "edinburgh",
        "name": "Edinburgh",
        "timezone": "Europe/London",
        "observer": LocationInfo(
            "Edinburgh", "United Kingdom", "Europe/London",
            55.9533, -3.1883
        ).observer
    },
    {
        "slug": "reykjavik",
        "name": "Reykjavik",
        "timezone": "Atlantic/Reykjavik",
        "observer": LocationInfo(
            "Reykjavik", "Iceland", "Atlantic/Reykjavik",
            64.1466, -21.9426
        ).observer
    },
    {
        "slug": "athens",
        "name": "Athens",
        "timezone": "Europe/Athens",
        "observer": LocationInfo(
            "Athens", "Greece", "Europe/Athens",
            37.9838, 23.7275
        ).observer
    },
    {
        "slug": "istanbul",
        "name": "Istanbul",
        "timezone": "Europe/Istanbul",
        "observer": LocationInfo(
            "Istanbul", "Turkey", "Europe/Istanbul",
            41.0082, 28.9784
        ).observer
    },

    # Asia and Middle East
    {
        "slug": "dubai",
        "name": "Dubai",
        "timezone": "Asia/Dubai",
        "observer": LocationInfo(
            "Dubai", "United Arab Emirates", "Asia/Dubai",
            25.2048, 55.2708
        ).observer
    },
    {
        "slug": "singapore",
        "name": "Singapore",
        "timezone": "Asia/Singapore",
        "observer": LocationInfo(
            "Singapore", "Singapore", "Asia/Singapore",
            1.3521, 103.8198
        ).observer
    },
    {
        "slug": "hong-kong",
        "name": "Hong Kong",
        "timezone": "Asia/Hong_Kong",
        "observer": LocationInfo(
            "Hong Kong", "Hong Kong", "Asia/Hong_Kong",
            22.3193, 114.1694
        ).observer
    },
    {
        "slug": "seoul",
        "name": "Seoul",
        "timezone": "Asia/Seoul",
        "observer": LocationInfo(
            "Seoul", "South Korea", "Asia/Seoul",
            37.5665, 126.9780
        ).observer
    },
    {
        "slug": "bangkok",
        "name": "Bangkok",
        "timezone": "Asia/Bangkok",
        "observer": LocationInfo(
            "Bangkok", "Thailand", "Asia/Bangkok",
            13.7563, 100.5018
        ).observer
    },

    # Oceania and Africa
    {
        "slug": "sydney",
        "name": "Sydney",
        "timezone": "Australia/Sydney",
        "observer": LocationInfo(
            "Sydney", "Australia", "Australia/Sydney",
            -33.8688, 151.2093
        ).observer
    },
    {
        "slug": "melbourne",
        "name": "Melbourne",
        "timezone": "Australia/Melbourne",
        "observer": LocationInfo(
            "Melbourne", "Australia", "Australia/Melbourne",
            -37.8136, 144.9631
        ).observer
    },
    {
        "slug": "auckland",
        "name": "Auckland",
        "timezone": "Pacific/Auckland",
        "observer": LocationInfo(
            "Auckland", "New Zealand", "Pacific/Auckland",
            -36.8509, 174.7645
        ).observer
    },
    {
        "slug": "cape-town",
        "name": "Cape Town",
        "timezone": "Africa/Johannesburg",
        "observer": LocationInfo(
            "Cape Town", "South Africa", "Africa/Johannesburg",
            -33.9249, 18.4241
        ).observer
    }
])