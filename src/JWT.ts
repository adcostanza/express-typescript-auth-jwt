const jwt = require('jwt-simple');
export class JWT {
  secret: string;
  constructor() {
    this.secret = process.env.secret
  }
  encode(payload:any): string {
    return jwt.encode(payload,this.secret);
  }
  decode(payload:any): string {
    return jwt.decode(payload,this.secret);
  }
}
