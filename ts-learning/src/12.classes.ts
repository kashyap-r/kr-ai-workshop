/**
 * In Typescript 
 */
// class User{
//     name: string;
//     age: number;

//     constructor(name: string, age: number){
//         this.name = name;
//         this.age = age
//     }
// }
// class User{
//     name: string;
//     age: number;

//     constructor(n: string, a: number){
//         this.name = n;
//         this.age = a
//     }
// }



// easier way to write the above code is...
class User{
    constructor(public name: string, public age: number) {
    }
}

// the public keyword means that the properties are automatically 
// created and assigned in the constructor, so you don't need to 
// explicitly declare them or assign them.
// Their scope is public, so they can be accessed from outside the class.
// if you want to make them private, you can use the private keyword 
// instead of public. The scope of private properties is limited to
// the class itself, so they cannot be accessed from outside the 
// class.

const max = new User('Max', 36);
const fred = new User('Fred', 34);
console.log(max, fred);

max.age = 55
console.log (max.age);

// is this correct ?
// class User{
//     constructor(public name: string, public age: number){
//         this.name = name;
//         this.age = age
//     }
// }

console.log("-------------------");

// marking class prperties as readonly means that they can only be 
// assigned a value once, either in the constructor or at the point
//  of declaration. After that, they cannot be changed. 
// This is useful for properties that should not be modified after 
// the object is created.

class User2{
    readonly hobbies: string[];
    constructor(public name: string, public age: number, hobbies: string[]){
        this.hobbies = hobbies;
    }
}

const max2 = new User2('Max', 36, ['Sports']);
console.log(max2.hobbies);

// max2.hobbies = ['Cooking']; // Error: Cannot assign to 'hobbies' because it is a read-only property. 

max2.hobbies.push('Cooking'); // This is allowed because we are modifying the contents of the array, not reassigning the property itself.
console.log(max2.hobbies);




