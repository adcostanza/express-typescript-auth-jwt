const express: any = require('express');
import { Request, Response, NextFunction, Router } from 'express';   // call express
// define our app using express
const bodyParser: any = require('body-parser');
const morgan = require('morgan'); //log requests to console

import { JWT } from './JWT';
import { AuthInput, Auth } from './Auth';
import { UserStore } from './UserStore';
import { DB } from './DB';
import { UserRoutes } from './UserRoutes';

export class Server {
  private app: any = express();
  private port = process.env.PORT || 8080;
  public router: Router = express.Router();
  private base: string;
  private jwt: JWT = new JWT();
  private db: DB = new DB();
  private userStore: UserStore = new UserStore(this.db);
  private auth: Auth = new Auth(this, this.jwt, this.userStore);
  private userRoutes: UserRoutes = new UserRoutes(this.router, this.auth, this.userStore);
  constructor(base: string) {
    this.base = base;
    this.app.use(bodyParser.urlencoded({ extended: true }));
    this.app.use(bodyParser.json());
    this.app.use(morgan('dev')); // record requests to console
  }

  setupRoute(): void {
    this.router.get('/setup/:key', async (req: Request, res: Response) => {
      //if (!this.auth.isType("admin")) return res.status(401).send("Unauthorized");
      if (req.params.key != "09809asdf09dfadsf3") return res.json({ action: "setup", success: false, message: "Wrong key" });
      const msg = await this.userStore.setupDB();
      if (msg == null) {
        return res.json({ action: "setup", success: false, message: msg })
      }
      return res.json({ action: "setup", success: true, message: msg });
    });
  }


  routes(): void {
    this.auth.authenticationMiddleware();
    this.setupRoute();
    this.auth.claimsRoutes();
    this.userRoutes.allRoutes();
    this.router.use(async (req: Request, res: Response, next: NextFunction) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS');
      next();
    });
  }

  start(): void {
    this.app.use(this.base, this.router);
    this.app.listen(this.port);
    console.log('Magic happens on port ' + this.port);
  }
}
