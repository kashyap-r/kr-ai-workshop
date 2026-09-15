
### Abstract Classes in TypeScript 

An abstract class is a class that is meant to act as a base/template for other 
classes, but is not meant to be instantiated directly.

It can contain both:
    - Implementation methods: shared behaviour that all subclasses can reuse
    - abstract methods/properties: declarations that force subclass to provide their own implementation.

abstract class Animal {
    constructor(public name: string) {}

    // concrete method 
    eat(): void {
        console.log(`${this.name} is eating`);
    }

    // abstract method 
    abstract makeSound(): void;
}

class Dog extends Animal {
  makeSound(): void {
    console.log("Woof!");
  }
}

class Cat extends Animal {
  makeSound(): void {
    console.log("Meow!");
  }
}

const dog = new Dog("Bruno");

dog.eat();
dog.makeSound();

#### Why do we need abstract classes?
Suppose you are building a payment system. You know that every payment method 
must support: pay()

But paying by differnt metthods like Credit card, PayPal, UPI, Bank transfer
will obviously work differently. 
At the same time, maybe all payment types share common functionality such as: 
    - validateAmount()
    - logTransaction()
    - generateReceipt()

This is where an abstract class becomes useful.

abstract class PaymentProcessor{
    constructor(protected amount: number){}

    validateAmount(): boolean {
        return this.amount > 0;
    }

    abstract pay(): void;
}

Now indidividual payment processors must implement pay()
class CreditCardPayment extends PaymentProcessor {
  pay(): void {
    if (this.validateAmount()) {
      console.log(`Paying ₹${this.amount} using Credit Card`);
    }
  }
}

class UPIPayment extends PaymentProcessor {
  pay(): void {
    if (this.validateAmount()) {
      console.log(`Paying ₹${this.amount} using UPI`);
    }
  }
}

const creditCard = new CreditCardPayment(5000);
creditCard.pay();

const upi = new UPIPayment(2000);
upi.pay();