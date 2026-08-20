
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


