interface Authenticatable {
  email: string;
  password: string;

  login(): void;
  logout(): void;
}

interface AuthenticatableAdmin extends Authenticatable {
  role: 'admin' | 'superadmin';
}

class AuthenticatableUser implements Authenticatable {
  constructor(
    public userName: string,
    public email: string,
    public password: string
  ) {}

  login() {
    // ...
  }

  logout() {
    // ...
  }
}

// ...

function authenticate(user: Authenticatable) {
  user.login();
}

// type Authenticatable = {
//   role: string;
// }

let user: Authenticatable;

user = {
  email: 'test@example.com',
  password: 'abc1',
  login() {
    // reach out to a database, check credentials, create a session
  },
  logout() {
    // clear the session
  },
};
