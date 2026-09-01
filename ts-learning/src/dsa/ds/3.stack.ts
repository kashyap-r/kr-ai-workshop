/**
 * Stack is a linear data structure that follows the Last In First Out (LIFO) principle.
 * This means the last element added to the stack will be the first one to be removed.  
 * 
 * Basic Operations of a stack include:
 * 1. Push: Add an element to the top of the stack.
 * 2. Pop: Remove the top element from the stack.
 * 3. Peek/Top: Retrieve the top element without removing it.
 * 4. isEmpty: Check if the stack is empty.
 * 5. Size: Get the number of elements in the stack.    
 * 
 * In TypeScript, we can implement a stack using an array or a linked list.
 * 
 */

// Implementing a stack using an array in TypeScript
//

class Stack<T> {
    private items: T[] = [];

    // Push an element onto the stack
    push(element: T): void {
        this.items.push(element);
    }

    // Pop an element off the stack
    pop(): T | undefined {
        return this.items.pop();
    }

    // Peek at the top element of the stack
    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    // Check if the stack is empty
    isEmpty(): boolean {
        return this.items.length === 0;
    }

    // Get the size of the stack
    size(): number {
        return this.items.length;
    }

    // Clear the stack
    clear(): void {
        this.items = [];
    }
}

// Example usage of the Stack class
const numberStack = new Stack<number>();
numberStack.push(10);
numberStack.push(20);
numberStack.push(30);

console.log("Top element:", numberStack.peek()); // Output: Top element: 30
console.log("Stack size:", numberStack.size()); // Output: Stack size: 3

console.log("Popped element:", numberStack.pop()); // Output: Popped element: 30
console.log("Stack size after pop:", numberStack.size()); // Output: Stack size after pop: 2

console.log("Is stack empty?", numberStack.isEmpty()); // Output: Is stack empty? false

numberStack.clear();
console.log("Stack size after clear:", numberStack.size()); // Output: Stack size after clear: 0        

// Other implementations of stack can be done using linked list, but for simplicity, we are using array here.
// without using generics, we can implement a stack for specific types like number or string, but using generics allows us to create a stack that can hold any type of data.

class GenericStack {
    items: any[] = []; // can hold any type of data

    push(element: any): void{
        this .items.push(element);
    }

    pop(): any {
        return this.items.pop();
    }
}

const stack = new GenericStack();
stack.push(10);
stack.push("Hello");
stack.push({name: "Alice", age: 30});

console.log(stack.pop()); // Output: { name: 'Alice', age: 30 }
console.log(stack.pop()); // Output: Hello
console.log(stack.pop()); // Output: 10

// just want to create a number stack and a string stack using the GenericStack class
const numberStack2 = new GenericStack();
numberStack2.push(1);
numberStack2.push(2);
numberStack2.push(3);

console.log(numberStack2.pop()); // Output: 3
console.log(numberStack2.pop()); // Output: 2
console.log(numberStack2.pop()); // Output: 1

const stringStack = new GenericStack();
stringStack.push("A");
stringStack.push("B");
stringStack.push("C");

console.log(stringStack.pop()); // Output: C
console.log(stringStack.pop()); // Output: B
console.log(stringStack.pop()); // Output: A    

// iterating over the numberStack2 and stringStack using for loop
console.log('Iterating over numberStack2:');
for (let i = 0; i < numberStack2.items.length; i++) {
    console.log(numberStack2.items[i]);
}

console.log('Iterating over stringStack:');
for (let i = 0; i < stringStack.items.length; i++) {
    console.log(stringStack.items[i]);
}   

//now let me implement a stack using linked list in TypeScript
class Node<T> {
    value: T;
    next: Node<T> | null = null;

    constructor(value: T) {
        this.value = value;
    }
}

class LinkedListStack<T> {
    private head: Node<T> | null = null;
    private length: number = 0;

    push(value: T): void {
        const newNode = new Node(value);
        if (this.head === null) {
            this.head = newNode;
        } else {
            newNode.next = this.head;
            this.head = newNode;
        }
        this.length++;
    }

    pop(): T | undefined {
        if (this.head === null) return undefined;
        const poppedValue = this.head.value;
        this.head = this.head.next;
        this.length--;
        return poppedValue;
    }

    peek(): T | undefined {
        return this.head ? this.head.value : undefined;
    }

    isEmpty(): boolean {
        return this.length === 0;
    }

    size(): number {
        return this.length;
    }
}

// Example usage of the LinkedListStack class
const linkedListStack = new LinkedListStack<number>();
linkedListStack.push(10);
linkedListStack.push(20);
linkedListStack.push(30);

console.log("Top element (Linked List Stack):", linkedListStack.peek()); // Output: Top element (Linked List Stack): 30
console.log("Stack size (Linked List Stack):", linkedListStack.size()); // Output: Stack size (Linked List Stack): 3

console.log("Popped element (Linked List Stack):", linkedListStack.pop()); // Output: Popped element (Linked List Stack): 30
console.log("Stack size after pop (Linked List Stack):", linkedListStack.size()); // Output: Stack size after pop (Linked List Stack): 2

console.log("Is stack empty? (Linked List Stack)", linkedListStack.isEmpty()); // Output: Is stack empty? (Linked List Stack) false         




