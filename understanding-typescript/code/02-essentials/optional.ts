function generateError(msg?: string) {
  throw new Error(msg);
}

generateError();

type User = {
  name: string;
  age: number;
  role?: 'admin' | 'guest'
};

let input = '';
const didProvideInput = input ?? false;
