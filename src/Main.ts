import { Server } from './Server';
import { Request, Response } from 'express';
let server: Server = new Server('/api');

server.routes();
server.router.get('/example'), async (req: Request, res: Response) => {
  return res.json({ example: "hello" });
}
server.start();
