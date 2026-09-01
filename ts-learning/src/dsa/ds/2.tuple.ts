/**
 * Tuple is a specific type of array where theorder of elements has a 
 * fixed relationship to their types. 
 * 
 * In TypeScript, tuples allow you to define an array with a fixed number 
 * of elements, where each element can have a different type.  
 * 
 */

let coordinate: [number, number] = [10, 20]; // A tuple representing a coordinate (x, y)

let person: [string, number] = ["Alice", 30]; // A tuple representing a person's name and age

// Accessing elements in a tuple
console.log(`Coordinate: (${coordinate[0]}, ${coordinate[1]})`);
console.log(`Person: Name - ${person[0]}, Age - ${person[1]}`);

// Tuples can also be used to represent more complex data structures
let employee: [string, number, boolean] = ["John Doe", 25, true]; // A tuple representing an employee's name, age, and employment status

console.log(`Employee: Name - ${employee[0]}, Age - ${employee[1]}, Employed - ${employee[2]}`);    

// Can I have a list of tuples? Yes, you can have an array of tuples. For example, an array of coordinates:
let coordinatesList: [number, number][] = [
    [10, 20],
    [30, 40],
    [50, 60]
];

console.log("List of Coordinates:");
coordinatesList.forEach((coord, index) => {
    console.log(`Coordinate ${index + 1}: (${coord[0]}, ${coord[1]})`);
});

// for loop to iterate over the coordinatesList
console.log('Using for loop to iterate over the coordinatesList:');
for (let i = 0; i < coordinatesList.length; i++) {
    console.log(`Coordinate ${i + 1}: (${coordinatesList[i][0]}, ${coordinatesList[i][1]})`);
}

// using tuple to represent a point in 3D space
let point3D: [number, number, number] = [1, 2, 3]; // A tuple representing a point in 3D space (x, y, z)

console.log(`Point in 3D Space: (${point3D[0]}, ${point3D[1]}, ${point3D[2]})`);    
