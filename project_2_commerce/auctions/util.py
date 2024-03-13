placeholder_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/1022px-Placeholder_view_vector.svg.png"

no_category = ['N/A']

def parse_categories(categories_string: str):

  if (categories_string is None):
    return None
  
  return categories_string.split(" ")
