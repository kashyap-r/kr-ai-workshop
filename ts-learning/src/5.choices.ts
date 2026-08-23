
// working with enums - is Typescript specific feature, not javascript

// to have a list of choices 

enum Role {
    Admin, 
    Editor, 
    Guest
}

let userRole: Role = Role.Admin

// check out the javascript code to understand how it is implemented
//u'll understand how the below works 
let userRole1: Role = 0 

// this errors out
// let userRole4: Role = 4 


enum newRole {
    Admin = 1, 
    Editor = 2, 
    Guest = 3
}

//Literal types 
let anotherUserRole: 'admin' | 'editor' | 'guest' =  'admin';

anotherUserRole = 'guest'

/**
 * to-do: 
 * 1. find out how this is applied in real-world situations
 * 2. combine literal types with union types
 */

let possibleResults: [1 | -1, 1 | -1];

possibleResults = [1, -1]


