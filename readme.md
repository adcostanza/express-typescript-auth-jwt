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

To protect a route you may type the following within your async router function:

```
if (!auth.isType("admin")) return res.status(403).send("Unauthorized");
```

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
