
// declaring an array 
let hobbies = ['sports', 'cooking', 'fishing', 'idling'];
hobbies.push('karting');

// declaring an array of strings
let vehicles: string[];



// flexible array 
let users: (string | number)[];
users = [1, "Mac"]
users = [5, 1]
users = ['Max', 'Emily']

//an array with generic data types / generic types 
let newUsers: Array<string | number>;

// the above mix of declarations are also true for the geenric types 

let possibleResults: number[];

possibleResults = [1, -1]
possibleResults = [5, 10, 12]

// -----------------------------------------------

let user1 = {
    name: 'max',
    age: 33
}


let user: {
    name: string;
    age: number;
} = {
    name: "Bond",
    age: 33
};

console.log(user.name || user.age)

// Get a bit creative and ...
let userRec: {
    name: string;
    age: number | string;
    hobbies: string[];
    role: {
        description: string;
        id: number
    }
} = {
    name: 'Bond',
    age: 33,
    hobbies: ['Sports', 'Religion'],
    role: {
        description: 'admin',
        id: 5
    }
}

/* 
to-do: 
How to assign and print values ?
Can this is a list of objects?
How to assign and print values looping thru?
*/

// the type {} does not mean an empty object 
let val: {} = 'some test';

// try to assign null to the above and it errors out, so the below statement means 
// any non-null undefined value is assigned to the "undefined" type 
let value:{} = {} 

// however, this is an empty object in typescript 
const someObj = {};

// in TYpescript object, you can have key value pairs, and the key can be a string or a number too
const someObject = {
    'name': 'Max',
    'age': 33
}

const someObject_1 = {
    0: 'Max',
    1: 33
}


// Flexible Objects with Record type

let data: Record<string, number | string>;

data = {
    entry1: 1,
    entry2: 'some string'
};

