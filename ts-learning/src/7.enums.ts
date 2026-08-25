/**
 * Enums 
 * Allows you to define a set of named constants, make your code readable maintainable and easier to understand
 * Three types 
 * 1. Numeric Enums 
 * 2. String Enums 
 * 3. Heterogeneous Enums
 * 4. Const Enums
 */
// Numeric enums 
// The first member up is assinged value 0 by default and each subsequent member is incremented by 1

enum Direction {
    up, 
    down,
    left, 
    right
}
let move: Direction = Direction.up;
console.log(move)
console.log(Direction.down)

// initialized numeric enums
enum myDirection {
    up = 1,
    down
}
let myMove : myDirection = myDirection.down
console.log(myMove)
console.log(myDirection.up)

// fully initialized numeric enums 
enum NEWS {
    north = 1,
    east = 2,
    west = 3,
    south = 4
}

// string enums
enum News{
    North = 'N',
    East = 'E',
    West = 'W',
    South = 'S'
}

// Hetereogenous enums 
enum Status {
    Active = 1,
    Inactive = 'INACTIVE',
    Pending = 2,
    Cancelled = 'Cancelled'
}

// const enums 
// the values are inlined during compilation 
// no enum object is generated in compiled javascript, reduced code and improves performance
const enum Directions {
    Up, 
    Down, 
    Left, 
    Right 
}

