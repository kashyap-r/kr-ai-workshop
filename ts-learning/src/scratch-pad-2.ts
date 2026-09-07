/* 
Arrays 
    - stores elements of the same type
    - are in contiguous memory locations 
    - supports index-based access 
    - array name represents starting address 

*/
// Declaring Arrays in Type Script
// Using square brackets 
console.log();
console.log("----------------------===Arrays demo===------------------------");

let marks: number[] = []; // empty array initialized 
let studentMarks: number[] = [91, 93, 99, 97];
let fruits : string[] = ['Apple', 'Banana', 'Cherry'];

console.log (studentMarks[0]);
console.log("The fruits I have are...")
for (let i=0; i<3; i++){
    console.log(fruits[i]);
}

console.log();
console.log("----------------------===Arrays using generic array type===------------------------");
// Using Generic Array Type

let veggies: (string | number)[] = ['Carrots', 21, 'Tomatoes', 5, 6, 'Coriander'];
let flowers: Array<string> = ['Rose', 'Hibiscus', 'Lotus', 'lillies', 'Daisy', 'Sunflower', 'Jasmine'];

console.log(veggies);
console.log(flowers[1]);
console.log(flowers[4]);

for (let index in flowers) {
    console.log(flowers[index]);
}

for (let i=0; i<veggies.length; i++){
    console.log(veggies[i]);
}

console.log();
console.log("----------------------===Types of Array - 1D, 2D, 3D===------------------------");
// Types of array
// Single Dimensional Array 
let arr: number[];
arr = [1, 2, 3, 4, 5];
for (let index in arr){
    console.log(arr[index]);
}


// multi-dimensional array 
let matrix: number[][] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
console.log(matrix);

// for (let i = 0; i)

