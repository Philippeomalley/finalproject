const getRecipteBtn = document.querySelector(".getRecipe");
const window1 = document.querySelector(".window");

getRecipteBtn.addEventListener("click", () => {
 showRecipe();
});

function showRecipe() {
 var objective1 = recipe1.recipe_cost - recipe1.recipe_rating;
 var objective2 = recipe2.recipe_cost - recipe2.recipe_rating;
 var temp = recipe1;
 if (objective1 > objective2) {
  temp = recipe2;
 }
 document.getElementById('recipeName').innerHTML = temp.recipe_name;
 document.getElementById('recipeCost').innerHTML = "Cost: " + temp.recipe_cost;
 document.getElementById('recipeRating').innerHTML = "Rating: " + temp.recipe_rating;
 document.getElementById('recipeIngredients').appendChild(makeUL(temp.ingredients));
 window1.classList.add("showWindow");

}

function makeUL(array) {
 // Create the list element:
 var list = document.createElement('ul');

 for (var i = 0; i < array.length; i++) {
  // Create the list item:
  var item = document.createElement('li');

  // Set its contents:
  item.appendChild(document.createTextNode(array[i]));

  // Add it to the list:
  list.appendChild(item);
 }

 // Finally, return the constructed list:
 return list;
}

var recipe1 = {
 recipe_name: "Halloumi aubergine burgers with harissa relish",
 recipe_cost: "14.43",
 recipe_rating: "4.7",
 recipe_img: "",
 ingredients: ["2 ½ Tbsp olive oil", "2 onions", "0.5 aubergine", "250g halloumi cheese", "1 Tbsp soft brown sugar", "1 roasted red pepper", "2 tsp harissa", "4 ciabatta rolls", "4 Tbsp hummus"]
};

var recipe2 = {
 recipe_name: "Sweet potato cakes with poached eggs",
 recipe_cost: "21.46",
 recipe_rating: "3.89",
 recipe_img: "",
 ingredients: ["4 eggs", "100g harissa", "200g greek yogurt", "handful herbs", "500g sweet potato", "200g gluten-free flour", "1 pack parsley", "4 egg whites"]
};

