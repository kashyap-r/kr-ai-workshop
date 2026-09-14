
// a 1-dimensional array 
const arr1D: number[] = [12, 45, 7, 32, 23];
console.log(arr1D);
// FInd the largest element in a 1-D Array 
let max1D: number = Math.max(...arr1D);
console.log("The largest element: ", max1D);

let arr2D: number[][] = [
    [1, 3, 5], 
    [12, 32, 52],
    [9, 19, 29]
];

// console.log(arr2D);
for (let i=0; i< arr2D.length; i++) {
    console.log(arr2D[i]);
}
// Find the largest element in a 2D array 
const max2D = Math.max(...arr2D.flat());
console.log(`The largest element: ${max2D}`);

type Matrix = number[][];

class MatrixMath {
    // ➕ ADDITION
    static add(A: Matrix, B: Matrix): Matrix {
        return A.map((row, i) => row.map((val, j) => val + B[i][j]));
    }

    // ➖ SUBTRACTION
    static subtract(A: Matrix, B: Matrix): Matrix {
        return A.map((row, i) => row.map((val, j) => val - B[i][j]));
    }

    // ✖️ STANDARD MATRIX MULTIPLICATION (Row x Column)
    static multiply(A: Matrix, B: Matrix): Matrix {
        const rowsA = A.length, colsA = A[0].length;
        const colsB = B[0].length;
        
        // Initialize an empty result matrix with zeros
        const result: Matrix = Array.from({ length: rowsA }, () => Array(colsB).fill(0));

        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsB; j++) {
                for (let k = 0; k < colsA; k++) {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return result;
    }

    // ➗ ELEMENT-WISE DIVISION 
    static divideElementWise(A: Matrix, B: Matrix): Matrix {
        return A.map((row, i) => row.map((val, j) => {
            if (B[i][j] === 0) throw new Error("Division by zero encountered!");
            return val / B[i][j];
        }));
    }
}

function printMatrix(matrix: Matrix): void {
    matrix.forEach(row => {
        // Map each number to a string and pad it so columns line up perfectly
        const formattedRow = row.map(num => num.toString().padStart(3, ' ')).join(' ');
        console.log(`[ ${formattedRow} ]`);
    });
}

const matrixA: Matrix = [
    [1, 2],
    [3, 4]
];

const matrixB: Matrix = [
    [5, 6],
    [7, 8]
];

console.log("Matrix A:");
printMatrix(matrixA);

console.log("\nMatrix B:");
printMatrix(matrixB);

console.log("\n--- Addition (A + B) ---");
printMatrix(MatrixMath.add(matrixA, matrixB));

console.log("\n--- Subtraction (A - B) ---");
printMatrix(MatrixMath.subtract(matrixA, matrixB));

console.log("\n--- Standard Multiplication (A × B) ---");
printMatrix(MatrixMath.multiply(matrixA, matrixB));

console.log("\n--- Element-wise Division (A ÷ B) ---");
printMatrix(MatrixMath.divideElementWise(matrixA, matrixB));

// Now do it manually 
// To perform these operations, let Matrix A and Matrix B be 
// two-dimensional grids of numbers, where A{i,j} represents the 
// element located at row (i) and column (j).
// Addition of 2 Matrices
// C[i, j] = A[i, j] + B[i, j]
// Matrix Subtraction (A-B),  C(i, J) = A[i, j] + B[i, j]
// Matrix Multiplication - 
// Dimension Rule: Matrix (A) must have dimensions m * n, 
// and Matrix (B) must have dimensions n * p. 
// C(i, j) = Summation of A(i, k) * B (k, j) for k=1 to n 


