const nextRecipteBtn = document.querySelector(".nextRecipe")
const prevRecipteBtn = document.querySelector(".prevRecipe")

const recipeImage = document.querySelector(".recipeImage")
const recipeName = document.querySelector(".recipeName")
const recipeIngredients = document.querySelector(".recipeIngredients")
const equivalentItems = document.querySelector(".equivalentItems")
const recipeRating = document.querySelector(".recipeRating")
const recipeCPS = document.querySelector(".recipeCPS")
const recipeTotal = document.querySelector(".recipeTotal")
const numServings = document.querySelector(".numServings")
const numRatings = document.querySelector(".numServings")
// recipeImage.innerHTML = "hello"
var i = 0;
displayRecipe();

// const window1 = document.querySelector(".window");


prevRecipteBtn.addEventListener("click", () => {
 if (i >= 0) {
  i--;
  console.log("here")
  displayRecipe()
 }
});

nextRecipteBtn.addEventListener("click", () => {
 if (i <= recipeList.length) {
  i++;
  console.log("here")
  displayRecipe()
 }
});

function displayRecipe() {
 recipeName.innerHTML = "<h2>" + recipeList[i]['recipe_name'] + "</h2>"
 recipeImage.innerHTML = "<img class='recipeImage' src=" + recipeList[i]['recipe_image'] + ">"
 recipeRating.innerHTML = "<h3>Rating " + recipeList[i]['recipe_rating'] + "/5 (" + recipeList[i]['recipe_numRatings'] + " ratings)</h3>"
 recipeCPS.innerHTML = "<h3>Cost per serving £" + recipeList[i]['cost_per_serving'] + "</h3>"
 numServings.innerHTML = "<h3>Serves " + recipeList[i]['recipe_NumServings'] + "</h3>"
 recipeTotal.innerHTML = "<h2>       £" + recipeList[i]['recipe_total'] + "</h2>"
 recipeIngredients.innerHTML = ingredientsList(recipeList[i]['ingredients']);
 equivalentItems.innerHTML = itemsList(recipeList[i]['ingredients'])
}

// function showRecipe() {
//  // var objective1 = recipe1.recipe_cost - recipe1.recipe_rating;
//  // var objective2 = recipe2.recipe_cost - recipe2.recipe_rating;
//  // var temp = recipe1;
//  // if (objective1 > objective2) {
//  //  temp = recipe2;
// }


// document.getElementById("recipe").innerHTML = recipeList[i]['recipe_title'];
// document.getElementBy('recipeCost').innerHTML = "Cost: " + temp.recipe_cost;
// document.getElementById('recipeRating').innerHTML = "Rating: " + temp.recipe_rating;
// document.getElementById('recipeIngredients').appendChild(makeUL(temp.ingredients));
// window1.classList.add("showWindow");



function ingredientsList(array) {
 // Create the list element:
 var list = document.createElement('ul');
 var fullList = "<ul>"
 for (var j = 0; j < array.length; j++) {
  var listItem = "<li><p>" + array[j]['ingredient_name'] + "</p></li>"
  fullList += listItem
 }
 fullList += "</ul>"
 return fullList;
}

function itemsList(array) {
 // Create the list element:
 var list = document.createElement('ul');
 var fullList = "<ul>"
 for (var j = 0; j < array.length; j++) {
  var listItem = "<li><p>" + array[j]['equivalent_product'] + "</p></li>"
  fullList += listItem
 }
 fullList += "</ul>"
 return fullList;
}

// var recipe1 = {
//  recipe_name: "Halloumi aubergine burgers with harissa relish",
//  recipe_cost: "14.43",
//  recipe_rating: "4.7",
//  recipe_img: "",
//  ingredients: ["2 ½ Tbsp olive oil", "2 onions", "0.5 aubergine", "250g halloumi cheese", "1 Tbsp soft brown sugar", "1 roasted red pepper", "2 tsp harissa", "4 ciabatta rolls", "4 Tbsp hummus"]
// };

// var recipe2 = {
//  recipe_name: "Sweet potato cakes with poached eggs",
//  recipe_cost: "21.46",
//  recipe_rating: "3.89",
//  recipe_img: "",
//  ingredients: ["4 eggs", "100g harissa", "200g greek yogurt", "handful herbs", "500g sweet potato", "200g gluten-free flour", "1 pack parsley", "4 egg whites"]
// };

