/**
 * LIteral Types allow variable, function parameters, and object properties 
 * to hold only specific values, improving type safety and preventing invalid
 * assignments. 
 *      - Restrict values to predefined litarls 
 *      - Improve code safety and code reliability 
 * Commonly used with union types to define valid values 
 */

// string literal types 

type Direction = "Up" | "Down" | "Left" | "Right";
let move: Direction;
move = "Up";
// move = "forward"
// Direction accepts only the values as defined 

// NUmeric LIteral Types - restricts a variable to s specific set of numeric values 

type Diceroll = 1 | 2 | 3 | 4 | 5 | 6

function rollDice(): Diceroll {
    return 4;
}
// return a value other than 1-6 will result in a compile time error 

// Boolean return types - restricts the variable or return value to either true or false 

type Success = true;
function operation(): Success {
    return true; // valied return value 
    // return false means it will error out
}
console.log(operation());
console.log();

/**
 * Union type to intersection type in typescript 
 */

// Union Type 
type Animal = "Dog" | "Cat" | "Bird"
// i.e. Animal can be Dog or Cat or Bird

// Intersection Type 
type Person = {name: string } & {age: number};
// here the person must contain both name and age properties

/** 
 * Using Distributive Conditional Types
 * 
 */

type UnionToIntersection<U> =
    (U extends unknown ? (arg: U) => void : never) extends
    (arg: infer I) => void
        ? I
        : never;

// Example usage
type UnionType = { a: number } | { b: string } | { c: boolean };

type IntersectionType = UnionToIntersection<UnionType>;

const myObject: IntersectionType = {
    a: 42,
    b: "hello",
    c: true
};

console.log(myObject);
console.log('----------------------00XIX00---------------------');

/**
 * Type Aliases - allow you to create reusable names for existing types, making complex type definitions easier to read and maintain
 * Type aliases do not create new types; they simply provide an alternative name for an existing type.
 */

type value = number | string | boolean;

// type value = number | string
let variable: value;

variable = 1;
console.log(variable);

variable = 'IAAIE';
console.log(variable)

variable = true 
console.log(variable);

variable = 4.2
console.log(variable);

// type alias in a function 

