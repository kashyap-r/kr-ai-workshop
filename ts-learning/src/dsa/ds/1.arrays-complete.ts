/**
 * Declaring an array in TypeScript can be done in two ways:
 * 1. Using square brackets [] after the type of the elements in the array.
 * 2. Using the Array<type> generic type.
 *
 * Example:
 * let numbers: number[] = [1, 2, 3];
 * let strings: Array<string> = ['a', 'b', 'c'];
 *
 * Both methods are equivalent and can be used interchangeably. 
 */
// array of numbers 
let numbers: number[] = [1, 2, 3];
console.log('Array of Numbers:', numbers);
console.log()
console.log("---------------------------------");

// array of strings 
let strings: Array<string> = ['a', 'b', 'c'];
console.log('Array of Strings:', strings);
console.log()
console.log("---------------------------------");

// generic array of any type
let anyArray: Array<any> = [1, 'a', true, { key: 'value' }];
console.log('Generic Array:', anyArray);
console.log()
console.log("---------------------------------");

// array of objects
interface Person {
    name: string;
    age: number;
}

let people: Person[] = [
    { name: 'Alice', age: 30 },
    { name: 'Bob', age: 25 }
];

console.log('Array of People:', people);
console.log()
console.log("---------------------------------");

// multi-dimensional array
let matrix: number[][] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

console.log('Matrix:', matrix);
console.log()
console.log("---------------------------------");

// Mixed type array
let mixedArray: (number | string | boolean)[] = [1, 'two', true, 4, 'five', false];
console.log('Mixed Type Array:', mixedArray);
console.log()
console.log("---------------------------------");

// Readonly array
let readonlyNumbers: ReadonlyArray<number> = [1, 2, 3];
console.log('Readonly Array:', readonlyNumbers);
console.log()
console.log("---------------------------------");

// Tuple type array
let tuple: [string, number] = ['age', 30];  
console.log('Tuple:', tuple);
console.log()
console.log("---------------------------------");   

// Accessing array elements
// Using index to access elements in the array
console.log('First Element of Numbers Array:', numbers[0]);
console.log('Second Element of Strings Array:', strings[1]);
console.log('First Person Name:', people[0].name);
console.log('Element in Matrix at (1, 2):', matrix[1][2]);
console.log('First Element of Mixed Array:', mixedArray[0]);
console.log('Tuple First Element:', tuple[0]);
console.log("---------------------------------");   
console.log()
// Modifying the array elements
// You can modify the elements of the array using their index
numbers[0] = 10;
strings[1] = 'd';
people[0].age = 31;
matrix[1][2] = 10;
mixedArray[0] = 5;
tuple[1] = 35;

console.log('Modified Numbers Array:', numbers);
console.log('Modified Strings Array:', strings);
console.log('Modified People Array:', people);
console.log('Modified Matrix:', matrix);
console.log('Modified Mixed Array:', mixedArray);
console.log('Modified Tuple:', tuple);     
console.log("---------------------------------");   
console.log()

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

let fruits: string[] = ['apple', 'banana', 'cherry', 'date', 'elderberry'];
// Using forEach() to iterate over the fruits array
console.log('Using forEach() to iterate over the fruits array:');
fruits.forEach((fruit, index) => {
    console.log(`Index ${index}: ${fruit}`);
});

console.log("---------------------------------");
console.log()

// just want to iterate using for loop to print the fruits array
console.log('Using for loop to iterate over the fruits array:');
for (let i = 0; i < fruits.length; i++) {
    console.log(`Index ${i}: ${fruits[i]}`);
}
console.log("---------------------------------");
console.log()    

// now let me iterate using find() method to find the first fruit that starts with the letter 'c'
let foundFruit = fruits.find(fruit => fruit.startsWith('c'));
console.log('First fruit that starts with the letter "c":', foundFruit);
console.log("---------------------------------");
console.log()

// now let me iterate using map() method to create a new array with the length of each fruit name
let fruitLengths = fruits.map(fruit => fruit.length);
console.log('Array of fruit name lengths:', fruitLengths);
console.log("---------------------------------");
console.log()

// now let me iterate using filter() method to create a new array with fruits that have more than 5 letters
let longFruits = fruits.filter(fruit => fruit.length > 5);
console.log('Array of fruits with more than 5 letters:', longFruits);
console.log("---------------------------------");
console.log()

// now let me iterate using reduce() method to get the total length of all fruit names combined
let totalLength = fruits.reduce((accumulator, fruit) => accumulator + fruit.length, 0);
console.log('Total length of all fruit names combined:', totalLength);
console.log("---------------------------------");

// now let me iterate using indexOf() method to find the index of 'cherry' in the fruits array
let cherryIndex = fruits.indexOf('cherry');
console.log('Index of "cherry" in the fruits array:', cherryIndex);
console.log("---------------------------------");

// now let me iterate using includes() method to check if 'banana' is in the fruits array
let hasBanana = fruits.includes('banana');
console.log('Does the fruits array include "banana"?', hasBanana);
console.log("---------------------------------");

// now let me iterate using slice() method to get a portion of the fruits array from index 1 to 3/  
let slicedFruits = fruits.slice(1, 4);
console.log('Sliced array (indices 1 to 3):', slicedFruits);
console.log("---------------------------------");   

// now let me iterate using splice() method to remove 2 elements starting from index 2 and add 'fig' and 'grape' in their place
let splicedFruits = fruits.splice(2, 2, 'fig', 'grape');
console.log('Spliced array (removed elements):', splicedFruits);
console.log('Fruits array after splicing:', fruits);
console.log("---------------------------------");   

// now let me iterate using push() method to add 'honeydew' to the end of the fruits array
fruits.push('honeydew');
console.log('Fruits array after pushing "honeydew":', fruits);
console.log("---------------------------------");

// now let me iterate using pop() method to remove the last element from the fruits array
let poppedFruit = fruits.pop();
console.log('Popped fruit:', poppedFruit);
console.log('Fruits array after popping:', fruits);
console.log("---------------------------------");

// now let me iterate using shift() method to remove the first element from the fruits array
let shiftedFruit = fruits.shift();
console.log('Shifted fruit:', shiftedFruit);
console.log('Fruits array after shifting:', fruits);
console.log("---------------------------------");

// now let me iterate using unshift() method to add 'kiwi' to the beginning of the fruits array
fruits.unshift('kiwi');
console.log('Fruits array after unshifting "kiwi":', fruits);
console.log("---------------------------------");   

// now let me iterate using reduceRight() method to get the total length of all fruit names combined, starting from the last element
let totalLengthRight = fruits.reduceRight((accumulator, fruit) => accumulator + fruit.length, 0);
console.log('Total length of all fruit names combined (using reduceRight):', totalLengthRight);
console.log("---------------------------------");   

// now let me iterate using every() method to check if all fruits have more than 3 letters
let allFruitsLongerThanThree = fruits.every(fruit => fruit.length > 3);
console.log('Do all fruits have more than 3 letters?', allFruitsLongerThanThree);
console.log("---------------------------------");   

// now let me iterate using some() method to check if at least one fruit has more than 5 letters
let someFruitsLongerThanFive = fruits.some(fruit => fruit.length > 5);
console.log('Is there at least one fruit with more than 5 letters?', someFruitsLongerThanFive);
console.log("---------------------------------");

// now let me iterate using findIndex() method to find the index of the first fruit that starts with the letter 'd'
let foundFruitIndex = fruits.findIndex(fruit => fruit.startsWith('d'));
console.log('Index of the first fruit that starts with the letter "d":', foundFruitIndex);
console.log("---------------------------------");

// now let me iterate using flat() method to flatten a multi-dimensional array of fruits
let multiDimensionalFruits: string[][] = [['apple', 'banana'], ['cherry', 'date'], ['elderberry']];
let flattenedFruits = multiDimensionalFruits.flat();
console.log('Flattened array of fruits:', flattenedFruits);
console.log("---------------------------------");

// now let me iterate using flatMap() method to create a new array by mapping each fruit to its length and flattening the result
let flatMappedFruits = fruits.flatMap(fruit => [fruit, fruit.length]);
console.log('FlatMapped array of fruits and their lengths:', flatMappedFruits);
console.log("---------------------------------");   

// now let me iterate using reverse() method to reverse the order of the fruits array
fruits.reverse();
console.log('Fruits array after reversing:', fruits);
console.log("---------------------------------");

// now let me iterate using sort() method to sort the fruits array in alphabetical order
fruits.sort();
console.log('Fruits array after sorting:', fruits);
console.log("---------------------------------");

// now let me iterate using join() method to join all the fruits in the array into a single string, separated by commas
let joinedFruits = fruits.join(', ');
console.log('Joined fruits string:', joinedFruits);
console.log("---------------------------------");

// now let me iterate using toString() method to convert the fruits array into a string
let fruitsString = fruits.toString();
console.log('Fruits array as string:', fruitsString);
console.log("---------------------------------");

// now let me iterate using fill() method to fill the fruits array with 'mango' from index 1 to 3
fruits.fill('mango', 1, 4);
console.log('Fruits array after filling with "mango" from index 1 to 3:', fruits);
console.log("---------------------------------");

// now let me iterate using copyWithin() method to copy the elements from index 0 to 2 and paste them starting at index 3
fruits.copyWithin(3, 0, 3);
console.log('Fruits array after copyWithin from index 0 to 2 to index 3:', fruits);
console.log("---------------------------------");

// now let me iterate using keys() method to get an iterator for the keys (indices) of the fruits array
let keysIterator = fruits.keys();
console.log('Keys (indices) of the fruits array:');
for (let key of keysIterator) {
    console.log(key);
}

// now let me iterate using values() method to get an iterator for the values of the fruits array
let valuesIterator = fruits.values();
console.log('Values of the fruits array:');
for (let value of valuesIterator) {
    console.log(value);
}   

// now let me iterate using entries() method to get an iterator for the key/value pairs of the fruits array
let entriesIterator = fruits.entries();
console.log('Entries (key/value pairs) of the fruits array:');
for (let entry of entriesIterator) {
    console.log(entry);
}

// now let me iterate using Array.from() method to create a new array from the fruits array
let newFruitsArray = Array.from(fruits);
console.log('New array created from the fruits array using Array.from():', newFruitsArray);
console.log("---------------------------------");   

// now let me iterate using Array.isArray() method to check if the fruits variable is an array
let isArray = Array.isArray(fruits);
console.log('Is the fruits variable an array?', isArray);
console.log("---------------------------------");

// now let me iterate using Array.of() method to create a new array with the given elements
let arrayOfFruits = Array.of('kiwi', 'lemon', 'mango');
console.log('New array created using Array.of():', arrayOfFruits);
console.log("---------------------------------");

