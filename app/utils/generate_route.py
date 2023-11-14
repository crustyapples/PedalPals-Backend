import polyline

def decode_route_geometry(encoded_path):
    """
    Decodes a polyline encoded path to a list of lat-lng pairs.
    
    :param encoded_path: Encoded polyline string.
    :return: List of (latitude, longitude) tuples.
    """
    return polyline.decode(encoded_path)

# Example usage
encoded_path = '''wqyFkmzxRp@B^EMiBOs@S[k@m@u@Y{G_BcAc@mC{@oA]o@KSEaPcBkEi@_Ca@gBi@EDg@l@{@p@uArAO@S?MEWIwAu@_@Oo@[}@i@]AsBkAqCyAmBgAyAy@YQw@e@YSk@a@y@q@_@]i@g@oBuBsB`BqD|CaD|CIImB}A}BmBKI}CiCIIMM}@}@]_@c@c@{@_AkAuAmA_BsA_BGIIIaFwF_FqFTW'''  # Replace with your encoded path
decoded_path = decode_route_geometry(encoded_path)
coords = []

for lat, lng in decoded_path:
    coords.append(f"{lat},{lng}")
    print(f"{lat},{lng}")

command = '''xcrun simctl location "iPhone 14" start '''

print(command + ' '.join(coords))


