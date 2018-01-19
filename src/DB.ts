const { Pool } = require('pg')
import { AuthClaims } from './Auth';
export class DB {

  public pool: any = new Pool({
    user: 'postgres',
    host: process.env.host,
    database: 'postgres',
    password: 'tacos88',
    port: 5432,
  })
  async query(query: string, values?: string[]): Promise<any> {

    if (values === undefined) {
      try {
        const client = await this.pool.connect();
        try {
          const res = await client.query(query);
          //Ensure that there is a result
          if(res.rowCount > 0) return res;
          console.log(query,res);
          return null;
        } catch (e) {
          console.log(query,e);
        }
        finally {
          client.release();
        }
      } catch (e) {
        console.log(query,e)
      }
      return null;
    } else {
      try {
        const client = await this.pool.connect();
        try {
          const res = await client.query(query, values);
          if(res.rowCount > 0) return res;
          console.log(query,values,res);
          return null;
        } catch (e) {
          console.log(query,values,e);
        }
        finally {
          client.release();
        }
      } catch (e) {
        console.log(query,values,e)
      }
      return null;
    }
  }
  async queryRows(query: string, values?: string[]): Promise<any> {

    if (values === undefined) {
      try {
        const client = await this.pool.connect();
        try {
          const res = await client.query(query);
          return res.rows;
        } catch (e) {
          console.log(e);
        }
        finally {
          client.release();
        }
      } catch (e) {
        console.log(e)
      }
      return null;
    } else {
      try {
        const client = await this.pool.connect();
        try {
          const res = await client.query(query, values);
          return res.rows;
        } catch (e) {
          console.log(e);
        }
        finally {
          client.release();
        }
      } catch (e) {
        console.log(e)
      }
      return null;
    }
  }
}
