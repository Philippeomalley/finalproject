from productitem.models import Item


testArray = ["1 onion", "1 red pepper", "2 garlic cloves", "1 Tbsp oil", "1 heaped tsp hot chilli powder", "1 tsp paprika", "1 tsp ground cumin", "500g lean minced beef",
             "1 beef stock cube", "400g can chopped tomatoes", "½ tsp dried marjoram", "1 tsp sugar", "2 Tbsp tomato purée", "410g can red kidney beans", "long grain rice", "soured cream"]


def test_function():

    for item in Item.objects.all():
        print(item.product_name)
