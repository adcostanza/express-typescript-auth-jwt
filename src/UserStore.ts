import { DB } from './DB';
import { AuthClaims, AuthInput, Auth } from './Auth';
const passwordHash = require('password-hash');

export class UserStore {
  constructor(private db: DB) {
  }
  async setupDB(): Promise<string> {
    //let query = 'CREATE TABLE Users (id SERIAL PRIMARY KEY, username VARCHAR, password VARCHAR, role VARCHAR)';
    //const tables = await this.db.queryRows(query);
    const query = 'INSERT INTO Users (username, password, role) VALUES ($1, $2, $3)'
    const hashedPassword = passwordHash.generate(process.env.pw);
    const values = [process.env.user, hashedPassword, "admin"];
    const status = await this.db.query(query, values);
    console.log("Initial user created")
    return status == null ? null : "User created: " + process.env.user;
  }
  async createUser(username: string, password: string, role: string): Promise<string> {
    const exists = await this.selectUser(username) == null ? false : true;
    if (!exists) {
      const query = 'INSERT INTO Users (username, password, role) VALUES ($1, $2, $3)'
      const hashedPassword = passwordHash.generate(password);
      const values = [username, hashedPassword, role];
      const status = await this.db.query(query, values);
      return status == null ? null : "User created: " + username;
    } else {
     return null;
    }
  }
  async deleteUser(username: string): Promise<string> {
    const query = 'DELETE FROM Users WHERE username=$1'
    const values = [username];
    const status = await this.db.query(query, values);
    return status == null ? null : "User deleted: " + username;
  }
  async changePassword(username: string, password: string): Promise<string> {
    const query = 'UPDATE Users SET password=$1 WHERE username=$2';
    const hashedPassword = passwordHash.generate(password);
    const values = [hashedPassword, username];
    const status = await this.db.query(query, values);
    return status == null ? null : "User password changed: " + username;
  }
  async selectAllUsers(): Promise<AuthClaims[]> {
    const query = "SELECT * FROM Users";
    const res = await this.db.queryRows(query);
    if (res == null) return res;
    return res.map((user: any) => {
      Auth.mapUserToAuthClaims(user);
    });
  }
  async selectUser(_username: string): Promise<AuthClaims> {
    const query = "SELECT * FROM Users where username=$1";
    const res = await this.db.queryRows(query, [_username]);
    if (res.length <= 0) return null;
    return res.map((user: any) => {
      return Auth.mapUserToAuthClaims(user);
    })
  }
  async getAuthClaims(authInput: AuthInput): Promise<AuthClaims> {
    const query = "SELECT * FROM users where username=$1 ORDER BY id DESC"
    const res = await this.db.queryRows(query, [authInput.username]);
    if (res == null) {
      return null;
    }
    try {
      const user = res[0];
      if (!passwordHash.verify(authInput.password, user.password)) return null;
      return res.map((user: any) => {
        return Auth.mapUserToAuthClaims(user);
      })
    } catch (e) { }
  }
}
