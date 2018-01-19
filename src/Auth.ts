import { Request, Response } from 'express';
import { JWT } from './JWT';
import { UserStore } from './UserStore';
import { Server } from './Server';
export interface AuthInput {
  username: string;
  password: string;
}
export interface AuthClaims {
  id: number;
  username: string;
  role: string;
  expires: number;
}
interface RefreshClaims {
  token: string;
  expiresIn: number;
}
export class Auth {
  private token: string;
  private claims: AuthClaims;
  constructor(private server: Server, private jwt: JWT, private userStore: UserStore) {

  }
  getUsername(): string {
    return this.claims.username;
  }
  async authenticated(authInput: AuthInput): Promise<boolean> {
    this.claims = await this.userStore.getAuthClaims(authInput);
    if (this.claims != null) {
      this.token = this.jwt.encode(this.claims);
      return true;
    } else {
      return false;
    }
  }

  static mapUserToAuthClaims(user: any): AuthClaims {
    const _min = 60; //expires every 60 mins
    return {
      id: user.id,
      username: user.username,
      role: user.role,
      expires: Date.now() + 1000 * 60 * _min
    }
  }

  //Express Middlware
  authenticationMiddleware(): void {
    const auth = this;
    this.server.router.use('/', function(req: Request, res: Response, next: any) {
      if (req.url === '/login' || req.url.includes('/setup')) {
        return next();
      } else {
        const token = req.headers['x-access-token'];
        try {
          const payload: any = auth.jwt.decode(token)[0];
          auth.claims = payload;
          if(auth.claims.expires < Date.now()) return res.status(401).send("Expired token");
          return next();
        } catch (e) {
          return res.status(401).send("Unauthorized");
        }
      }
    });
    this.loginRoute();
  }

  //Login route for express
  loginRoute(): void {
    this.server.router.post('/login', async (req: Request, res: Response) => {
      const authInput: AuthInput = req.body;
      const authenticated: boolean = await this.authenticated(authInput);
      if (authenticated) {
        res.json(this.getToken());
      } else {
        res.status(401).send("Unauthorized");
      }
    });
  }
  claimsRoutes(): void {
    const auth = this;
    this.server.router.get('/claims', async (req: Request, res: Response) => {
      if (!auth.isType("admin")) return res.status(401).send("Unauthorized");
      const claims: AuthClaims[] = await auth.userStore.selectAllUsers();
      return res.json(claims);
    });
    this.server.router.get('/claims/:user', async (req: Request, res: Response) => {
      if (!auth.isType("admin")) return res.status(401).send("Unauthorized");
      const user: AuthClaims = await auth.userStore.selectUser(req.params.user);
      if (user == null) return res.json({ success: false })
      return res.json(user);
    });
  }
  //Helper functions
  isType(_type: string): boolean {
    return this.claims.role == _type;
  }
  getToken(): any {
    return { token: this.token };
  }
  getRefreshClaims(token: string): RefreshClaims {
    return {
      token: token,
      expiresIn: 20
    }
  }
}
