// / Some good points in variable declaration 
/*
let age = 24;
console.log("Age : "+ age)
age = "99"
console.log("Age : "+ age)

The assingment age="99" will error because the initial assignment to the variable is a number and assigning a string to it will throw an error
*/

// Using the "any" type - This allows the variable to be assigned any type of data
// (Not really a practical use and a best practice - but then its there !! )

let age: any  = 24;
console.log("Age : "+ age)
age = "99"
console.log("Age : "+ age)

let newAge: string | number = 33
console.log("Datatype of the variable newAge is ", typeof(newAge))

newAge = "199"
console.log("Datatype of the variable newAge is ", typeof(newAge))
