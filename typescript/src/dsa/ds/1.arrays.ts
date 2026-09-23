
// array of numbers 
let numbers:number[] = [1, 2, 3, 4, 5];

let var1 = "Kashyap";
let var2 = ['k', 'a', 's', 'h'];
let var3 = 12;
let var4 : string[] = ['a', 'b', 'c']

// console.log(typeof(var1));
// console.log(typeof(var2));
// console.log(typeof(var3));
// console.log(typeof(var4));

/** For var2 and var4,the output show as object because at runtime those are objects. 
 * However, in typescript the contents of var2 and var4 are string
string
object
number
object
 */
// Array Methods 
// TypeScript arrays have many built-in methods that can be used to manipulate the array elements. Some of the commonly used methods are:
// 1. push(): Adds one or more elements to the end of an array and returns the new length of the array.
// 2. pop(): Removes the last element from an array and returns that element.
// 3. shift(): Removes the first element from an array and returns that element.
// 4. unshift(): Adds one or more elements to the beginning of an array and returns the new length of the array.
// 5. splice(): Changes the contents of an array by removing or replacing existing elements and/or adding new elements in place.
// 6. slice(): Returns a shallow copy of a portion of an array into a new array object selected from start to end (end not included).
// 7. indexOf(): Returns the first index at which a given element can be found in the array, or -1 if it is not present.
// 8. includes(): Determines whether an array includes a certain value among its entries, returning true or false as appropriate.
// 9. forEach(): Executes a provided function once for each array element.
// 10. map(): Creates a new array populated with the results of calling a provided function on every element in the calling array.
// 11. filter(): Creates a new array with all elements that pass the test implemented by the provided function.
// 12. reduce(): Executes a reducer function (that you provide) on each element of the array, resulting in a single output value.   
// forEach() method: Iterates over each element in the array and executes a provided function for each element.
// find() method: Returns the value of the first element in the array that satisfies the provided testing function. If no values satisfy the testing function, undefined is returned.


let fruits: string[] = ["apple", "banana", "cherry", "dates", "elderberry"];

// console.log (fruits)
// console.log(fruits.length)

// for (let i=0; i < fruits.length; i++){
//     console.log(fruits[i]);
// }
// Push
let x = fruits.push("JackFruit", "Fig", "StrawBerry");
// console.log(x);
// console.log (fruits);
// Pop()
// let dfruit = fruits.pop();
// console.log("Deleted Fruit:", dfruit);  

// // shift - delete the element at the start
// let felement  = fruits.shift();
// console.log (typeof(felement));
// console.log (felement)
// fruits.unshift("Apricot");
// console.log (fruits);
// console.log(fruits.indexOf('Fig'));

// fruits.forEach((fruit, index) => {
//     console.log(`Index ${index}: ${fruit}`);
// });

// Itrating through an array 
// for (let i=0; i < fruits.length; i++){
//     for (let j=0; j<fruits[i].length; j++) {
//         console.log(fruits[i][j]);
//     }
//     console.log();
//     // console.log(`Fruit: ${fruits[i]}, Len: ${fruits[i].length}`);
// }

// Multi-Dimensional arrays 
let arr : number[][] = [
    [1, 2, 3], 
    [4, 5, 6],
    [7, 8, 9, 0]];


console.log("The no. of rows in the array:",arr.length); // gives the no. of rows
console.log(arr[0].length); // gives the no. of elements in the row
console.log(arr[1].length);
console.log(arr[2].length);

console.log()
