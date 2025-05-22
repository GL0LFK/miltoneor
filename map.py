import random
from collections import Counter

def generate_map(realm_width=10, realm_height=6):

    realm = [[0 for _ in range(realm_width)] for _ in range(realm_height)]

    fields = ["bridge", "cave", "fields", "forest", "hills", "mayor", "mountain", "plains", "blacksmith", "Alidar", "jewelery",
              "alchemy", "tavern", "shop", "stables", "coast", "underpass", "jail", "court", "Erigow", "Sirenar", "Yllinor"]

    y = 0
    x = 0

    total_fields = realm_width * realm_height
    field_limits = {
        "cave": 1,
        "Alidar": random.randint(0,1),
        "Erigow": random.randint(0,1),
        "Sirenar": random.randint(0,1),
        "Yllinor": 1,
        "court": random.randint(0,1),
        "jail": random.randint(1,2),
        "shop": random.randint(0,1),
        "mayor": random.randint(0,3),
        "tavern": random.randint(1,3),
        "jewelery": random.randint(1,2),
        "blacksmith": random.randint(1,2)
    }

    # Defining the adjacency rules for clustering fields and make the map appear more real
    adjacency_rules = {
        "fields": fields,  # fields can be next to anything
        "plains": fields,
        "forest": ["fields", "plains", "forest", "hills", "cave"],
        "hills": ["fields", "plains", "forest", "hills", "mountain", "cave"],
        "mountain": ["hills", "mountain", "cave"],
        "coast": ["fields", "plains", "coast", "bridge", "underpass"],
        "bridge": ["fields", "plains", "coast", "bridge"],
        "cave": ["forest", "hills", "mountain", "cave"],
        "Alidar": ["fields", "plains", "shop", "tavern", "stables"],
        "Erigow": ["fields", "coast", "jewelery", "alchemy", "tavern"],
        "Sirenar": ["fields", "plains", "mayor", "stables", "blacksmith"],
        "Yllinor": ["mountain", "forest", "mayor", "jewelery", "alchemy", "tavern", "shop", "stables", "blacksmith", "jail", "court"],
        "mayor": ["town", "fields", "plains"],
        "jewelery": ["town", "fields", "plains"],
        "alchemy": ["town", "fields", "plains"],
        "tavern": ["town", "fields", "plains"],
        "shop": ["town", "fields", "plains"],
        "stables": ["town", "fields", "plains"],
        "blacksmith": ["town", "fields", "plains"],
        "underpass": ["coast", "fields", "plains"],
        "jail": ["town", "fields", "plains"],
        "court": ["town", "fields", "plains"],
    }

    def count_field(field_name):
        return sum(row.count(field_name) for row in realm)

    def get_neighbors(realm, x, y):
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # left, right, up, down
            nx, ny = x + dx, y + dy
            if 0 <= nx < realm_width and 0 <= ny < realm_height:
                n = realm[ny][nx]
                if n != 0:
                    neighbors.append(n)
        return neighbors

    def get_valid_fields(neighbors):
        if not neighbors:
            return fields
        valid = []
        for f in fields:
            if all(n in adjacency_rules.get(f, fields) for n in neighbors):
                valid.append(f)
        return valid if valid else fields

    for y in range(realm_height):
        for x in range(realm_width):
            while True:
                field = random.choice(fields)
                if field in field_limits:
                    if count_field(field) < field_limits[field]:
                        realm[y][x] = field
                        break
                else:
                    realm[y][x] = field
                    break

    # Print the map
    for row in realm:
        print(" ".join(f"{cell:10s}" for cell in row))

    return realm

