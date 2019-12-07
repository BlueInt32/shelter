export class LoginResult {
  public token: string;
  public expires: string;

  constructor() {
    this.token = '';
    this.expires = '';
  }
}
