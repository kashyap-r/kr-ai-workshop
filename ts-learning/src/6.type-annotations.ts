/**
 * Type Annotations 
 * - Explicitly specify the type of variables, function parameters, return values, and object protperties, improving type safety and code readability.
 *      - Define the expected data type explicitly
 *      - Detect type-related errors during development 
 *      - Improve code readability 
 */
// where can type annotations be used?
// variables, functions, objects, arrays, classes 
// In variables 
const str: string = 'typescript_rocks'
const num: number = 8
const arr: (string | number)[] = ['Hi', 'TypeScript', 500]

console.log(typeof(str))
console.log(typeof  num)
console.log(arr)


//Function type annotations define the types of parameters and the return value.
function greet(name: string): string {
    return `Hello, ${name}!`;
}
console.log(greet("Bond"));

// Object type annotations define the required properties and their types 
// {name: string, age:number}  is the typescript type definition stating this 
// object must have exactly a text/ string name and a number age
// {name: "James bond", age: 40 } is the actaul object containing the data
const person: {name: string, age:number} = {
    name: "James Bond",
    age: 40
};
console.log(person);


// Arrays - array type annotations specify the type of elements an array can contain 

const numbers: number[] = [1, 2, 3, 4, 5];
console.log(numbers)

// classes 
// type annotations can be applied to class properties, constructor parameters, and method return types, 

class Rectangle {
    width: number;
    height: number;

    constructor(width: number, height: number){
        this.width = width;
        this.height = height;
    }

    area(): number {
        return this.width * this.height
    }
}

const rect = new Rectangle(5, 10);
console.log('Am here now!!')
console.log(rect)
console.log(`The sides of the rectangle: width: ${rect.width}, height: ${rect.height}`)
console.log(rect.area)
console.log(`The area of the rectangle: ${rect.area()}`)


class newRectangle {
    width: number;
    height: number;

    constructor(width: number, height: number){
        this.width = width;
        this.height = height;
    }

    // note I have added get here
    get area(): number {
        return this.width * this.height
    }
}

const rectOne = new newRectangle(5, 10);
console.log('Am here now!!')
console.log(rectOne)
console.log(`The sides of the new rectangle: width: ${rectOne.width}, height: ${rectOne.height}`)
console.log(rectOne.area)
// you dont need to add paranthesis for a function call
//console.log(`The area of the rectangle: ${rectOne.area()}`)

/**
 * Type Inference: allows TypeScript to automatically determine the type of variables, function return values, objects, and arrays based on their assigned values, reducing the need for explicit type annotations
 */
// inference of variable type
let age = 25;
let uName = 'Bond';

console.log(`Variable type of age: ${typeof age}`)
console.log(`Variable type oof age: ${typeof uName}`)
console.log(`Name: ${uName}, age: ${age}`)

// inference of array type 
let fruits = ["Appple", "Banana", "Cherry"]
console.log(fruits)
console.log(`Array type: ${typeof fruits}`)

// Inference of function return type
function add(a: number, b: number) {
    return a+b
}
console.log(typeof add(2, 12))

// Inference of Object type 
let heperson = {
    name: "James Bond",
    age: 44
}
console.log(typeof(heperson))
console.log(heperson)
console.log(heperson.name)
