class User {
  protected _firstName: string = '';
  private _lastName: string = '';

  set firstName(name: string) {
    if (name.trim() === '') {
      throw new Error('Invalid name.');
    }
    this._firstName = name;
  }

  set lastName(name: string) {
    if (name.trim() === '') {
      throw new Error('Invalid name.');
    }
    this._lastName = name;
  }

  get fullName() {
    return this._firstName + ' ' + this._lastName;
  }

  static eid = 'USER';

  static greet() {
    console.log('Hello!');
  }
}

console.log(User.eid);
User.greet();

const max = new User();
max.firstName = 'Max';
max.lastName = '';
// max._firstName = 'Max 2';
console.log(max.fullName);

class Employee extends User {
  constructor(public jobTitle: string) {
    super();
    // super.firstName = 'Max';
  }

  work() {
    // ...
    console.log(this._firstName);
    // super._firstName
  }
}

abstract class UIElement {
  constructor(public identifier: string) {}

  clone(targetLocation: string) {
    // logic to duplicate the UI element
  }
}

// let uiElement = new UIElement();

class SideDrawerElement extends UIElement {
  constructor(public identifier: string, public position: 'left' | 'right') {
    super(identifier);
  }

  // ...
}
