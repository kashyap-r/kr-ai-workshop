// enum Role {
//   Admin,
//   Editor,
//   Guest,
// }

// type MyNumber = number;
type Role = 'admin' | 'editor' | 'guest' | 'reader';
type User = {
  name: string;
  age: number;
  role: Role;
  permissions: string[];
};

let userRole: Role = 'admin';

// ...

userRole = 'guest';

let possibleResults: [1 | -1, 1 | -1]; // [1, -1]

possibleResults = [1, -1];

function access(role: Role) {
  // ...
}