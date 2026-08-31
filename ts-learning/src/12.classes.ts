// class User{
//     name: string;
//     age: number;

//     constructor(name: string, age: number){
//         this.name = name;
//         this.age = age
//     }
// }

// is this correct ?
// class User{
//     constructor(public name: string, public age: number){
//         this.name = name;
//         this.age = age
//     }
// }

class User{
    constructor(public name: string, public age: number) {
    }
}

const max = new User('Max', 36);
const fred = new User('Fred', 34);
console.log(max, fred);

max.age = 55

console.log (max.age);