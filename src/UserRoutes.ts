import { Request, Response, Router } from 'express';
import { Auth } from './Auth';
import { UserStore } from './UserStore';

export class UserRoutes {
  constructor(private router: Router, private auth: Auth, private userStore: UserStore) { }

  changePasswordAdminRoute(): void {
    this.router.post('/passwords/:user', async (req: Request, res: Response) => {
      if (!this.auth.isType("admin")) return res.status(401).send("Unauthorized");
      const msg = await this.userStore.changePassword(req.params.user, req.body.password);
      if (msg == null) {
        return res.json({ action: "changePasswordAdmin", success: false, message: "User does not exist: " + req.params.user });
      }
      return res.json({ action: "changePasswordAdmin", success: true, message: msg });
    });
  }
  changePassword(): void {
    this.router.post('/passwords/', async (req: Request, res: Response) => {
      const msg = await this.userStore.changePassword(this.auth.getUsername(), req.body.password);
      if (msg == null) {
        return res.json({ action: "changePassword", success: false, message: "User could not change their own password." });
      }
      return res.json({ action: "changePassword", success: true, message: msg });
    });
  }
  deleteUserRoute(): void {
    this.router.delete('/users/:username', async (req: Request, res: Response) => {
      if (!this.auth.isType("admin")) return res.status(401).send("Unauthorized");
      const msg = await this.userStore.deleteUser(req.params.username);
      if (msg == null) {
        return res.json({ action: "deleteUser", success: false, message: "User could not be deleted: " + req.params.username });
      }
      return res.json({ action: "deleteUser", success: true, message: msg });
    });
  }
  createUserRoute(): void {
    this.router.post('/users/:user', async (req: Request, res: Response) => {
      if (!this.auth.isType("admin")) return res.status(401).send("Unauthorized");
      const msg = await this.userStore.createUser(req.params.user, req.body.password, req.body.role);
      if (msg == null) {
        return res.json({ action: "createUser", success: false, message: "User already exists" });
      }
      return res.json({ success: true, message: msg });
    });
  }

  allRoutes(): void {
    this.changePasswordAdminRoute();
    this.changePassword();
    this.deleteUserRoute();
    this.createUserRoute();
  }
}
