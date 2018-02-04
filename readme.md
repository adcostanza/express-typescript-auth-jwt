## A Boilerplate Authentication API in TypeScript/Express
Boilerplate code for JWT authentication for a TypeScript Express JSON API delivered over HTTP.

### Purpose
The purpose of this TypeScript module is to make it easy to set up a new authenticated Express API without having to write all the code that allows user login, authentication, JWT handling, changing passwords, etc. There are many ways this could be done, so feel free to modify what I have done here to suit your needs.

## Instructions
Import the utility like this:

See `main.ts` for an example implementation, repeated below:

    import { Server } from './Server';
    let server: Server = new Server('/api');

    server.routes(); //adds all of the user/auth routes
    server.router.get('/example'), async (req: Request, res: Response) => {
      return res.json({ example: "hello" });
    }
    server.start();

The route above is automatically protected by the auth API. You may also check authorization by typing the following into your async router function:

```
if (!auth.isType("admin")) return res.status(401).send("Unauthorized");
```

## Built in Routes
### Setup route
**PURPOSE** Set up first user defined in dockerfile in Database as admin.

**ROUTE** `POST /setup/:key`

The key for setting up the first user can be found and defined inline the setupRoute of Server.ts (09809asdf09dfadsf3 by default):

```
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
  ```
---

### Auth Related

**PURPOSE** Login

**ROUTE** `POST /login`

**POST DATA**
```
{
  username: string;
  password: string;
}

```

**RETURNS** `success:boolean`

**AUTH** none

---

**PURPOSE** Lookup current users and admins, get roles

**ROUTE** `GET /claims/:user`

**RETURNS**
```
{
  id: number;
  username: string;
  role: string;
  expires: number;
}
```

**AUTH** admin

---
**PURPOSE** Get your own auth claims / roles

**ROUTE** `GET /claims`

**RETURNS** all users AuthClaims

**AUTH** admin

---

### Users

**PURPOSE** Change user password as Admin

**ROUTE** `POST /passwords/:user`

**POST DATA**
`password:string`

**RETURNS** `success:boolean`

**AUTH** admin

---

**PURPOSE** Allow a user to change their own password

**ROUTE** `POST /passwords`

**POST DATA**
`password:string`

**RETURNS** `success:boolean`

**AUTH** none

---

**PURPOSE** Delete user as admin

**ROUTE** `DELETE /users/:user`

**RETURNS** `success:boolean`

**AUTH** admin

---

**PURPOSE** Create user as admin

**ROUTE** `POST /users/:user`

**POST DATA**
`password:string`

**RETURNS** `success:boolean`

**AUTH** admin

## First time setup

Type the following to set up the environment for both Docker and NPM:

```
./setup-env.sh
npm install
```

## Configuration
Configure the files `run.sh` and `run-docker.sh` with your first user. The `Server` has a setup route that creates an initial user.

## Running the Server

Run the following:

```
npm run compose
npm run up
```

Or alternatively:

```
tsc
docker-compose build --no-cache
docker-compose up
```

### Database in Docker, Python locally
Run the following:
```
npm run db
npm start
```

Or with only docker and the shell:

```
docker-compose up db -d
./run.sh
```
### Cleaning up
Shutting down the database and clearing the data:
```
docker-compose down -v
```
#### Additional commands
You may run `tsc` to compile `/src/*.ts` folder into `/dist/*.js`

You may run `webpack` to compile `/src/main.ts` and all dependencies into `/dist/bundle.js`

## Testing
I recently wrote a post that goes into more depth about [testing an HTTP JSON API with Python](http://acostanza.com/2018/01/01/testing-http-json-api-python/). I had actually made that test module specifically while I made the express API. The gist of it is:

#### Setting up Test Environment

```
cd tests
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```
#### Running tests
```
python manyUsers.py
python selectUser.py
python userRoutes.py
```

## Website
Visit my website at [acostanza.com](http://acostanza.com)

This post is also located [here](http://acostanza.com/2018/01/18/auth-api-typescript-express/).
